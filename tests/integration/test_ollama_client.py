from unittest.mock import patch
from traductor.infrastructure.translators.ollama_client import OllamaTranslator

# Usamos @patch para interceptar la función "post" de la librería requests
@patch('traductor.infrastructure.translators.ollama_client.requests.post')
def test_ollama_translator_success(mock_post):
    # 1. Configuramos el "mock" para que devuelva una respuesta falsa exitosa (Status 200)
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "This is a highly confidential text."}

    # 2. Instanciamos nuestro cliente
    translator = OllamaTranslator(model_name="llama3")
    
    # 3. Ejecutamos la traducción
    result = translator.translate_text("Este es un texto súper confidencial.")

    # 4. Verificamos que extrajo la traducción correcta del JSON simulado
    assert result == "This is a highly confidential text."

    # 5. Verificamos que el payload se armó correctamente con las reglas estrictas
    called_args, called_kwargs = mock_post.call_args
    payload_enviado = called_kwargs['json']
    
    assert payload_enviado['model'] == 'llama3'
    assert "Este es un texto súper confidencial." in payload_enviado['prompt']
    assert "Respond ONLY with the translated English text" in payload_enviado['prompt']