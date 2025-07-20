import groq
import re
import logging
from typing import Optional, List
from .memory import Memory

from config import config

class GroqClient:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.memory = Memory(path="grok_memory.json", max_len=30)
        self.client = self._init_client()
        self.async_client = self._init_async_client()
        config.groq_models = self.list_models()
        self.system_prompt = {
            "role": "system",
            "content": (
                "Tu es Mac42 une assistante IA, précis et clair. "
                "Réponds toujours en français."
                "Utilise un langage naturel et évite les jargons techniques. "
                "evite les répétitions et les phrases inutiles. "
            )
        }

    def _init_client(self):
        try:
            return groq.Client(api_key=config.groq_api_key)
        except Exception as e:
            self.logger.error(f"Erreur init Groq: {str(e)}")
            raise

    def _init_async_client(self):
        return groq.AsyncClient(api_key=config.groq_api_key)

    async def async_chat_completion(
        self,
        model: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> Optional[str]:
        context = self.memory.get()
        messages = [self.system_prompt] + context + [{"role": "user", "content": user_message}]

        try:
            response = await self.async_client.chat.completions.create(
                model=model,
                messages=messages,  # type: ignore
                temperature=temperature,
                max_tokens=max_tokens
            )
            answer = self._sanitize_message(str(response.choices[0].message.content))

            self.memory.add("user", user_message)
            self.memory.add("assistant", answer)

            return answer
        except Exception as e:
            self.logger.warning(f"Erreur Groq async (modèle {model}): {str(e)}")
            return None

    def list_models(self) -> List[str]:
        try:
            response = self.client.models.list()
            return [model.id for model in response.data]
        except Exception as e:
            self.logger.error(f"Erreur liste modèles: {str(e)}")
            return ["llama3-70b-8192"]

    def _sanitize_message(self, text: str) -> str:
        text = re.sub(r"<[^>]*>", "", text)
        text = re.sub(r"[^\w\sÀ-ÿ.,!?'-]", "", text)
        return re.sub(r"\s+", " ", text).strip()
