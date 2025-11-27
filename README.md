# Talyn AI Image Generator

A local, privacy-focused AI image generator built with **Streamlit** and **Stable Diffusion**.

## � Project Overview
Talyn is a robust, user-friendly application designed to generate high-quality images from text prompts directly on your local machine. Unlike cloud-based services, Talyn ensures complete privacy by running all computations locally. It leverages the power of **Stable Diffusion** (specifically optimized for photorealism) to create stunning visuals for artists, designers, and hobbyists.

### 🏗️ Architecture
The application follows a modular architecture:
- **Frontend (`app.py`)**: Built with **Streamlit**, providing an interactive web interface for prompt input, parameter tuning, and image gallery display.
- **Backend Logic (`inference.py`)**: Handles the initialization of the Stable Diffusion pipeline, model loading, and hardware acceleration (MPS/CUDA/CPU).
- **Utilities (`utils.py`)**: Contains helper functions for:
    - **Safety**: Keyword filtering and negative prompt enforcement.
    - **Prompt Engineering**: Style preset application.
    - **Post-Processing**: Watermarking and metadata management.
    - **Storage**: File system operations for saving images and JSON metadata.

## 🚀 Features
- **High-Quality Generation**: Uses **Realistic Vision V6.0** (SD 1.5) for photorealistic results.
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

## 💻 Technology Stack & Model Details
- **Language**: Python 3.9+
- **Interface**: Streamlit
- **ML Library**: PyTorch, Diffusers, Transformers
- **Image Processing**: Pillow (PIL)
- **Default Model**: `SG161222/Realistic_Vision_V6.0_B1_noVAE`
    - **Type**: Stable Diffusion 1.5 (Fine-tuned for photorealism)
    - **Resolution**: Optimized for 512x512 and 768x768
    - **License**: CreativeML Open RAIL-M

## 🛠️ Setup & Installation

1.  **Prerequisites**:
    - Python 3.9+ (Python 3.9.6 recommended).
    - **Mac Users**: macOS 12.3+ for MPS support.
    - **Windows/Linux**: CUDA drivers installed (if using NVIDIA GPU).

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```
    *Note: The first run will automatically download the model weights (~2-4 GB). This may take a few minutes depending on your internet connection.*

## 🎨 Usage & Example Prompts

1.  **Open the App**: Go to the local URL provided (e.g., `http://localhost:8506`).
2.  **Enter a Prompt**: Describe your image.
3.  **Select Settings**: Choose a style, number of images, and advanced settings.
4.  **Generate**: Click "Generate".

### Example Prompts
- **Photorealistic**: *"A futuristic city at sunset, cyberpunk style, neon lights, highly detailed, 8k resolution"*
- **Portrait**: *"Portrait of a robot in Van Gogh style, thick brush strokes, starry night background, expressive"*
- **Nature**: *"A serene lake surrounded by mountains, morning mist, reflection, photorealistic, cinematic lighting"*

## 💡 Prompt Engineering Tips
- **Be Specific**: Instead of "a dog", try "a golden retriever puppy running in a park, sunlight, shallow depth of field".
- **Use Style Keywords**: Words like "cinematic", "4k", "masterpiece", "trending on artstation" significantly improve quality.
- **Negative Prompts**: The app handles safety, but you can add terms like "blurry", "distorted", "low contrast" to improve quality further.
- **Aspect Ratio**: For portraits, use 512x768. For landscapes, use 768x512.

## ⚙️ Hardware Requirements
- **GPU (Recommended)**:
    - **Apple Silicon**: M1, M2, M3, M4 (8GB+ RAM recommended).
    - **NVIDIA**: GTX 1060 or higher (4GB+ VRAM).
- **CPU**: Compatible with any modern multi-core CPU (Intel/AMD), but generation will be significantly slower (1-3 mins per image).
- **RAM**: Minimum 8GB system RAM.

## ⚠️ Limitations & Future Improvements
### Limitations
- **Generation Time**: CPU generation is slow.
- **Memory**: High resolutions (1024x1024+) may crash on systems with <16GB RAM using SD 1.5.
- **Text Rendering**: Stable Diffusion 1.5 struggles with rendering legible text inside images.

### Future Improvements
- **Fine-tuning**: Support for LoRA adapters to train on custom datasets.
- **Image-to-Image**: Allow users to upload an image as a starting point.
- **Inpainting**: Edit specific parts of an image.
- **Upscaling**: Integrated AI upscaling for high-resolution export.

## 🛡️ Ethical AI
This tool includes a multi-layer safety system to prevent the generation of harmful, violent, or inappropriate content. All images are watermarked to indicate they are AI-generated.
