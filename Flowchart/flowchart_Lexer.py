from ply import lex


class MyLexer():

    # CONSTRUCTOR
    def __init__(self):
        # print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)

    # DESTRUCTOR
    def __del__(self):
        # print('Lexer destructor called.')
        pass

    def init_parser(self, myParser):
        self.parser = myParser

    reserved = {
        'D': 'DECISION_TYPE',
        'P': 'PROCESS_TYPE',
        'T': 'TERMINAL_TYPE'
    }

    # list of TOKENS
    tokens = [
                 'INT',
                 'CL',
                 'nl',
                 'H',
                 'STRING'
             ] + list(reserved.values())

    # Compute column.
    # input is the input text string
    # token is a token instance
    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    # tokens DEFINITION

    def t_STRING(self, t):
        r'([a-zA-Z ][a-zA-Z 0-9?!, %*+./]*)'
        t.type = self.reserved.get(t.value, 'STRING')  # Check for reserved words
        # print(f"string:{t}")
        return t

    def t_INT(self, t):
        r'([1-9][0-9]*|0)'
        # print(f"INT={t}")
        return t

    def t_CL(self, t):
        r':'
        return t

    def t_nl(self, t):
        r'(\$|\n)'
        return t

    def t_H(self, t):
        r'-'
        # print(t)
        return t

    def t_eof(self, t):
        # print("EOF reached")
        t.lexer.skip(1)

    def t_error(self, t):
        r'.'
        print("ERROR (Character not recognized): ", t.value)
        return t
