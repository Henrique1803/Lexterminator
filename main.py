from src.af import AF

af1 = AF.from_file("input_af/af_a_par.txt")  # L = número de a's par
af2 = AF.from_file("input_af/af_b_mod3.txt") # L = número de b's múltiplo de 3

af_union = AF.union(af1, af2) # união dos dois
af_union.print_transition_table()
 
print("------------")
af = af_union.determinize()
af.print_transition_table()
af.to_file("output_af/af_output.txt")
print("------------")

entrada = "abbb"
reconhecido, estados_finais = af.run(entrada)

if reconhecido:
    print(f"A entrada '{entrada}' foi aceita. Estados finais: {estados_finais}")
else:
    print(f"A entrada '{entrada}' não foi aceita.")

