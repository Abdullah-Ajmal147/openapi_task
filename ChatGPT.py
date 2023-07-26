import openai


class ChatGPTbotapi:
    def __init__(self, openai_key):
        self.openai_key = openai_key
        self.prompts = []

    def create_prompt(self, prompt):
        max_token_limit = 4096
        token_count = len(openai.ChatCompletion.create(prompt, api_key=self.openai_key).choices[0].message['content'].split())
        if token_count > max_token_limit:
            return None

        self.prompts.append(prompt)
        return len(self.prompts) - 1

    def get_response(self, prompt_id):
        if prompt_id >= 0 and prompt_id < len(self.prompts):
            prompt = self.prompts[prompt_id]

            max_token_limit = 4096
            token_count = len(openai.ChatCompletion.create(prompt, api_key=self.openai_key).choices[0].message['content'].split())
            if token_count <= max_token_limit:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    api_key=self.openai_key
                )
                return response.choices[0].message['content']
            else:
                chunks = [prompt[i:i + max_token_limit] for i in range(0, len(prompt), max_token_limit)]
                full_response = ""
                for chunk in chunks:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": chunk}
                        ],
                        api_key=self.openai_key
                    )
                    full_response += response.choices[0].message['content']
                return full_response
        else:
            return None