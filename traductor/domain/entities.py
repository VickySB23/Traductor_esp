from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TranslationBlock:
    block_id: str
    original_text: str
    translated_text: Optional[str] = None

    def is_translated(self) -> bool:
        return bool(self.translated_text and self.translated_text.strip())

@dataclass
class Document:
    filename: str
    blocks: list[TranslationBlock] = field(default_factory=list)

    def get_pending_blocks(self) -> list[TranslationBlock]:
        return [block for block in self.blocks if not block.is_translated()]

# --- NUEVO CÓDIGO ---
@dataclass
class GlossaryTerm:
    """Representa una pareja de traducción ya aprobada en la base de datos."""
    original: str
    translation: str