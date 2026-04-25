from traductor.domain.entities import TranslationBlock, Document

def test_translation_block_status():
    block = TranslationBlock(block_id="p_01", original_text="Texto confidencial")
    
    # Al crearse, no debería estar traducido
    assert not block.is_translated()
    
    # Al asignarle texto, debería cambiar su estado
    block.translated_text = "Confidential text"
    assert block.is_translated()

def test_document_pending_blocks():
    doc = Document(
        filename="reporte.epub",
        blocks=[
            TranslationBlock("1", "Capítulo 1", "Chapter 1"),
            TranslationBlock("2", "Texto secreto") # Falta traducir
        ]
    )
    
    pending = doc.get_pending_blocks()
    
    # Debería detectar que solo falta 1 bloque por traducir
    assert len(pending) == 1
    assert pending[0].block_id == "2"