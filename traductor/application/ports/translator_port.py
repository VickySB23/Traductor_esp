from abc import ABC, abstractmethod

class TranslatorPort(ABC):
    """
    Contrato para el motor de traducción (Ollama, DeepL, GPT, etc.).
    """

    @abstractmethod
    def translate_text(self, text: str) -> str:
        """
        Recibe un texto en español y debe devolver pura y exclusivamente
        la traducción al inglés.
        """
        pass