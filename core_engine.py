import os
import json
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont

class FormatEngine:
    def __init__(self):
        # Præcise pixel-dimensioner ud fra dine specifikationer
        self.resolutions = {
            "24:9": (1536, 576),
            "16:9": (1920, 1080)
        }

    def analyze_slide(self, image_path, target_lang="English"):
        """
        TRIN 1: Simuleret AI analyse med neutrale konference-data.
        (Når vi sætter ægte AI på, lægger vi API-kaldet ind her)
        """
        ai_data = {
            "background_hex": "#0F172A", 
            "text_content": "Velkommen til den årlige konference. Vi glæder os til at præsentere dagens program.",
            "translated_text": "Welcome to the annual conference. We look forward to presenting today's program."
        }
        
        return ai_data

    def split_text(self, text, max_lines):
        """
        TRIN 2: Auto-split tekst hvis den overskrider grænsen.
        """
        words = text.split(" ")
        max_words_per_slide = max_lines * 8 
        
        slides_text = []
        current_slide = []
        
        for word in words:
            current_slide.append(word)
            if len(current_slide) >= max_words_per_slide:
                slides_text.append(" ".join(current_slide))
                current_slide = []
                
        if current_slide:
            slides_text.append(" ".join(current_slide))
            
        return slides_text

    def render_image(self, slide_data, format_type="24:9", layout="split"):
        """
        TRIN 3: Generer det nye PNG billede baseret på data og eksakte pixels.
        """
        width, height = self.resolutions.get(format_type, (1920, 1080))
        
        # Opret et nyt tomt lærred med baggrundsfarven
        new_slide = Image.new("RGB", (width, height), color=slide_data["background_hex"])
        draw = ImageDraw.Draw(new_slide)
        
        # Indlæs en standard skrifttype
        try:
            font_title = ImageFont.truetype("arial.ttf", 60)
            font_body = ImageFont.truetype("arial.ttf", 45)
        except IOError:
            font_title = ImageFont.load_default()
            font_body = ImageFont.load_default()

        # Layout logik: Split side-om-side for 24:9
        if layout == "split" and format_type == "24:9":
            # Originaltekst til venstre
            draw.text((100, 100), "ORIGINAL:", fill="white", font=font_title)
            draw.text((100, 200), slide_data["text_content"], fill="white", font=font_body)
            
            # Oversat tekst til højre
            draw.text((width // 2 + 50, 100), "TRANSLATION:", fill="gray", font=font_title)
            draw.text((width // 2 + 50, 200), slide_data["translated_text"], fill="gray", font=font_body)

        elif layout == "over_under":
            # Originaltekst øverst, oversættelse nederst
            draw.text((100, 100), slide_data["text_content"], fill="white", font=font_title)
            draw.text((100, 300), slide_data["translated_text"], fill="gray", font=font_body)

        return new_slide