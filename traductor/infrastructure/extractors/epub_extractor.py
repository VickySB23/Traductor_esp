import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from traductor.application.ports.extractor_port import DocumentExtractorPort
from traductor.domain.entities import Document, TranslationBlock
import warnings
from bs4 import XMLParsedAsHTMLWarning

# Le decimos a Python que ignore esta advertencia específica
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


class EpubExtractor(DocumentExtractorPort):
    def __init__(self):
        self._current_book = None
        self._chapters = {} 

    def extract(self, file_path: str) -> Document:
        self._current_book = epub.read_epub(file_path)
        all_blocks = []
        
        for item in self._current_book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            chapter_id = item.get_id()
            soup = BeautifulSoup(item.get_content(), 'lxml')
            self._chapters[chapter_id] = soup
            
            for i, element in enumerate(soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])):
                text = element.get_text(strip=True)
                if text and len(element.find_all(recursive=False)) == 0:
                    block_id = f"{chapter_id}||{i}"
                    element['data-trans-id'] = block_id
                    
                    all_blocks.append(TranslationBlock(
                        block_id=block_id,
                        original_text=text
                    ))
        
        return Document(filename=file_path, blocks=all_blocks)

    def assemble(self, document: Document, output_path: str) -> None:
        if not self._current_book:
            raise ValueError("No hay un libro cargado.")

        for block in document.blocks:
            if block.is_translated() and block.translated_text:
                chapter_id, _ = block.block_id.split("||")
                soup = self._chapters.get(chapter_id)
                if soup:
                    element = soup.find(attrs={"data-trans-id": block.block_id})
                    if element:
                        element.string = block.translated_text
                        del element['data-trans-id']

        for item in self._current_book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            chapter_id = item.get_id()
            if chapter_id in self._chapters:
                item.set_content(str(self._chapters[chapter_id]).encode('utf-8'))

        epub.write_epub(output_path, self._current_book)