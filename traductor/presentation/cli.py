import argparse
import sys
from traductor.infrastructure.extractors.bs4_extractor import BS4Extractor
from traductor.infrastructure.translators.ollama_client import OllamaTranslator
from traductor.application.use_cases.translate_book import TranslateBookUseCase

def run():
    # 1. Configuramos la interfaz de terminal
    parser = argparse.ArgumentParser(description="Traductor de documentos 100% local y confidencial.")
    parser.add_argument("input", help="Ruta del archivo HTML original")
    parser.add_argument("output", help="Ruta donde se guardará el archivo traducido")
    parser.add_argument("--model", default="llama3", help="Modelo de Ollama a utilizar (ej. llama3, mistral)")
    
    args = parser.parse_args()

    print(f"[*] Preparando entorno aislado para: {args.input}")
    
    # 2. COMPOSITION ROOT: Instanciamos las infraestructuras reales
    extractor = BS4Extractor()
    translator = OllamaTranslator(model_name=args.model)
    
    # 3. Inyectamos las dependencias en nuestro Caso de Uso (El cerebro)
    use_case = TranslateBookUseCase(extractor=extractor, translator=translator)

    # 4. Ejecutamos el flujo
    print(f"[*] Conectando con motor local de IA ({args.model})...")
    print("[*] Procesando bloques de texto. Esto puede demorar dependiendo del hardware...")
    
    try:
        use_case.execute(input_path=args.input, output_path=args.output)
        print(f"\n[+] ¡Éxito! Documento traducido guardado de forma segura en: {args.output}")
    except Exception as e:
        print(f"\n[-] Error crítico durante la ejecución: {e}")
        sys.exit(1)