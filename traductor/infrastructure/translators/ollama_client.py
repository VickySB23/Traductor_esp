import requests
from traductor.application.ports.translator_port import TranslatorPort

class OllamaTranslator(TranslatorPort):
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.base_url = base_url

    def translate_text(self, text: str) -> str:
        # Si nos llega un texto vacío o solo espacios, no perdemos tiempo consultando al modelo
        if not text.strip():
            return ""

        # El "System Prompt": Le damos un rol claro y reglas estrictas para que no nos devuelva basura
        prompt = (
            "You are a professional literary translator. "
            "Translate the following text from English to Spanish. "
            "Respond ONLY with the translated Spanish text, no explanations, no quotes, no markdown.\n\n"
            f"Original text: {text}"
        )

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False  # Queremos la respuesta completa de una sola vez
        }

        try:
            # Enviamos la petición al servidor local de Ollama
            response = requests.post(self.base_url, json=payload, timeout=120)
            
            # Esto lanza una excepción si Ollama devuelve un error (ej. error 500)
            response.raise_for_status() 
            
            data = response.json()
            # Extraemos puramente el texto de la respuesta y le sacamos espacios extra
            return data.get("response", "").strip()
            
        except requests.RequestException as e:
            # En un sistema para producción, acá levantaríamos una Custom Exception de nuestro dominio
            raise RuntimeError(f"Error comunicándose con Ollama local: {e}")