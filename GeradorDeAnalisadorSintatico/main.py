from src.model.lr_parsing import LRParsing
from src.model.slr_table import SLRTable
from src.model.grammar import Grammar
from src.utils.closure_and_canonnical_collection import *


if __name__ == "__main__":
    
    grammar = Grammar("src/input/grammar_slides.txt")
    
    extended_grammar = extend_grammar(grammar)
    
    collection, transitions = canonical_collection(extended_grammar)
    
    # útil para ordenar as produções com base na ordem de aparição no arquivo
    prod_order = get_production_order(extended_grammar)
    
    slr_table = SLRTable(extended_grammar, collection, transitions, prod_order)

    entrada_text = "id * id + id"
    entrada = list(entrada_text.split())
    
    parsing = LRParsing(extended_grammar, slr_table)

    a, b = parsing.parse(entrada)

    print_canonical_collection(collection, extended_grammar)
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    slr_table.print_table()
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("Entrada: ", entrada_text)
    print("Passou? ",b)
    print(a)