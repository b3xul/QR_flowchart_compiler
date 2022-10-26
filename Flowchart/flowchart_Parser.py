from flowchart_Lexer import *
from ply import yacc


class Node:
    def __init__(self, id_, type_, label):
        self.id = id_
        self.type_ = type_
        self.label = label
        if type_ == 'P' or type_ == 'T':
            self.next_node = None
        elif type_ == 'D':
            self.next_nodes = {}


class MyParser:
    # CONSTRUCTOR
    def __init__(self, myLexer, mode):
        # print("Parser called.")
        self.parser = yacc.yacc(module=self)
        self.lexer = myLexer
        self.label = 0
        self.lineno = 1

        self.mode = mode

        if self.mode == 'graph':
            self.shapes = {'D': 'diamond', 'P': 'box', 'T': 'oval'}
        elif self.mode == 'interactive':
            self.nodes = {}

    # DESTRUCTOR
    def __del__(self):
        # print('Parser destructor called.')
        pass

    tokens = MyLexer.tokens

    def navigate_flowchart(self, initial_node: Node):
        curr = initial_node

        while curr.type_ != 'T':
            if curr.type_ == 'P':
                # DEACTIVATE ALL PLUGINS EXCEPT X
                print(curr.label)
                curr = curr.next_node
            elif curr.type_ == 'D':
                options = list(curr.next_nodes.keys())
                while True:
                    # Build prompt like "Are there new Rick and Morty episodes?? [0:Yes!, 1:No..]"
                    prompt = f"{curr.label}? ["
                    for (i, label) in enumerate(options):
                        prompt += f"{i}:{label}"
                        if i != len(options) - 1:
                            prompt += ", "
                    prompt += "]\n"

                    selected_option = input(prompt)
                    if selected_option in options:
                        # Accept "Yes!" or "No.." as answer
                        # curr = curr.next_nodes[Yes!] = node3
                        curr = curr.next_nodes[selected_option]
                        break
                    elif int(selected_option) in range(len(options)):
                        # Accept "0" or "1" as answer
                        # curr = curr.next_nodes[list(curr.next_nodes.keys())[0]] = node3
                        curr = curr.next_nodes[options[int(selected_option)]]
                        break
                    else:
                        print("Invalid option")
        else:
            print(curr.label)

    # GRAMMAR START
    def p_prog(self, p):
        '''
        prog : node_list nl links_list
        '''
        # print('\tProgram recognized correctly!')
        if self.mode == 'graph':
            print("flowchart.render(view=True, format='png', outfile='Flowchart/flowchart.png', cleanup=True)")
            print("print('flowchart.png generated correctly!')")
        elif self.mode == 'interactive':
            # from Python 3.6 dict maintains insertion order. We expect the first defined node to be the first node
            # of the flowchart
            self.navigate_flowchart(next(iter(self.nodes.values())))

    def p_node_list(self, p):
        '''
        node_list : node_list node
                    | node
        '''
        # print(f"Recognized nodelist!")

    def p_node(self, p):
        '''
        node : INT type CL STRING nl
        '''
        # 1 D : ARE YOU USING THE LATEST VERSION OF THE PLUGIN X
        # print(f"Recognized node: {p[1]} {p[2]} {p[3]} {p[4]} {p[5]}")
        if self.mode == 'graph':
            # print(f"flowchart.node('1','ARE YOU USING THE LATEST VERSION OF THE PLUGIN X',shape='{self.shapes[D]}')")
            print(f"flowchart.node('{p[1]}','{p[4]}',shape='{self.shapes[p[2]]}')")
        elif self.mode == 'interactive':
            # Node def __init__(self, id_, type_, label):
            # self.nodes[1] = Node(1, D, ARE YOU USING THE LATEST VERSION OF THE PLUGIN X)
            self.nodes[p[1]] = Node(p[1], p[2], p[4])

    def p_type(self, p):
        '''
        type :  DECISION_TYPE
                | PROCESS_TYPE
                | TERMINAL_TYPE
        '''
        # type = "DECISION_TYPE" | "PROCESS_TYPE" | "TERMINAL_TYPE"
        p[0] = p[1]
        # print(f"type={p[1]}")

    def p_links_list(self, p):
        '''
        links_list : links_list links
                    | links
        '''
        # print("Recognized links list!")

    def p_links(self, p):
        '''
        links : links link nl
                |
        '''

    def p_link(self, p):
        '''
        link : link arrow INT
            | INT arrow INT
        '''
        # chain links by passing the latest INT encountered to link
        p[0] = p[3]
        # print(f"Recognized link: ", end=" ")
        # for x in range(1, len(p)):
        #     print(p[x], end=" ")
        # print()
        if self.mode == 'graph':
            # print(f"flowchart.edge('5','6','Yes')")
            print(f"flowchart.edge('{p[1]}','{p[3]}','{p[2]}')")
        elif self.mode == 'interactive':
            type_ = self.nodes[p[1]].type_
            if type_ == 'P' or type_ == 'T':
                # self.nodes[5].next_node = self.nodes[6]
                self.nodes[p[1]].next_node = self.nodes[p[3]]
            elif type_ == 'D':
                # self.nodes[5].next_nodes["YES"] = self.nodes[6]
                # dictionary like { "Yes" : node6, "No" : node3,... }
                self.nodes[p[1]].next_nodes[p[2]] = self.nodes[p[3]]
        # print(self.nodes[p[1]].next_nodes)

    def p_arrow(self, p):
        '''
        arrow : H STRING H
                | H
        '''
        p[0] = ''
        if len(p) == 4:
            # arrow = STRING
            p[0] = p[2]

    def p_error(self, p):
        '''
        error :
        '''
        print("Parser error")
