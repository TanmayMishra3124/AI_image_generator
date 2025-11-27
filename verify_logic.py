import unittest
from PIL import Image
from utils import check_safety, enhance_prompt, add_watermark, save_image_and_metadata, DEFAULT_NEGATIVE_PROMPT

class TestCoreLogic(unittest.TestCase):
    def test_safety_filter(self):
        # Safe prompt
        is_safe, _ = check_safety("A beautiful sunset")
        self.assertTrue(is_safe)
        
        # Unsafe prompt
        is_safe, reason = check_safety("This contains violence and blood")
        self.assertFalse(is_safe)
        self.assertIn("violence", reason)

        # New restricted keyword test
        is_safe, reason = check_safety("Selling cocaine")
        self.assertFalse(is_safe)
        self.assertIn("cocaine", reason)

    def test_prompt_enhancement(self):
        base = "A cat"
        enhanced = enhance_prompt(base, "Van Gogh")
        self.assertIn("starry night style", enhanced)
        self.assertIn("masterpiece", enhanced)

    def test_default_negative_prompt(self):
        self.assertIn("nsfw", DEFAULT_NEGATIVE_PROMPT)
        self.assertIn("nude", DEFAULT_NEGATIVE_PROMPT)
        self.assertIn("porn", DEFAULT_NEGATIVE_PROMPT)
        self.assertIn("topless", DEFAULT_NEGATIVE_PROMPT)
        self.assertIn("nipples", DEFAULT_NEGATIVE_PROMPT)
        self.assertIn("poorly drawn face", DEFAULT_NEGATIVE_PROMPT)
        self.assertIn("mutation", DEFAULT_NEGATIVE_PROMPT)

    def test_watermark(self):
        # Create a dummy image
        img = Image.new('RGB', (100, 100), color = 'red')
        watermarked = add_watermark(img)
        # Just check if it runs without error and returns an image
        self.assertIsNotNone(watermarked)
        self.assertNotEqual(img, watermarked) # Should be different (modified)

    def test_save_image_custom_filename(self):
        from utils import save_image_and_metadata
        import os
        import shutil
        
        # Setup
        img = Image.new('RGB', (100, 100), color = 'blue')
        prompt = "test prompt"
        params = {"test": "params"}
        output_dir = "test_outputs"
        prefix = "custom_name"
        
        try:
            # Execute
            run_dir, img_path, jpg_path = save_image_and_metadata(img, prompt, params, output_dir=output_dir, filename_prefix=prefix)
            
            # Verify
            self.assertTrue(os.path.exists(img_path))
            self.assertTrue(os.path.exists(jpg_path))
            self.assertIn(f"{prefix}.png", img_path)
            self.assertIn(f"{prefix}.jpg", jpg_path)
            
        finally:
            # Cleanup
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)

if __name__ == '__main__':
    unittest.main()
