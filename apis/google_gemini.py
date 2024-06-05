import google.generativeai as genai

class GoogleGeminiAPI:
    def __init__(self, api_key, model_name="gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)

    def generate_content(self, prompt, temperature=1, top_p=0.95, max_output_tokens=2048):
        response = genai.generate_text(
            model=self.model_name,
            prompt=prompt,
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_output_tokens
        )
        return response

# Modellvarianten und Standardwerte
MODELS = {
    "gemini-1.5-pro": {
        "description": "Audio, Bilder, Videos und Text",
        "max_output_tokens": 8096,
        "default_temperature": 1.0,
        "default_top_p": 0.95,
        "default_max_output_tokens": 2048
    },
    "gemini-1.5-flash": {
        "description": "Audio, Bilder, Videos und Text",
        "max_output_tokens": 8096,
        "default_temperature": 1.0,
        "default_top_p": 0.95,
        "default_max_output_tokens": 2048
    },
    "gemini-1.0-pro": {
        "description": "Text",
        "max_output_tokens": 8096,
        "default_temperature": 1.0,
        "default_top_p": 0.95,
        "default_max_output_tokens": 2048
    },
    "gemini-pro-vision": {
        "description": "Bilder, Videos und Text",
        "max_output_tokens": 8096,
        "default_temperature": 1.0,
        "default_top_p": 0.95,
        "default_max_output_tokens": 2048
    }
}

def get_model_settings(model_name):
    return MODELS.get(model_name, {
        "description": "Unknown model",
        "max_output_tokens": 8096,
        "default_temperature": 1.0,
        "default_top_p": 0.95,
        "default_max_output_tokens": 2048
    })
