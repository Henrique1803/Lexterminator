from src.model.grammar import Grammar
from src.utils.closure_and_canonnical_collection import *

if __name__ == "__main__":
    
    # Carrega a gramática original
    original_grammar = Grammar("src/input/grammar_slides.txt")
    
    # Estende a gramática
    extended_grammar = extend_grammar(original_grammar)

    collection, transitions = canonical_collection(extended_grammar)
    print_canonical_collection(collection, extended_grammar)
    print(transitions)