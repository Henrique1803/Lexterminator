# ![Lexterminator Logo](src/ui/resources/logo-lexterminator-resized.png)

# Lexterminator

**Lexterminator** é um projeto desenvolvido para a disciplina **INE5421 - Linguagens Formais e Compiladores** na Universidade Federal de Santa Catarina (UFSC).  
O projeto consiste na implementação de um **analisador léxico** e de um **analisador sintático SLR**, formando as primeiras etapas de um compilador. O analisador léxico utiliza expressões regulares como entrada para gerar um autômato finito determinístico (AFD) capaz de reconhecer e classificar os tokens da linguagem. Já o analisador sintático recebe como entrada uma gramática livre de contexto compatível com SLR(1) e constrói automaticamente a tabela de análise, sendo capaz de validar a estrutura sintática de programas escritos nessa linguagem.

---

## 👥 Autores

- **Henrique M. Teodoro** (23100472)  
- **Jonatan F. Hartmann** (23104231)  
- **Rodrigo Schwartz** (23100471)

---

## 🎯 Objetivo

A aplicação recebe como entrada um **conjunto de definições regulares**, utilizadas para descrever os tokens da linguagem. Essas expressões regulares são convertidas em **autômatos finitos não determinísticos (AFNs)**, que são então unidos e convertidos em um único **autômato finito determinístico (AFD)** capaz de reconhecer e classificar os tokens. O analisador léxico resultante é capaz de processar um arquivo de entrada contendo uma sequência de palavras, reconhecendo e classificando cada uma conforme os padrões definidos.

Em seguida, a **lista de tokens** reconhecidos pelo analisador léxico é utilizada como entrada para o analisador sintático, que opera com base em uma **gramática livre de contexto compatível com SLR(1)**. A partir dessa gramática, são construídas automaticamente as **tabelas de análise (ACTION e GOTO)**, permitindo ao analisador identificar se a sequência de tokens forma um programa válido segundo as regras sintáticas da linguagem. Durante esse processo, são identificadas estruturas como declarações, comandos e expressões, além de erros sintáticos, caso existam.

---

## 📂 Organização do Projeto

```text
├── main.py                      # Início da aplicação (abre GUI)
├── Makefile                     # Comandos úteis: run, clean
├── requirements.txt             # Dependências via pip
└── src
    ├── control/                 # Conexão entre modelo e interface
    ├── data/
    │   ├── input_compile/                  # Exemplos de entrada de programas a serem compilados
    │   ├── input_grammars/                 # Exemplos de gramáticas SLR(1) para o analisador sintático
    │   ├── input_regular_definitions/      # Exemplos de entrada de definições regulares para o analisador léxico
    │   ├── output_af/                      # Saída do AFD em texto
    │   ├── output_automata_diagram/        # Imagem do autômato (PNG)
    │   ├── output_canonical_items/         # Imagem do diagrama de itens canônicos construídos pelo analisador sintático
    │   ├── output_lexical_analyzer/        # Lista de tokens reconhecidos
    │   ├── output_parsing_table/           # Tabela de parsing feita sobre um programa compilado na análise sintática
    │   └── output_slr_table/               # Tabela SLR construído sobre a gramática de entrada
    ├── model/                   # Implementações relacionadas ao Analisador Léxico e ao Analisador Sintático
    ├── ui/                      # Arquivos .ui (interface PyQt5) e recursos
    ├── utils/                   # Funções auxiliares
    └── view/                    # Views PyQt5
```

---

## 🧪 Entradas e Saídas - Analisador Léxico

