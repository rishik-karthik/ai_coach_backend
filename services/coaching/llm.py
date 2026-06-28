from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue):
        prompt = f"Event: {event}"

        if issue:
            prompt += f" Form Issue: {issue}"
            #This is the most important part of the code. LLMs don't inherently remember the past; 
            # you have to send them the entire conversation history every single time you ask a question.
            # It puts the System Prompt at the very top so the AI remembers its personality.
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:], #The * unpacks the list, and [-10:] grabs only the last 10 messages.
            {"role": "user", "content": prompt}
        ]
        #groq api key-> chat feature-> completions -> make request to server
        #completion : A specific class inside chat. In AI terminology, a "completion" is when you give an AI a prompt, and it completes the thought.
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
        )

        text = response.choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": text})

        return text
    