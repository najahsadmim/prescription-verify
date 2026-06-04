import sys
import torch
from transformers import pipeline
from exception import InvalidImageError

class TextExtractionEngine:
    def __init__(self, model_name: str="Salesforce/blip-image-captioning-base"):
        self.model_name=model_name
        self.device= 0 if torch.cuda.is_available() else -1
        print(f"[Engine] Initializing Hugging Face pipeline on device ID {self.device}")
        
        self.pipeline= pipeline("image-to-text", model=self.model_name, device=self.device)
        
    def extract_text(self, image_path: str) -> str:
        print(f"[Engine] Processing asset matrix for: {image_path}...")
        
        try:
            with open(image_path, "rb") as file_check:
                pass
            
        except FileNotFoundError:
            error_type, error_msg, traceback=sys.exc_info()
            raise InvalidImageError(f"Sys Runtime Error: Target file not found -> {image_path}")
        
        except Exception as e:
            raise InvalidImageError(f"Sys Runtime Error: Cannot reach file layer -> {e}")
        
        outputs=self.pipeline(image_path)
        if not outputs or 'generated_text' not in outputs[0]:
            return ""
        return outputs[0]['generated_text']