### 📥 Entrada:
1. **Definições regulares** (Exemplos: `src/data/input_regular_definitions/*.txt`):  
   - Define os **tokens válidos**.
   - Formato esperado:  
     ```txt
     letter: [A-za-z_]
     digit: [0-9]
     id: <letter> (<letter> | <digit>)*
     number: <digit>+
     ```

   - ⚠️ **Validações**:
     - Operadores suportados: `|`, `*`, `+`, `?`, concatenação implícita ou explícita.
     - `&` equivalente ao símbolo vazio.
     - Suporte a agrupamentos `()`.
     - Suporte a espaço `\s`.
     - Grupos e sequências lógicas no formato `[A-Za-z0-9_]` (para A, B .., Z, a, b, .. z, 0, ..., 9, _)
     - Aliases de definições anteriores no formato `<alias>`.
     - Uma definição por linha, no formato `definição: expressão` .
     - Nomes de tokens devem ser alfanuméricos e únicos.
     - **Caracteres de escape `\`**:
      - Qualquer símbolo imediatamente após o caractere `\` é considerado um símbolo literal, não um operador.
      - Para representar como literal, os seguintes símbolos devem ser escapados: `\\`, `\<`, `\>`, `\(`, `\)` `\[` `\]` `\*` `\|` `\.` `\?` `\+` `\&` `\-`, `\\s`

2. **Arquivo para análise léxica** (Exemplos: `src/data/input_lexical_analyzer/*.txt`):  
   - Contém o texto a ser reconhecido/tokenizado.
   - Considera uma palavra por linha.

---

### 📤 Saída:
1. **AFD Unificado** (Saída padrão: `src/data/output_af/af_output.txt`):  
   - Mostra o autômato determinizado resultante da união dos AFNs.
   - Formato:
      ```txt
      número de estados
      estado inicial
      estados finais separados por vírgula
      símbolos do alfabeto separados por vírgula
      transição na forma: <estado atual,símbolo,estado destino>
      transição na forma: <estado atual,símbolo,estado destino>
      ...
      ```

2. **Diagrama do Autômato** (Saída padrão: `src/data/output_automata_diagram/automata_diagram.png`):  
   - Imagem gerada automaticamente usando `graphviz`.

3. **Tokens Reconhecidos** (Saída padrão: `src/data/output_lexical_analyzer/tokens_output.txt`):  
   - Lista os tokens encontrados no arquivo de entrada ou aponta erros de reconhecimento.
   - Formato:
      ```txt
      <lexema,token> // em caso de ser reconhecido como um token válido
      <lexema,erro!> // em caso de não ser reconhecido como token válido
      ```

---

## 🧩 Entradas e Saídas - Analisador Sintático

### 📥 Entrada:

1. **Gramática Livre de Contexto SLR(1)** (Exemplos: `src/data/input_grammars/*.txt`):

   * Define as regras sintáticas da linguagem.
   * Formato esperado:

     ```txt
     <programa> ::= <declaracoes> <comandos> .
     <declaracoes> ::= <dcl_const> <dcl_var> <dcl_procs>
     <dcl_const> ::= const inteiro id = num_int ; <dcl_const>
     <dcl_const> ::= &
     ...
     ```
   * ⚠️ **Validações e restrições**:

     * Apenas **uma produção por linha**, no formato: `<não-terminal> ::= produção`.
     * `&` representa a **produção vazia** (ε).
     * O símbolo inicial deve ser o **primeiro não-terminal definido**.
     * O símbolo `::=` separa o lado esquerdo do lado direito da produção.
     * Terminais e não-terminais devem estar **separados por espaços**.
     * Terminais podem ser literais (ex: `+`, `:=`, `id`) ou palavras reservadas da linguagem.
     * Não-terminais devem estar entre **sinais de menor e maior** (ex: `<comando>`).
     * A gramática deve ser compatível com **SLR(1)** — não ambígua, sem conflitos shift-reduce ou reduce-reduce.
     * **Os terminais da gramática obrigatoriamente devem estar definidos como tokens nas definições regulares, sem exceção.**

2. **Lista de Tokens Reconhecidos** (Saída do léxico / Exemplo: `src/data/output_lexical_analyzer/tokens_output.txt`):

   * Contém a sequência de `<lexema,token>` gerada pelo analisador léxico.
   * Apenas os **nomes dos tokens** são usados pelo sintático (não os lexemas).

---

### 📤 Saída:

1. **Tabela SLR(1)** (Saída padrão: `src/data/output_slr_table/slr_table.csv`):
   * Contém as tabelas **ACTION** e **GOTO** utilizadas na análise SLR, no formato CSV.

2. **Items Canônicos** (Saída padrão: `src/data/output_canonical_items_diagram/canonical_items_diagram.png`):
   * Contém o diagrama dos items canônicos gerados na construção do analisador sintático

3. **Resultado da Análise Sintática** (Saída padrão: `src/data/output_parsing_table/parsing_table.csv`):

   * Contém o registro passo a passo da análise sintática do programa (shift, reduce, etc.), no formato CSV.
   * A tabela finaliza com a ação "ERRO", ou "ACCEPT".

---

## 🖥️ Interface Gráfica

A interface foi construída usando **PyQt5** e permite:
- Carregar arquivos de entrada (definições regulares e gramática SLR(1)).
- Carregar arquivos para compilação.
- Visualizar a estrutura do AFD em diagrama e tabela.
- Visualizar a tabela SLR e seus itens canônicos.
- Acompanhar a análise léxica com destaque para os tokens reconhecidos no arquivo de entrada, em forma de tabela.
- Acompanhar a análise sintática com destaque para os shift-reduces realizados, em forma de tabela.

---

## ▶️ Como Executar

### 🔧 Pré-requisitos:

1. Python 3.10+
2. [Graphviz](https://graphviz.org/download/) instalado no sistema (para gerar o autômato)
3. Instalar dependências Python:
   ```bash
   pip install -r requirements.txt
   ```

### 💻 Linux:
Utilize o `Makefile`:

```bash
make run     # Instala as dependências e executa a aplicação
make clean   # Remove arquivos temporários
```

---

## 📦 Dependências

Listadas em `requirements.txt`. Principais:

- `PyQt5`
- `prettytable`
- `graphviz` (binding Python e pacote do sistema)

---
