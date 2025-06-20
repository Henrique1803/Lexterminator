from pathlib import Path

"""
Utilitários para o uso de paths ao salvar e abrir arquivos, 
tomando o caminho absoluto para evitar problemas em diferentes sistemas operacionais
"""
PROGRAM_DIR = Path(__file__).parents[2]
LEXICAL_ANALYZER_INPUT_DIR = PROGRAM_DIR / "src/data/input_lexical_analyzer"
SINTATICAL_ANALYZER_INPUT_DIR = PROGRAM_DIR / "src/data/input_sintatical_analyzer"
REGULAR_DEFINITIONS_INPUT_DIR = PROGRAM_DIR / "src/data/input_regular_definitions" 
FA_OUTPUT_DIR = PROGRAM_DIR / "src/data/output_af"
LEXICAL_ANALYZER_OUTPUT_DIR = PROGRAM_DIR / "src/data/output_lexical_analyzer"
AUTOMATA_DIAGRAM_DIR = PROGRAM_DIR / "src/data/output_automata_diagram"
SLR_TABLE_DIR = PROGRAM_DIR / "src/data/output_slr_table"
CANONICAL_ITEMS_DIAGRAM_DIR = PROGRAM_DIR / "src/data/output_canonical_items_diagram"

"""
TODO:
- corrigir ux: ocultar botão de análise sintática quando já estiver nela ou quando estiver desabilitada
- colocar "ERRO" da sintática de vermelho e accept em verde
- função de salvar tabela de parsing
- ajustar README e about
- ajustar comentários
"""