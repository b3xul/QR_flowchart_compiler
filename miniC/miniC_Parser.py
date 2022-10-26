from miniC_Lexer import *
from ply import yacc


class MyParser:

    # CONSTRUCTOR
    def __init__(self, myLexer):
        print("Parser called")
        self.parser = yacc.yacc(module=self)
        self.lexer = myLexer
        self.label = 0
        self.lineno = 1

    # DESTRUCTOR
    def __del__(self):
        print('Parser destructor called.')

    tokens = MyLexer.tokens

    # Ensure our parser understands the correct order of operations.
    # The precedence variable is a special Ply variable.

    precedence = (

        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'NOT'),
        ('left', 'MIN', 'MAJ', 'MIN_EQ', 'EQ_MIN', 'MAJ_EQ', 'EQ_MAJ', 'EQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'STAR', 'DIV'),
        ('left', 'UMINUS'),

    )

    def genLabel(self):
        self.label = self.label + 1
        return self.label

    # GRAMMAR START

    def p_prog(self, p):
        '''
        prog : decl_list stmt_list
        '''

        print('\tEND')

    # DECLARATION

    def p_decl_list(self, p):
        '''
        decl_list : decl_list decl 
                    | 
        '''

    def p_decl(self, p):
        '''
        decl : type var_list S
        '''

    # error in declaration
    def p_decl_error(self, p):
        '''
        decl : type error S
        '''
        print("Error in declaration ( row:",
            p[2].lineno, ", column:", self.lexer.find_column(p[2].lexer.lexdata, p[2]), ")")

    def p_type(self, p):
        '''
        type : INT_TYPE 
                | DOUBLE_TYPE
        '''

        if (p[1] == 'int'):
            p[0] = 'INT'
        elif (p[1] == 'double'):
            p[0] = 'DOUBLE'

    def p_m_copy(self, p):
        '''
        m_copy : empty
        '''

        # passing inherited TYPE - attribute for variable list
        p[0] = p[-2]

    def p_var_list(self, p):
        '''
        var_list : var 
                    | var_list CM m_copy var
        '''

        # equivalent to RESULT = parser.stack(-2)
        if (len(p) == 5):
            p[0] = p[-1]
        else:
            p[0] = p[1]  # passing inherited TYPE ATTRIBUTE for variable list

    def p_var(self, p):
        '''
        var : ID array
        '''

        p[0] = p[-1]  # inheriting TYPE ATTRIBUTE for variable list
        print(p[-1], p[1], p[2])

    def p_array(self, p):
        '''
        array : empty
                | array SO INT SC
        '''

        if (len(p) == 2):
            p[0] = ""  # empty string
        elif (len(p) == 5):
            p[0] = p[1] + "[" + p[3] + "]"

    # INSTRUCTIONS

    def p_stmt_list(self, p):
        '''
        stmt_list : stmt_list stmt 
                    | stmt 
        '''

    # error in statement
    def p_stmt_list_error(self, p):
        '''
        stmt_list : error stmt 
        '''
        print("Error in statement ( row:",
            p[1].lineno, ", column:", self.lexer.find_column(p[1].lexer.lexdata, p[1]), ")")

    def p_stmt(self, p):
        '''
        stmt : if 
                | while 
                | assignment 
                | print 
                | BO stmt_list BC
        '''

    # Project instruction
    def p_assignment(self, p):
        '''
        assignment : id S 
                        | id EQ exp S 
        '''

        if (len(p) == 3):
            print("\t", p[1])

        elif (len(p) == 5):
            print("\tEVAL ", p[3], "\n\tASS ", p[1])

    # error in statement
    def p_stmt_error(self, p):
        '''
        stmt :  BO stmt_list error BC 
                | BO error BC 
                | error S 
        '''
        if (len(p) == 5):
            print("Missing ; before } at ( row:",
                p[3].lineno, ", column:", self.lexer.find_column(p[3].lexer.lexdata, p[3]), ")")

        elif (len(p) == 4):
            print("Missing ; before } at ( row:",
                p[1].lineno, ", column:", self.lexer.find_column(p[2].lexer.lexdata, p[2]), ")")

        else:
            print("Error in statement ( row:",
                p[2].lineno, ", column:", self.lexer.find_column(p[1].lexer.lexdata, p[1]), ")")

    # error in assignment
    def p_assignment_error(self, p):
        '''
        assignment : id EQ error S 
                        | error EQ exp S 
        '''
        # p[1] == None ---> error

        print(p[1], p[2], p[3], p[4])
        if (p[3] != None and p[1] == None):
            if (p[1] == None):
                print("Error in assignment ( row:",
                    p[3].lineno, ", column:", self.lexer.find_column(p[3].lexer.lexdata, p[3]), ")")
            else:
                print("Error in assignment ( row:",
                    p[1].lineno, ", column:", self.lexer.find_column(p[1].lexer.lexdata, p[1]), ")")

        elif (p[3] == None and p[1] != None):
            if (p[3] == None):
                print("Error in expression ( row:",
                    p[1].lineno, ", column:", self.lexer.find_column(p[1].lexer.lexdata, p[1]), ")")
            else:
                print("Error in expression ( row:",
                    p[3].lineno, ", column:", self.lexer.find_column(p[3].lexer.lexdata, p[3]), ")")

            # print("Error in expression ( row:", p[2].lineno, ", column:", self.lexer.find_column(p[
            # 2].lexer.lexdata, p[2]),")")

    # Print instruction
    def p_print(self, p):
        '''
        print : PRINT id S
        '''

        print("\tPRINT ", p[2])

    # error in print instruction
    def p_print_error(self, p):
        '''
        print : PRINT error S
        '''

        print("Error in print instruction ( row:",
            p[2].lineno, ", column:", self.lexer.find_column(p[2].lexer.lexdata, p[2]), ")")

    # If instruction
    def p_if(self, p):
        '''
        if  :  IF if_condition nt0_if stmt
                | IF if_condition nt0_if stmt ELSE nt1_if stmt 
                | IF if_condition nt0_if stmt error nt1_if stmt
        '''
        if (len(p) == 8):
            if (p[5] == 'else'):
                print("L", p[3], ":")
            else:
                print("Error, else expected in if instruction ( row:",
                    p[5].lineno, ", column:", self.lexer.find_column(p[5].lexer.lexdata, p[5]), ")")

        else:
            print("L", p[3], ":")

    def p_if_condition(self, p):
        '''
        if_condition : RO exp RC
        '''

        p[0] = p[2]

    def p_if_condition_error(self, p):
        '''
        if_condition : RO error RC
                        | error exp RC
                        | RO exp error
        '''
        if (p[3] == ')'):
            if (p[1] == '('):
                print("Error in if condition ( row:",
                    p[2].lineno, ", column:", self.lexer.find_column(p[2].lexer.lexdata, p[2]), ")")

            else:
                print("Error ( expected in if instruction ( row:",
                    p[1].lineno, ", column:", self.lexer.find_column(p[1].lexer.lexdata, p[1]), ")")

        else:
            print("Error ) expected in if instruction ( row:",
                p[3].lineno, ", column:", self.lexer.find_column(p[3].lexer.lexdata, p[3]), ")")


    def p_nt0_if(self, p):
        '''
        nt0_if : empty
        '''

        p[0] = self.genLabel()
        print("\tEVAL ", p[-1], "\t\t/* if (line ", self.lineno, ") */\n\tGOTOF L", p[0])

    def p_nt1_if(self, p):
        '''
        nt1_if : empty
        '''

        p[0] = self.genLabel()
        print("\tGOTO L", p[0])
        print("L", p[0], ":", end="")

    # While instruction
    def p_while(self, p):
        '''
        while : WHILE while_condition nt0_while stmt
        '''

        l = p[3]
        print("\tGOTO L", l[0])
        print("L", l[1], ":", end="")


    def p_while_condition(self, p):
        '''
        while_condition : RO exp RC
        '''
        p[0] = p[2]

    def p_while_condition_error(self, p):
        '''
        while_condition : RO error RC
                            | error exp RC
                            | RO exp error
        '''

        if (p[3] == ')'):
            if (p[1] == '('):
                print("Error in while condition ( row:",
                    p[2].lineno, ", column:", self.lexer.find_column(p[2].lexer.lexdata, p[2]), ")")

            else:
                print("Error ( expected in while instruction ( row:",
                    p[1].lineno, ", column:", self.lexer.find_column(p[1].lexer.lexdata, p[1]), ")")

        else:
            print("Error ) expected in while instruction ( row:",
                p[3].lineno, ", column:", self.lexer.find_column(p[3].lexer.lexdata, p[3]), ")")

    def p_nt0_while(self, p):
        '''
        nt0_while : empty
        '''

        x = [self.genLabel(), self.genLabel()]
        p[0] = x
        print("L", x[0], ":\tEVAL ", p[-1], "\t\t/* while (line ", self.lineno, ") */\n\tGOTOF L", x[1])


    # Expressions
    def p_exp(self, p):
        '''
        exp :   exp AND exp
                | exp OR exp
                | NOT exp
                | exp EQ EQ exp
                | exp MIN exp
                | exp MAJ exp
                | exp MAJ_EQ exp
                | exp EQ_MAJ exp
                | exp MIN_EQ exp
                | exp EQ_MIN exp
                | exp PLUS exp
                | exp MINUS exp
                | exp STAR exp
                | exp DIV exp
                | RO exp RC
                | id
                | INT
                | DOUBLE
                | MINUS INT %prec UMINUS
                | MINUS DOUBLE %prec UMINUS
        '''

        if len(p) == 2:
            p[0] = p[1]

        elif (len(p) == 3):
            if (p[1] == '!'):
                p[0] = p[2] + " ! "

            elif p[1] == '-':
                p[0] = "-" + p[2]

        elif (len(p) == 4):
            if (p[2] == '&'):
                p[0] = p[1] + " " + p[3] + " & "
            elif (p[2] == '|'):
                p[0] = p[1] + " " + p[3] + " | "
            elif (p[2] == '<'):
                p[0] = p[1] + " " + p[3] + " < "
            elif (p[2] == '>'):
                p[0] = p[1] + " " + p[3] + " > "
            elif (p[2] == '<='):
                p[0] = p[1] + " " + p[3] + " <= "
            elif (p[2] == '=<'):
                p[0] = p[1] + " " + p[3] + " <= "
            elif (p[2] == '>='):
                p[0] = p[1] + " " + p[3] + " >= "
            elif (p[2] == '=>'):
                p[0] = p[1] + " " + p[3] + " >= "
            elif (p[2] == '+'):
                p[0] = p[1] + " " + p[3] + " + "
            elif (p[2] == '-'):
                p[0] = p[1] + " " + p[3] + " - "
            elif (p[2] == '*'):
                p[0] = p[1] + " " + p[3] + " * "
            elif (p[2] == '/'):
                p[0] = p[1] + " " + p[3] + " / "
            elif (p[1] == '('):
                p[0] = p[2]

    def p_exp_error(self, p):
        '''
        exp : RO error RC
        '''

        print("Error in expression")

    def p_id(self, p):
        '''
        id : ID
            | ID SO INT SC
            | ID SO ID SC
        '''

        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 5:
            p[0] = p[1] + "[" + p[3] + "]"

    def p_error(self, p):
        '''
        error: 
        '''

    def p_empty(self, p):
        '''
        empty :
        '''
