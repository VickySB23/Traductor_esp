from traductor.domain.entities import Document, TranslationBlock
from traductor.application.ports.extractor_port import DocumentExtractorPort
from traductor.application.ports.translator_port import TranslatorPort
from traductor.application.use_cases.translate_book import TranslateBookUseCase

# --- 1. Creamos Fakes para simular la infraestructura ---

class FakeExtractor(DocumentExtractorPort):
    def extract(self, file_path: str) -> Document:
        # Simulamos que leímos un archivo y encontramos dos párrafos
        blocks = [
            TranslationBlock("1", "Hola"),
            TranslationBlock("2", "Mundo confidencial")
        ]
        return Document(filename=file_path, blocks=blocks)

    def assemble(self, document: Document, output_path: str) -> None:
        # Simulamos el guardado. En una prueba real, podríamos verificar
        # que este método fue llamado y con qué datos.
        self.last_saved_document = document
        self.last_output_path = output_path

class FakeTranslator(TranslatorPort):
    def translate_text(self, text: str) -> str:
        # Un traductor bobo que solo agrega un prefijo
        return f"EN_{text}"

# --- 2. La Prueba Unitaria del Caso de Uso ---

def test_translate_book_flow():
    # Preparamos las herramientas falsas
    fake_extractor = FakeExtractor()
    fake_translator = FakeTranslator()
    
    # Instanciamos el caso de uso inyectando las dependencias
    use_case = TranslateBookUseCase(fake_extractor, fake_translator)
    
    # Ejecutamos el flujo
    use_case.execute("input.epub", "output.epub")
    
    # Verificamos los resultados en el extractor falso
    saved_doc = fake_extractor.last_saved_document
    assert fake_extractor.last_output_path == "output.epub"
    
    # Verificamos que los bloques fueron efectivamente traducidos
    assert saved_doc.blocks[0].translated_text == "EN_Hola"
    assert saved_doc.blocks[1].translated_text == "EN_Mundo confidencial"
    assert saved_doc.blocks[0].is_translated() is True