from abc import ABC, abstractmethod
from traductor.domain.entities import Document

class DocumentExtractorPort(ABC):
    """
    Contrato que cualquier extractor (EPUB, PDF, HTML) debe cumplir.
    La lógica de negocio solo hablará con estos métodos.
    """

    @abstractmethod
    def extract(self, file_path: str) -> Document:
        """
        Debe abrir un archivo, extraer el texto útil y devolver 
        una entidad Document pura del dominio.
        """
        pass

    @abstractmethod
    def assemble(self, document: Document, output_path: str) -> None:
        """
        Debe tomar un Document (ya con los bloques traducidos) y 
        generar el archivo final en disco, preservando la estructura.
        """
        pass