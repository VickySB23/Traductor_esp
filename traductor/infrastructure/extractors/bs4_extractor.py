from bs4 import BeautifulSoup
from traductor.application.ports.extractor_port import DocumentExtractorPort
from traductor.domain.entities import Document, TranslationBlock

class BS4Extractor(DocumentExtractorPort):
    def __init__(self):
        self._current_soup = None

    def extract(self, file_path: str) -> Document:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._current_soup = BeautifulSoup(content, 'lxml')
        blocks = []
        
        for i, element in enumerate(self._current_soup.find_all(['p', 'h1', 'h2', 'h3', 'span', 'li'])):
            text = element.get_text(strip=True)
            if text and len(element.find_all(recursive=False)) == 0:
                block_id = f"trans_block_{i}"
                element['data-trans-id'] = block_id
                blocks.append(TranslationBlock(block_id=block_id, original_text=text))
        
        return Document(filename=file_path, blocks=blocks)

    def assemble(self, document: Document, output_path: str) -> None:
        if not self._current_soup:
            raise ValueError("No hay un documento cargado en memoria para ensamblar.")
            
        for block in document.blocks:
            # La doble condición le asegura a Pylance que el texto no es 'None'
            if block.is_translated() and block.translated_text:
                element = self._current_soup.find(attrs={"data-trans-id": block.block_id})
                if element:
                    element.string = block.translated_text
                    del element['data-trans-id']
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(self._current_soup))