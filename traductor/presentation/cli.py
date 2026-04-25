import argparse
import sys
from traductor.infrastructure.extractors.bs4_extractor import BS4Extractor
from traductor.infrastructure.extractors.epub_extractor import EpubExtractor
from traductor.infrastructure.translators.ollama_client import OllamaTranslator
from traductor.infrastructure.database.sqlite_glossary import SQLiteGlossary
from traductor.application.use_cases.translate_book import TranslateBookUseCase

def run():
    parser = argparse.ArgumentParser(description="Traductor de documentos 100% local y confidencial.")
    parser.add_argument("input", help="Ruta del archivo original (HTML o EPUB)")
    parser.add_argument("output", help="Ruta donde se guardará el archivo traducido")
    parser.add_argument("--model", default="llama3", help="Modelo de Ollama a utilizar")
    
    args = parser.parse_args()

    print(f"[*] Preparando entorno aislado para: {args.input}")
    
    # --- COMPOSITION ROOT ---
    # 1. Instanciamos el extractor correcto según la extensión
    if args.input.lower().endswith(".epub"):
        extractor = EpubExtractor()
    else:
        extractor = BS4Extractor()
        
    # 2. Instanciamos el motor de IA y la Base de Datos
    translator = OllamaTranslator(model_name=args.model)
    glossary = SQLiteGlossary() # Se guardará en data/glossary.sqlite3
    
    # 3. Inyectamos TODAS las dependencias en nuestro Caso de Uso
    use_case = TranslateBookUseCase(
        extractor=extractor, 
        translator=translator,
        glossary=glossary
    )

    print(f"[*] Conectando con motor local de IA ({args.model})...")
    print("[*] Procesando bloques de texto. Usando Memoria de Traducción (Glosario)...")
    
    try:
        use_case.execute(input_path=args.input, output_path=args.output)
        print(f"\n[+] ¡Éxito! Documento traducido guardado de forma segura en: {args.output}")
    except Exception as e:
        print(f"\n[-] Error crítico durante la ejecución: {e}")
        sys.exit(1)