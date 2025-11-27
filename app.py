import streamlit as st
import time
import random
from inference import ImageGenerator
from utils import check_safety, enhance_prompt, add_watermark, save_image_and_metadata, STYLE_PRESETS, DEFAULT_NEGATIVE_PROMPT

# Page Config
st.set_page_config(
    page_title="Talyn AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Initialize Model (Cached)
@st.cache_resource
def get_generator():
    return ImageGenerator()

try:
    generator = get_generator()
except Exception as e:
    st.error(f"Failed to initialize model: {e}")
    st.stop()

# Sidebar Controls
st.sidebar.title("🎨 Configuration")

prompt = st.sidebar.text_area("Enter your prompt:", height=100, placeholder="A futuristic city at sunset...")
negative_prompt = st.sidebar.text_input("Negative Prompt (Optional):", placeholder="blurry, distorted, low quality")

style = st.sidebar.selectbox("Style Preference", ["None"] + list(STYLE_PRESETS.keys()))

num_images = st.sidebar.slider("Number of Images", 1, 4, 1)

filename_prefix = st.sidebar.text_input("Filename Prefix", value="image", help="Prefix for saved filenames")

with st.sidebar.expander("Advanced Settings"):
    steps = st.slider("Inference Steps", min_value=10, max_value=100, value=30)
    guidance_scale = st.slider("Guidance Scale", min_value=1.0, max_value=20.0, value=7.5)
    width = st.selectbox("Width", [512, 768], index=0)
    height = st.selectbox("Height", [512, 768], index=0)
    seed = st.number_input("Seed (Optional)", value=0, min_value=0, step=1)
    use_random_seed = st.checkbox("Random Seed", value=True)

if use_random_seed:
    seed = None
elif seed == 0:
    seed = None

# Main Content
st.title("✨ AI-Powered Image Generator")
st.markdown("Generate high-quality images locally using Stable Diffusion.")

if st.sidebar.button("Generate", type="primary"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        # 1. Safety Check
        # Sanitize prompt to remove newlines and extra spaces
        clean_prompt = prompt.replace("\n", " ").strip()
        
        is_safe, reason = check_safety(clean_prompt)
        if not is_safe:
            st.error(f"🚫 Request Blocked: {reason}")
        else:
            # 2. Prompt Engineering
            final_prompt = enhance_prompt(prompt, style if style != "None" else None)
            
            # Display processing info
            with st.status("Processing...", expanded=True) as status:
                st.write("🔍 Validating prompt... Safe.")
                st.write(f"✨ Enhancing prompt: '{final_prompt}'")
                
                # 3. Generation Loop
                generated_images = []
                start_time = time.time()
                
                progress_bar = st.progress(0)
                
                for i in range(num_images):
                    st.write(f"🎨 Generating image {i+1}/{num_images}...")
                    
                    # Use a specific seed for each image if not random, or let generator handle it
                    current_seed = seed if seed is not None else random.randint(0, 2**32 - 1)
                    
                    try:
                        # Force-append safety negative prompt to ensure it's always applied
                        final_negative_prompt = f"{negative_prompt}, {DEFAULT_NEGATIVE_PROMPT}" if negative_prompt else DEFAULT_NEGATIVE_PROMPT
                        
                        img = generator.generate(
                            final_prompt,
                            negative_prompt=final_negative_prompt,
                            steps=steps,
                            guidance_scale=guidance_scale,
                            seed=current_seed,
                            width=width,
                            height=height
                        )
                        
                        # 4. Post-processing
                        st.write("🏷️ Adding watermark...")
                        watermarked_img = add_watermark(img)
                        
                        # 5. Storage
                        st.write("💾 Saving to disk...")
                        params = {
                            "original_prompt": prompt,
                            "final_prompt": final_prompt,
                            "negative_prompt": negative_prompt,
                            "steps": steps,
                            "guidance_scale": guidance_scale,
                            "seed": current_seed,
                            "style": style
                        }
                        run_dir, img_path, img_jpg_path = save_image_and_metadata(watermarked_img, final_prompt, params, filename_prefix=f"{filename_prefix}_{i+1}")
                        
                        generated_images.append({
                            "image": watermarked_img,
                            "path": img_path,
                            "jpg_path": img_jpg_path,
                            "seed": current_seed,
                            "dir": run_dir
                        })
                        
                        progress_bar.progress((i + 1) / num_images)
                        
                    except Exception as e:
                        st.error(f"Error generating image {i+1}: {e}")
                
                end_time = time.time()
                status.update(label="✅ Generation Complete!", state="complete", expanded=False)
            
            # 6. Display Results
            st.success(f"Generated {num_images} images in {end_time - start_time:.2f} seconds.")
            
            cols = st.columns(num_images)
            for idx, item in enumerate(generated_images):
                with cols[idx]:
                    st.image(item["image"], use_container_width=True)
                    st.caption(f"Seed: {item['seed']}")
                    st.text(f"Saved to: {item['dir']}")
                    
                    # Download buttons
                    # We need to read the file back to bytes for the download button
                    with open(item["path"], "rb") as file:
                        btn = st.download_button(
                            label="Download PNG",
                            data=file,
                            file_name=f"generated_image_{idx+1}.png",
                            mime="image/png",
                            key=f"dl_png_{idx}"
                        )
                    
                    with open(item["jpg_path"], "rb") as file:
                        btn_jpg = st.download_button(
                            label="Download JPEG",
                            data=file,
                            file_name=f"{filename_prefix}_{idx+1}.jpg",
                            mime="image/jpeg",
                            key=f"dl_jpg_{idx}"
                        )

st.markdown("---")
st.markdown("🔒 **Privacy Focused**: All processing happens locally. No data leaves your machine.")
