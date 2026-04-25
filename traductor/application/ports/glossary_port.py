from abc import ABC, abstractmethod
from typing import Optional
from traductor.domain.entities import GlossaryTerm

class GlossaryPort(ABC):
    """
    Contrato para la Memoria de Traducción. 
    Define cómo interactuamos con la base de datos (SQLite, Postgres, etc.)
    """

    @abstractmethod
    def get_translation(self, original_text: str) -> Optional[GlossaryTerm]:
        """
        Busca un texto exacto en la base de datos.
        Si existe, devuelve la entidad GlossaryTerm. Si no, devuelve None.
        """
        pass

    @abstractmethod
    def save_translation(self, original_text: str, translated_text: str) -> None:
        """
        Guarda una nueva pareja de traducción en la base de datos
        para acelerar futuras ejecuciones.
        """
        pass