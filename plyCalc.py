from ply import lex, yacc
import math

env = {'pi':math.pi}

tokens = [
	'NUMBER',
	'STRING',
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'POW',
	'LPAREN',
	'RPAREN',
	'NAME',
	'ASSIGN'
]

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POW = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z]+'
t_ASSIGN = r'='

t_ignore = ' \t\n'

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t
	
def t_STRING(t):
	r'"[\S\s]*?"'
	t.value = t.value.rstrip('"').lstrip('"')
	return t

def t_error(t):
	print(f'TokenError: {t.value[0]}')
	t.lexer.skip(len(t.value))

lexer = lex.lex()

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
	('left', 'POW')
)

def p_expression(p):
	'''expression : expression POW expression
				  | expression TIMES expression
				  | expression DIVIDE expression
				  | expression PLUS expression
				  | expression MINUS expression'''
	try:
		if p[2] == '*':
			p[0] = p[1] * p[3]
		elif p[2] == '/':
			p[0] = p[1] / p[3]
		elif p[2] == '+':
			p[0] = p[1] + p[3]
		elif p[2] == '-':
			p[0] = p[1] - p[3]
		elif p[2] == '^':
			p[0] = p[1] ** p[3]
	except:
		print(f'ExpressionError: {p[2]}')
		
def p_paren(p):
	'expression : LPAREN expression RPAREN'
	p[0] = p[2]
		
def p_num_expression(p):
	'''expression : NUMBER
				  | STRING'''
	p[0] = p[1]
	
def p_assign(p):
	'expression : NAME ASSIGN expression'
	env[p[1]] = p[3]
	p[0] = p[3]
	
def p_var_expression(p):
	'expression : NAME'
	try:
		p[0] = env[p[1]]
	except KeyError:
		print(f'NameError: {p[1]!r} ')

def p_error(p):
	if p is None:
		return
	print(f'SyntaxError: {p.value}')
	
parser = yacc.yacc()
while True:
	print(parser.parse(input('> ')))
