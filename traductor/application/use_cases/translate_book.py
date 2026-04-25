from traductor.application.ports.extractor_port import DocumentExtractorPort
from traductor.application.ports.translator_port import TranslatorPort

class TranslateBookUseCase:
    def __init__(self, extractor: DocumentExtractorPort, translator: TranslatorPort):
        # Inyección de dependencias: recibimos las herramientas por el constructor
        self.extractor = extractor
        self.translator = translator

    def execute(self, input_path: str, output_path: str) -> None:
        """Orquesta todo el flujo de traducción de un documento."""
        
        # 1. Extraemos el documento (El extractor nos devuelve la entidad Document)
        document = self.extractor.extract(input_path)
        
        # 2. Buscamos qué bloques faltan traducir
        pending_blocks = document.get_pending_blocks()
        
        # 3. Traducimos cada bloque
        for block in pending_blocks:
            translated = self.translator.translate_text(block.original_text)
            block.translated_text = translated
            
        # 4. Ensamblamos el documento final con los textos actualizados
        self.extractor.assemble(document, output_path)