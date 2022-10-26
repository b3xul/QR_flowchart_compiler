from ply import lex


class MyLexer():


    # CONSTRUCTOR
    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)

    # DESTRUCTOR
    def __del__(self):
        print('Lexer destructor called.')

    def init_parser(self, myParser):
        self.parser = myParser

    # list of TOKENS
    tokens = [

        'nl',
        'ws',
        'RC', 'RO', 'BC', 'BO', 'SO', 'SC',
        'DIV', 'STAR', 'PLUS', 'MINUS',
        'MIN', 'MAJ', 'MIN_EQ', 'MAJ_EQ', 'EQ_MIN', 'EQ_MAJ', 'EQ',
        'OR', 'NOT', 'AND',
        'INT_TYPE', 'DOUBLE_TYPE',
        'IF', 'ELSE', 'WHILE', 'PRINT',
        'S', 'CM', 'ID',
        'INT', 'DOUBLE',

    ]

    # list of STATES -> used only the one to catch comments
    states = (
        ('COMMENT', 'exclusive'),
    )

    t_ws = r'([ \t])'

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        self.parser.lineno += len(t.value)
        t.lexer.lineno += len(t.value)
        pass

    # Compute column.
    # input is the input text string
    # token is a token instance
    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    # tokens DEFINITION
    def t_nl(self, t):
        r'(\s|\r)'
        pass

    def t_RO(self, t):
        r'\('
        return t

    def t_RC(self, t):
        r'\)'
        return t

    def t_BO(self, t):
        r'\{'
        return t

    def t_BC(self, t):
        r'\}'
        return t

    def t_SO(self, t):
        r'\['
        return t

    def t_SC(self, t):
        r'\]'
        return t

    def t_EQ(self, t):
        r'\='
        return t

    def t_PLUS(self, t):
        r'\+'
        return t

    def t_MINUS(self, t):
        r'\-'
        return t

    def t_MIN(self, t):
        r'\<'
        return t

    def t_MAJ(self, t):
        r'\>'
        return t

    def t_MIN_EQ(self, t):
        r'\<='
        return t

    def t_MAJ_EQ(self, t):
        r'\>='
        return t

    def t_EQ_MIN(self, t):
        r'\=<'
        return t

    def t_EQ_MAJ(self, t):
        r'\=>'
        return t

    def t_OR(self, t):
        r'\|'
        return t

    def t_NOT(self, t):
        r'\!'
        return t

    def t_AND(self, t):
        r'&'
        return t

    def t_INT_TYPE(self, t):
        r'int'
        return t

    def t_DOUBLE_TYPE(self, t):
        r'double'
        return t

    def t_PRINT(self, t):
        r'print'
        return t

    def t_IF(self, t):
        r'if'
        return t

    def t_WHILE(self, t):
        r'while'
        return t

    def t_ELSE(self, t):
        r'else'
        return t

    def t_S(self, t):
        r'\;'
        return t

    def t_CM(self, t):
        r'\,'
        return t

    def t_ID(self, t):
        r'([a-zA-Z_][a-zA-Z0-9_]*)'
        return t

    def t_DOUBLE(self, t):
        r'(([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+))(e|E(\+|\-)?[0-9]+)?'
        return t

    def t_INT(self, t):
        r'([1-9][0-9]*|0)'
        return t

    def t_eof(self, t):
        # print("EOF reached")
        t.lexer.skip(1)

    # COMMENT STATE

    def t_INITIAL_comm(self, t):
        r'\/\*'
        self.lexer.begin('COMMENT')

    def t_COMMENT_end(self, t):
        '\*\/'
        self.lexer.begin('INITIAL')

    def t_COMMENT_body(self, t):
        r'.'
        pass

    def t_COMMENT_nl(self, t):
        r'(\n|\r|\r\n)|\s|\t'
        pass

    def t_COMMENT_error(self, t):
        r'.'
        print("ERROR:", t.value)
        return t

    def t_STAR(self, t):
        r'\*'
        return t

    def t_DIV(self, t):
        r'\/'
        return t

    def t_error(self, t):
        r'.'
        print("ERROR (Character not recognized): ", t.value)
        return t
