import anthropic

class AnthropicClaude3API:
    def __init__(self, api_key, model_name="claude-3-opus-20240229"):
        self.api_key = api_key
        self.model_name = model_name
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_completion(self, prompt, max_tokens=1024):
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            messages=[{"role": 'user', "content": prompt}]
        )
        return response
