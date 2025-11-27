# Talyn AI Image Generator

A local, privacy-focused AI image generator built with **Streamlit** and **Stable Diffusion**.

## 🚀 Features
- **High-Quality Generation**: Currently configured with **Realistic Vision V6.0** (SD 1.5) for excellent photorealism with low resource usage.
- **Text-to-Image**: Generate images from text prompts with adjustable parameters.
- **Style Presets**: Enhance prompts with presets like Photorealistic, Artistic, Anime, etc.
- **Robust Safety**:
    - **Keyword Filter**: Blocks explicit prompts.
    - **Negative Prompt Enforcement**: Force-appends safety terms to prevent NSFW generation.
    - **Internal Safety Checker**: Scans generated images to block inappropriate content.
- **Local Execution**: Runs entirely on your machine.
    - **Mac M-Series**: Uses **MPS** (Metal Performance Shaders) for acceleration.
    - **NVIDIA**: Uses **CUDA**.
    - **CPU**: Automatic fallback.
- **Watermarking**: Adds "AI-generated" labels to images.
- **Storage & Export**: Automatically saves images (PNG & JPEG) and metadata to timestamped folders.

## ⚙️ Model Flexibility (SDXL Support)
This application is optimized for **Stable Diffusion 1.5** (Realistic Vision V6.0) for the best balance of speed and quality on consumer hardware.

**Want higher quality?**
The code supports **SDXL (Stable Diffusion XL)** models like `RealVisXL V4.0` or `Segmind SSD-1B`.
To upgrade:
1. Open `inference.py`.
2. Change `StableDiffusionPipeline` to `StableDiffusionXLPipeline`.
3. Update `model_id` to an SDXL model (e.g., `SG161222/RealVisXL_V4.0`).
4. In `app.py`, update the default resolution to `1024x1024`.

*Note: SDXL requires significantly more RAM and VRAM.*

## 🛠️ Setup

1.  **Prerequisites**:
    - Python 3.9+ (Python 3.9.6 recommended).
    - **Mac Users**: macOS 12.3+ for MPS support.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

## 🎨 Usage
1.  Open the local URL provided by Streamlit (usually http://localhost:8501).
2.  **Prompt**: Enter a description of the image you want.
3.  **Settings**: Adjust number of images, style, and advanced settings (steps, guidance) in the sidebar.
4.  **Generate**: Click the "Generate" button.
5.  **Download**: View the gallery and download images in PNG or JPEG format.

## 💻 Hardware Support
- **Apple Silicon (M1/M2/M3/M4)**: Automatically detects and uses **MPS** for fast generation.
- **NVIDIA GPUs**: Automatically detects and uses **CUDA**.
- **CPU**: Works on any machine, but generation will be slower.

## 🛡️ Ethical AI
This tool includes a multi-layer safety system to prevent the generation of harmful, violent, or inappropriate content. All images are watermarked to indicate they are AI-generated.
