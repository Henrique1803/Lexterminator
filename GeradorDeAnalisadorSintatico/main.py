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

    entrada = list("id * id + id".split())
    
    parsing = LRParsing(extended_grammar, slr_table)

    a, b = parsing.parse(entrada)
    print("Passou? ",b)
    print(a)