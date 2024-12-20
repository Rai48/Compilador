import re
import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox

def exibir_mensagem(titulo, mensagem, sucesso=True):
    root = tk.Tk()
    root.title(titulo)
    
    # Define o tamanho da janela
    largura = 400
    altura = 200
    tela_largura = root.winfo_screenwidth()
    tela_altura = root.winfo_screenheight()

    # Calcula a posição para centralizar a janela
    pos_x = (tela_largura // 2) - (largura // 2)
    pos_y = (tela_altura // 2) - (altura // 2)

    # Define a geometria da janela e a centraliza
    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    
    # Cria um fundo com cor diferente para sucesso ou erro
    if sucesso:
        root.config(bg="#D4EDDA")  # Cor de fundo verde claro para sucesso
    else:
        root.config(bg="#F8D7DA")  # Cor de fundo vermelho claro para erro
    
    # Cria um frame centralizado
    frame = tk.Frame(root, bg=root.cget("bg"))
    frame.pack(expand=True)

    # Define o título e a mensagem com fonte personalizada
    titulo_label = tk.Label(frame, text=titulo, font=("Arial", 16, "bold"), bg=root.cget("bg"))
    titulo_label.pack(pady=10)
    
    mensagem_label = tk.Label(frame, text=mensagem, font=("Arial", 12), bg=root.cget("bg"))
    mensagem_label.pack(pady=10)
    
    # Botão para fechar a janela
    botao = tk.Button(frame, text="Fechar", command=root.quit, font=("Arial", 12), bg="#5A6268", fg="white")
    botao.pack(pady=10)

    # Exibe a janela
    root.mainloop()


def exibir_mensagem_sucesso():
    exibir_mensagem("Sucesso", "Tabela de símbolos gerada com sucesso!", sucesso=True)


class AnalisadorLexico:
    operators = {'=' : 'Simbolo_Atribuicao',
                '==' : 'Simbolo_Comparacao',
                '+' : 'Simbolo_Op_Adicao',
                '-' : 'Simbolo_Op_Subtracao',
                '/' : 'Simbolo_Op_Divisao',
                '*' : 'Simbolo_Op_Multiplicacao',
                '<' : 'Simbolo_Op_Menorque',
                '>' : 'Simbolo_Op_Maiorque',
                '%' : 'Simbolo_Op_Modulo' }
    operators_key = operators.keys()

    logical_operators = {'&' : 'Simbolo_Op_E',
                        '|' : 'Simbolo_Op_OU',
                        '~' : 'Simbolo_Op_Negacao',
                        '!' : 'Simbolo_Negacao' }
    logical_operators_key = logical_operators.keys()

    symbols = {
        '_' : 'Simbolo_Underscore',
        '{' : 'Simbolo_Chave_Abertura',
        '}' : 'Simbolo_Chave_Fecha',
        '[' : 'Simbolo_Colchete_Abertura',
        ']' : 'Simbolo_Colchete_Fecha',
        '(' : 'Simbolo_Parenteses_Abertura',
        ')' : 'Simbolo_Parenteses_Fecha',
        '?' : 'Simbolo_Interrogacao',
        '^' : 'Simbolo_Circunflexo',
    }
    symbols_key = symbols.keys()


    punctuation_symbol = { ':' : 'Dois-Pontos',
                            ';' : 'Ponto-Virgula', 
                            '.' : 'Ponto' , 
                            ',' : 'Virgula' }
    punctuation_symbol_key = punctuation_symbol.keys()

    literal_symbol = { 'true' : 'true',
                            'false' : 'false' }
    literal_symbol_key = literal_symbol.keys()


    keywords = {
        'auto': 'auto',
        'break': 'break',
        'bool': 'bool',
        'case': 'case',
        'char': 'char',
        'const': 'const',
        'continue': 'continue',
        'default': 'default',
        'do': 'do',
        'double': 'double',
        'else': 'else',
        'enum': 'enum',
        'extern': 'extern',
        'float': 'float',
        'for': 'for',
        'goto': 'goto',
        'if': 'if',
        'int': 'int',
        'long': 'long',
        'register': 'register',
        'return': 'return',
        'short': 'short',
        'signed': 'signed',
        'sizeof': 'sizeof',
        'static': 'static',
        'struct': 'struct',
        'switch': 'switch',
        'typedef': 'typedef',
        'union': 'union',
        'unsigned': 'unsigned',
        'void': 'void',
        'volatile': 'volatile',
        'while': 'while',
        'printf' : 'printf',
        'scanf' : 'scanf'
    }
    keywords_key = keywords.keys()

    identifier_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    number_pattern = re.compile(r'^[0-9]+$')
    string_pattern = re.compile(r'^\".*\"$|^\'.*\'$', re.UNICODE) 

    results = []

    with open("C.txt", encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):

            line = re.sub(r'//.*?(\n|$)', '\n', line)
            line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)

            line = re.sub(r'#include.*?\n', '', line)

            token_pattern = re.compile(r'(\".*?\"|\'.*?\'|[a-zA-Z_][a-zA-Z0-9_]*|==|=|\+|\-|\*|\/|<|>|%|&|\||~|!|{|}|[|]|\(|\)|\?|:|;|\.|,|\s+)')
            tokens = token_pattern.findall(line)

            column_number = 1
            for token in tokens:
                token = token.strip()
                if not token:
                    column_number += len(token)
                    continue

                result = {'Lexema': token, 'Token': None, 'Linha': line_number, 'Coluna': column_number}

                if token in operators_key:
                    result['Token'] = 'Identificador de Operador: ' + operators[token]
                elif token in literal_symbol_key:
                    result['Token'] = 'Literal: ' + literal_symbol[token]
                elif token in logical_operators_key:
                    result['Token'] = 'Operador Lógico: ' + logical_operators[token]
                elif token in keywords_key:
                    result['Token'] = 'Palavra-chave: ' + keywords[token]
                elif token in punctuation_symbol_key:
                    result['Token'] = 'Símbolo de Pontuação: ' + punctuation_symbol[token]
                elif token in symbols_key:
                    result['Token'] = 'Símbolo: ' + symbols[token]
                elif identifier_pattern.match(token):
                    result['Token'] = 'Identificador'
                elif number_pattern.match(token):
                    result['Token'] = 'Número'
                elif string_pattern.match(token):
                    result['Token'] = 'String'
                else:
                    result['Token'] = 'Token não faz parte do vocabulário (Erro)'

                results.append(result)
                column_number += len(token) + 1


    df = pd.DataFrame(results)


    base_filename = "tabela_simbolos"
    counter = 1
    filename = f"{base_filename}_{counter}.xlsx"

    json_filename = filename.replace(".xlsx", ".json")  # Gera o nome do arquivo JSON com o mesmo nome base
    df.to_json(json_filename, orient="records", force_ascii=False)  # Salvando como JSON sem lines=True
    print(f"Tabela de símbolos gerada com sucesso em JSON: {json_filename}")

    while os.path.exists(filename):
        counter += 1
        filename = f"{base_filename}_{counter}.xlsx"

    df.to_excel(filename, index=False)

    exibir_mensagem_sucesso()