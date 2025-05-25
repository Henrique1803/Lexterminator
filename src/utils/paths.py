from pathlib import Path

PROGRAM_DIR = Path(__file__).parents[2]
LEXICAL_ANALYZER_INPUT_DIR = PROGRAM_DIR / "src/data/input_lexical_analyzer"
REGULAR_DEFINITIONS_INPUT_DIR = PROGRAM_DIR / "src/data/input_regular_definitions" 
FA_OUTPUT_DIR = PROGRAM_DIR / "src/data/output_af"
LEXICAL_ANALYZER_OUTPUT_DIR = PROGRAM_DIR / "src/data/output_lexical_analyzer"
AUTOMATA_DIAGRAM_DIR = PROGRAM_DIR / "src/data/output_automata_diagram"