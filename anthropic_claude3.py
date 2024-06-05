import openai

class OpenAIGPT4oAPI:
    def __init__(self, api_key, model_name="gpt-4o"):
        self.api_key = api_key
        self.model_name = model_name
        openai.api_key = self.api_key

    def generate_completion(self, messages, temperature=0.5, max_tokens=1500, top_p=1, frequency_penalty=0, presence_penalty=0):
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
