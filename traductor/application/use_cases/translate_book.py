import concurrent.futures
from tqdm import tqdm
from traductor.application.ports.extractor_port import DocumentExtractorPort
from traductor.application.ports.translator_port import TranslatorPort
from traductor.application.ports.glossary_port import GlossaryPort

class TranslateBookUseCase:
    def __init__(
        self, 
        extractor: DocumentExtractorPort, 
        translator: TranslatorPort,
        glossary: GlossaryPort
    ):
        self.extractor = extractor
        self.translator = translator
        self.glossary = glossary

    def _process_block(self, block):
        """Esta es la tarea individual que hará cada hilo"""
        cached_term = self.glossary.get_translation(block.original_text)
        
        if cached_term:
            block.translated_text = cached_term.translation
        else:
            translated = self.translator.translate_text(block.original_text)
            block.translated_text = translated
            if translated and translated.strip():
                self.glossary.save_translation(block.original_text, translated)
        return block

    def execute(self, input_path: str, output_path: str) -> None:
        document = self.extractor.extract(input_path)
        pending_blocks = document.get_pending_blocks()
        
        # max_workers=4 significa que 4 párrafos se traducen simultáneamente
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Enviamos todos los bloques a los trabajadores
            futures = {executor.submit(self._process_block, block): block for block in pending_blocks}
            
            # Envolvemos con tqdm para seguir viendo la barra de progreso
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(pending_blocks), desc="Traduciendo libro", unit="bloque"):
                pass # El trabajo pesado ya se hizo en _process_block
            
        self.extractor.assemble(document, output_path)