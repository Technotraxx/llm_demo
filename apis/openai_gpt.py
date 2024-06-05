import openai

class OpenAIGPT4oAPI:
    def __init__(self, api_key, model_name="gpt-4o"):
        self.api_key = api_key
        self.model_name = model_name
        openai.api_key = self.api_key

    def generate_completion(self, messages, temperature=1, max_tokens=2048, top_p=1, frequency_penalty=0, presence_penalty=0):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response

# Modellvarianten und Standardwerte
MODELS = {
    "gpt-4o": {
        "description": "Text und Bilder",
        "max_tokens": 4096,
        "default_temperature": 1,
        "default_top_p": 1,
        "default_frequency_penalty": 0,
        "default_presence_penalty": 0,
        "default_max_tokens": 2048
    },
    "gpt-3.5-turbo-16k": {
        "description": "Text",
        "max_tokens": 4096,
        "default_temperature": 1,
        "default_top_p": 1,
        "default_frequency_penalty": 0,
        "default_presence_penalty": 0,
        "default_max_tokens": 2048
    }
}

def get_model_settings(model_name):
    return MODELS.get(model_name, {
        "description": "Unknown model",
        "max_tokens": 4096,
        "default_temperature": 1,
        "default_top_p": 1,
        "default_frequency_penalty": 0,
        "default_presence_penalty": 0,
        "default_max_tokens": 2048
    })
