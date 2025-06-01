# ![Lexterminator Logo](src/ui/resources/logo-lexterminator-resized.png)

# Lexterminator

**Lexterminator** é a primeira parte de um projeto desenvolvido para a disciplina **INE5421 - Linguagens Formais e Compiladores** na Universidade Federal de Santa Catarina (UFSC).  
Esta etapa consiste na implementação de um **analisador léxico**, utilizando expressões regulares como entrada e gerando um autômato finito determinístico (AFD) capaz de reconhecer e classificar tokens.

---

## 👥 Autores

- **Henrique M. Teodoro** (23100472)  
- **Jonatan F. Hartmann** (23104231)  
- **Rodrigo Schwartz** (23100471)

---

## 🎯 Objetivo

A aplicação recebe como entrada um **conjunto de definições regulares**. As expressões regulares são convertidas em **autômatos finitos**, que são posteriormente **unidos e determinizados** para formar um único AFD capaz de reconhecer os tokens definidos. Permite reconhecer e classificar palavras em um **arquivo de entrada com palavras a serem reconhecidas**.

---

## 📂 Organização do Projeto

```text
├── main.py                      # Início da aplicação (abre GUI)
├── Makefile                     # Comandos úteis: run, clean
├── requirements.txt             # Dependências via pip
└── src
    ├── control/                 # Conexão entre modelo e interface
    ├── data/
    │   ├── input_regular_definitions/      # Exemplos de entrada de definições regulares
    │   ├── input_lexical_analyzer/         # Exemplos de entrada de palavras a serem reconhecidas e classificadas
    │   ├── output_af/                      # Saída do AFD em texto
    │   ├── output_automata_diagram/        # Imagem do autômato (PNG)
    │   └── output_lexical_analyzer/        # Lista de tokens reconhecidos
    ├── model/                   # Implementações do Autômato, Analisador Léxico, Árvore, Expressões e Definições regulares.
    ├── ui/                      # Arquivos .ui (interface PyQt5) e recursos
    ├── utils/                   # Funções auxiliares
    └── view/                    # Views PyQt5
```

---

## 🧪 Entradas e Saídas

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

## 🖥️ Interface Gráfica

A interface foi construída usando **PyQt5** e permite:
- Carregar arquivos de entrada (definições regulares e palavras a serem reconhecidas).
- Visualizar a estrutura do AFD em diagrama e tabela.
- Acompanhar a análise léxica com destaque para os tokens reconhecidos no arquivo de entrada, em forma de tabela.

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
