import base64
import io
from PIL import Image
import google.generativeai as genai

class GeminiModel:
    def __init__(self):
        genai.configure(api_key="AIzaSyD6NSWFspgQgBOHt2F08VZStEvc37xMBZ4")  # Replace with env variable in production
        self.model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

        self.system_prompt = """
        You are a fashion enrichment and analysis assistant for a fashion recommendation engine.

        Your input will be either:
        - A user query describing a desired outfit or styling preference
        - A single fashion product
        - An image showing an entire outfit or clothing item

        Your job is to extract and infer detailed metadata that can be used to understand the fashion context, and assist recommendation engines.

        Analyze the text and/or image and return a single structured JSON object with:

        - `title`: A concise, descriptive title (e.g., "Monochrome Winter Streetwear Outfit", "Beige Cotton Trench Coat").
        - `description`: A complete natural-language paragraph that summarizes the outfit or product in fashion-oriented language.
        - `items`: A list of one or more detected/described fashion items. Each item should include:
          - `type`: (e.g., jacket, boots, crop top, saree, bag)
          - `color`: Dominant visible color(s)
          - `material`: (e.g., denim, cotton, leather, chiffon)
          - `fit`: (e.g., slim fit, oversized, relaxed)
          - `gender`: Target gender (Men, Women, Unisex)
          - `aesthetic`: Overall aesthetic (e.g., grunge, streetwear, techwear, boho, minimalist, formal)
          - `season`: Season(s) it’s suitable for (e.g., summer, winter, all-season)
          - `occasion`: Best suited occasion(s) (e.g., casual outing, wedding, formal dinner, beach vacation)
          - `tags`: A list of 15–30 rich, relevant, search-optimized fashion tags that combine aesthetics, materials, categories, colors, seasons, style trends.
          - `semantic_category`: "",  # General category (e.g., tops, bottoms, footwear, accessories)
          - `categories`: []  # Breadcrumb-style list from high-level to specific category
        """

    def generate_metadata(self, query=None, image_data=None):
        """Generate structured fashion metadata using Gemini"""
        inputs = [self.system_prompt]

        # Add optional query
        if query and query.strip():
            inputs.append(f"User Query:\n{query.strip()}")

        # Add optional image
        if image_data:
            image_obj = self.decode_base64_image(image_data)
            inputs.append(image_obj)

        # Generate metadata
        response = self.model.generate_content(inputs, stream=False)
        return self._parse_response_text(response.text)

    def decode_base64_image(self, base64_str):
        """Decode base64 image string to PIL Image for Gemini"""
        try:
            header, encoded = base64_str.split(",", 1) if "," in base64_str else ("", base64_str)
            image_bytes = base64.b64decode(encoded)
            return Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            raise ValueError(f"Failed to decode image: {str(e)}")

    def _parse_response_text(self, raw_text):
        """Safely parse Gemini response to return raw JSON-like string"""
        try:
            return eval(raw_text, {"__builtins__": None}, {})  # Or use json.loads() if you format output as JSON string
        except:
            return {"raw_response": raw_text}
