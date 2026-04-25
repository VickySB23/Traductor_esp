import sqlite3
import os
from typing import Optional
from traductor.application.ports.glossary_port import GlossaryPort
from traductor.domain.entities import GlossaryTerm

class SQLiteGlossary(GlossaryPort):
    def __init__(self, db_path: str = "data/glossary.sqlite3"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Crea la tabla si es la primera vez que se ejecuta el programa."""
        # Aseguramos que la carpeta exista
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Usamos el texto original como clave primaria para búsquedas súper rápidas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    original_text TEXT PRIMARY KEY,
                    translated_text TEXT NOT NULL
                )
            """)
            conn.commit()

    def get_translation(self, original_text: str) -> Optional[GlossaryTerm]:
        # Agregamos timeout=15
        with sqlite3.connect(self.db_path, timeout=15) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT translated_text FROM translations WHERE original_text = ?", 
                (original_text,)
            )
            row = cursor.fetchone()
            
            if row:
                return GlossaryTerm(original=original_text, translation=row[0])
            return None

    ddef save_translation(self, original_text: str, translated_text: str) -> None:
        # Agregamos timeout=15
        with sqlite3.connect(self.db_path, timeout=15) as conn:
            cursor = conn.cursor()
            # INSERT OR IGNORE evita errores si por alguna razón intentamos guardar el mismo texto dos veces
            cursor.execute(
                "INSERT OR IGNORE INTO translations (original_text, translated_text) VALUES (?, ?)",
                (original_text, translated_text)
            )
            conn.commit()