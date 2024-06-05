import anthropic

class AnthropicClaudeAPI:
    def __init__(self, api_key, model_name="claude-3-opus-20240229"):
        self.api_key = api_key
        self.model_name = model_name
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_completion(self, prompt, max_tokens=2048, temperature=1):
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": 'user', "content": prompt}]
        )
        return response

# Modellvarianten und Standardwerte
MODELS = {
    "claude-3-opus-20240229": {
        "description": "Text und Bilder",
        "max_tokens": 4096,
        "default_temperature": 1,
        "default_max_tokens": 2048
    },
    "claude-3-sonnet-20240229": {
        "description": "Text und Bilder",
        "max_tokens": 4096,
        "default_temperature": 1,
        "default_max_tokens": 2048
    },
    "claude-3-haiku-20240307": {
        "description": "Text und Bilder",
        "max_tokens": 4096,
        "default_temperature": 1,
        "default_max_tokens": 2048
    }
}

def get_model_settings(model_name):
    return MODELS.get(model_name, {
        "description": "Unknown model",
        "max_tokens": 4096,
        "default_temperature": 1,
        "default_max_tokens": 2048
    })
