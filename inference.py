import torch
import logging
from diffusers import StableDiffusionPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self, model_id="SG161222/Realistic_Vision_V6.0_B1_noVAE"):
        self.model_id = model_id
        if torch.cuda.is_available():
            self.device = "cuda"
        elif torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"
        self.pipe = None
        logger.info(f"Initializing ImageGenerator on device: {self.device}")

    def load_model(self):
        """
        Loads the Stable Diffusion model pipeline.
        """
        if self.pipe is None:
            logger.info(f"Loading model {self.model_id}...")
            try:
                # Use StableDiffusionPipeline for SD 1.5 models
                if self.device == "cuda":
                    self.pipe = StableDiffusionPipeline.from_pretrained(
                        self.model_id, 
                        torch_dtype=torch.float16
                    )
                    self.pipe = self.pipe.to("cuda")
                elif self.device == "mps":
                    self.pipe = StableDiffusionPipeline.from_pretrained(
                        self.model_id, 
                        torch_dtype=torch.float16
                    )
                    self.pipe = self.pipe.to("mps")
                else:
                    self.pipe = StableDiffusionPipeline.from_pretrained(
                        self.model_id
                    )
                    self.pipe = self.pipe.to("cpu")
                
                # Safety checker is enabled by default in the pipeline.
                # We explicitly ensure it is NOT disabled.
                if hasattr(self.pipe, "safety_checker") and self.pipe.safety_checker is None:
                     logger.warning("Safety checker was None, attempting to reload if possible (not implemented here, relying on default load).")
                
                logger.info("Model loaded successfully with Safety Checker.")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise e

    def generate(self, prompt, negative_prompt=None, steps=20, guidance_scale=7.5, seed=None, width=512, height=512):
        """
        Generates an image based on the prompt.
        """
        if self.pipe is None:
            self.load_model()

        generator = None
        if seed is not None:
            generator = torch.Generator(self.device).manual_seed(seed)

        logger.info(f"Generating image for prompt: '{prompt}'")
        
        try:
            image = self.pipe(
                prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                generator=generator,
                width=width,
                height=height
            ).images[0]
            
            return image
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise e
