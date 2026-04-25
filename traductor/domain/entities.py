from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TranslationBlock:
    """Representa un fragmento de texto aislado que necesita traducción."""
    block_id: str             # ID único para saber de qué nodo HTML vino
    original_text: str        # El texto original en español
    translated_text: Optional[str] = None  # El texto en inglés (arranca vacío)

    def is_translated(self) -> bool:
        """Verifica si el bloque ya fue procesado y tiene contenido."""
        return bool(self.translated_text and self.translated_text.strip())

@dataclass
class Document:
    """Representa el libro completo gestionado en memoria."""
    filename: str
    blocks: list[TranslationBlock] = field(default_factory=list)

    def get_pending_blocks(self) -> list[TranslationBlock]:
        """Devuelve solo los bloques que faltan traducir."""
        return [block for block in self.blocks if not block.is_translated()]