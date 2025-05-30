# gemini_model.py
import google.generativeai as genai
from PIL import Image
import json
import io
import base64

# === Setup Gemini API ===
genai.configure(api_key="AIzaSyD6NSWFspgQgBOHt2F08VZStEvc37xMBZ4")
model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

# === System Prompt ===
system_prompt = """
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
  - `aesthetic`: Overall aesthetic (e.g., grunge, streetwear, techwear, boho, minimalist, formal).
  - `season`: Season(s) it’s suitable for (e.g., summer, winter, all-season).
  - `occasion`: Best suited occasion(s) (e.g., casual outing, wedding, formal dinner, beach vacation)
  - `tags`: A list of 15–30 rich, relevant, search-optimized fashion tags that combine aesthetics, materials, categories, colors, seasons, style trends.
  - `semantic_category`:"", # General category (e.g., tops, bottoms, footwear, accessories)
  - `categories`: [], # Breadcrumb-style list from high-level to specific category
"""

class GeminiModel:
    def __init__(self):
        self.model = model
        self.prompt = system_prompt

    def generate_metadata(self, query=None, image_data=None):
        inputs = [self.prompt]
        if query:
            inputs.append(f"User Query:\n{query.strip()}")

        if image_data:
            try:
                image = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
                inputs.append(image)
            except Exception as e:
                raise ValueError("Image decoding failed") from e

        response = self.model.generate_content(inputs, stream=False)
        return json.loads(response.text)
