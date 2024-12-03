import json
import tkinter as tk
from tkinter import messagebox

# Definindo uma gramática simples de exemplo para a linguagem C
class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def current_token(self):
        """Retorna o token atual"""
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None

    def avancar(self):
        """Avança para o próximo token"""
        self.posicao += 1
        if self.posicao >= len(self.tokens):
            return None
        return self.tokens[self.posicao]

    def match(self, lexema):
        """Compara o lexema atual com o esperado e avança se forem iguais"""
        token = self.current_token()
        if token and token['Lexema'] == lexema:
            self.avancar()
            return True
        return False

    def parse(self):
        """Inicia a análise sintática"""
        if not self.programa():
            return False
        return True

    def programa(self):
        """S -> 'int' 'main' '(' ')' '{' Declarações Corpo '}'"""
        if self.match("int"):
            if self.match("main"):
                if self.match("("):
                    if self.match(")"):
                        if self.match("{"):
                            if self.declaracoes():
                                if self.corpo():
                                    # Verifica se o próximo token é None, e se for, retorna o erro de fechamento
                                    if self.current_token() is None:
                                        self.error("Esperado '}', mas encontrou: fim de entrada")
                                        return False
                                    if self.match("}"):
                                        return True
                                    else:
                                        return False
                                else:
                                    self.error("Esperado corpo de instruções após declarações, mas encontrou: " + (self.current_token() or {}).get('Lexema', 'fim de entrada'))
                                    return False
                            else:
                                self.error("Esperado declarações após '{', mas encontrou: " + (self.current_token() or {}).get('Lexema', 'fim de entrada'))
                                return False
                        else:
                            self.error("Esperado '{', mas encontrou: " + (self.current_token() or {}).get('Lexema', 'fim de entrada'))
                            return False
                    else:
                        self.error("Esperado ')', mas encontrou: " + (self.current_token() or {}).get('Lexema', 'fim de entrada'))
                        return False
                else:
                    self.error("Esperado '(', mas encontrou: " + (self.current_token() or {}).get('Lexema', 'fim de entrada'))
                    return False
            else:
                self.error("Esperado 'main', mas encontrou: " + (self.current_token() or {}).get('Lexema', 'fim de entrada'))
                return False
        else:
            self.error("Esperado 'int', mas encontrou: " + (self.current_token() or {}).get('Lexema', 'fim de entrada'))
            return False

    def declaracoes(self):
        """Declarações -> Declaração | Declarações Declaração"""
        if self.declaracao():
            if self.declaracoes():
                return True
            return True  # Caso base
        return False

    def declaracao(self):
        if self.match("int") or self.match("bool") or self.match("float") or self.match("string") or self.match("double"):
            if self.identificador():
                while self.match(","):  # Suporte para múltiplos identificadores
                    if not self.identificador():
                        self.error("Esperado identificador após ','.")
                        return False
                if self.match("="):
                    if self.expressao():
                        if not self.match(";"):
                            self.error("Esperado ';' após a expressão de atribuição.")
                            return False
                        return True
                    else:
                        self.error("Esperado expressão após '='.")
                        return False
                elif self.match(";"):
                    return True
                else:
                    self.error("Esperado '=' ou ';' após o identificador.")
                    return False
            else:
                self.error("Esperado identificador após o tipo.")
                return False
        return False

    def expressao(self):
        """Expressao -> Identificador | Literal"""
        token = self.current_token()
        if token and (token['Token'] in ["Identificador", "Literal", "Literal: true", "Literal: false"]):
            self.avancar()
            return True
        return False

    def identificadores(self):
        """Identificadores -> Identificador | Identificador ',' Identificadores"""
        if self.identificador():
            while self.match(","):  # Permite múltiplos identificadores separados por vírgulas
                if not self.identificador():
                    self.error("Esperado identificador após ',' na lista de identificadores.")
                    return False
            return True
        return False

    def identificador(self):
        """Identificador -> Identificador (verifica se o token é um identificador)"""
        token = self.current_token()
        if token and token['Token'] == "Identificador":
            self.avancar()
            return True
        return False

    def corpo(self):
        """Corpo -> Instrução | Corpo Instrução | Declaração | Corpo Declaração"""
        # Tentando analisar uma instrução
        if self.instrucao():
            # Se uma instrução for encontrada, tenta continuar com o corpo
            if self.match("return"):  # Caso o 'return' seja encontrado, esperamos o ponto e vírgula após
                if self.match(";"):  # Verifica o ponto e vírgula após o 'return'
                    return True
                else:
                    self.error("Esperado ';' após o 'return'.")
                    return False

            # Se uma instrução foi encontrada, verificamos se existe mais instruções no corpo
            if self.corpo():
                return True
            return True  # Caso base, quando não há mais instruções

        # Se não encontrou uma instrução, tenta uma declaração
        elif self.declaracao():
            # Se uma declaração for encontrada, tenta continuar com o corpo
            if self.corpo():
                return True
            return True  # Caso base, quando não há mais declarações

        return False  # Caso base, quando não encontrar uma instrução ou declaração válida

    def instrucao(self):
        """Instrução -> 'printf' | 'scanf' | Atribuição | return | if"""
        token_atual = self.current_token()  # Captura o token atual antes de tentar fazer match

        if self.match("if"):
            if self.match("("):  # Espera o parêntese de abertura do 'if'
                if self.expressao():  # Espera a expressão dentro dos parênteses
                    if self.match(")"):  # Espera o parêntese de fechamento
                        if self.match("{"):  # Espera o início do bloco de código
                            if self.corpo():  # Espera o corpo da instrução 'if'
                                if self.match("}"):  # Espera o fechamento do bloco
                                    return True
                                else:
                                    self.error("Esperado '}' após o corpo do 'if'.")
                                    return False
                            else:
                                self.error("Esperado corpo de instruções após o 'if'.")
                                return False
                        else:
                            self.error("Esperado '{' após o 'if'.")
                            return False
                    else:
                        self.error("Esperado ')' após a expressão do 'if'.")
                        return False
                else:
                    self.error("Esperado expressão após '('.")
                    return False
            else:
                self.error("Esperado '(' após 'if'.")
                return False

        if self.match("return"):
            if self.expressao():  # Verifica se há uma expressão após 'return'
                pass  # Aceita a expressão opcional
            if self.match(";"):  # Ponto e vírgula obrigatório
                return True
            else:
                self.error("Esperado ';' após o 'return'.")
                return False

        if self.match("printf"):
            if self.match("("):  # Verifica o parêntese de abertura
                token = self.current_token()
            
                if token and token['Token'] == "String":  # Verifica se o próximo token é uma string
                    self.avancar()  # Avança para o próximo token após a string

                    # Verifique se há parâmetros adicionais após a string (se houver, pode haver vírgulas)
                    while self.match(","):
                        token = self.current_token()
                        if token and token['Token'] == "Identificador":
                            self.avancar()
                        else:
                            self.error(f"Esperado identificador após vírgula, encontrado: {token['Lexema']}")
                            return False

                    # Verifique o fechamento do parêntese
                    if self.match(")"):
                        # Verifique o ponto e vírgula
                        if self.match(";"):
                            return True
                        else:
                            self.error("Esperado ';' após a expressão printf.")
                            return False
                    else:
                        self.error("Esperado ')' após os parâmetros de printf.")
                        return False
                else:
                    self.error(f"Esperado uma string após '('. Encontrado: {token['Lexema']}.")
                    return False
            else:
                self.error("Esperado '(' após 'printf'.")
                return False

        elif self.match("scanf"):
            if self.match("("):  # Verifica o parêntese de abertura
                token = self.current_token()

                if token and token['Token'] == "String":  # Verifica se o próximo token é uma string
                    self.avancar()  # Avança para o próximo token após a string

                    # Verifique se há parâmetros adicionais após a string (se houver, pode haver vírgulas)
                    while self.match(","):
                        if self.match("&"):  # Verifica se o próximo token é '&'
                            if self.identificador():  # Espera um identificador
                                pass
                            else:
                                self.error("Esperado identificador após '&'.")
                                return False
                        else:
                            self.error("Esperado '&' antes do identificador em scanf.")
                            return False

                    # Verifique o fechamento do parêntese
                    if self.match(")"):
                        # Verifique o ponto e vírgula
                        if self.match(";"):
                            return True
                        else:
                            self.error("Esperado ';' após a expressão scanf.")
                            return False
                    else:
                        self.error("Esperado ')' após os parâmetros de scanf.")
                        return False
            else:
                self.error("Esperado '(' após 'scanf'.")
                return False

        elif self.identificador():
            if self.match("="):
                if self.identificador():  # Agora esperamos outro identificador, como num1 ou num2
                    if self.match("+"):  # Se for uma operação de adição
                        if self.identificador():  # Espera outro identificador
                            if self.match(";"):  # E o ponto e vírgula no final
                                return True
                            else:
                                self.error("Esperado ';' após a expressão.")
                                return False
                        else:
                            self.error("Esperado um identificador após '+'")
                            return False
                    else:
                        self.error("Esperado um operador de adição '+' ou outro operador.")
                        return False
                else:
                    self.error("Esperado um identificador à direita do '='.")
                    return False
            else:
                self.error("Esperado '=' para atribuição.")
                return False

        return False

    def error(self, mensagem):
        """Exibe uma mensagem de erro detalhada com a linha, coluna e causa do erro"""
        token = self.current_token()
        if token:
            print(f"Erro na linha {token['Linha']}, coluna {token['Coluna']}: {mensagem}")
        else:
            print(f"Erro na análise sintática: {mensagem}")

# Função para carregar os tokens de um arquivo JSON
def carregar_tokens(tabela_simbolos_1):
    with open(tabela_simbolos_1, 'r') as arquivo:
        return json.load(arquivo)

# Função para exibir a janela de sucesso ou erro com estilo melhorado
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

# Função principal para rodar o analisador
def main():
    tokens = carregar_tokens("tabela_simbolos_1.json")

    analisador = AnalisadorSintatico(tokens)

    if analisador.parse():
        exibir_mensagem("Sucesso", "Análise sintática bem-sucedida!", sucesso=True)
    else:
        exibir_mensagem("Erro", "Erro na análise sintática.", sucesso=False)

if __name__ == "__main__":
    main()