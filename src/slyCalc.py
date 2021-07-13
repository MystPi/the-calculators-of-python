from sly import Lexer, Parser
import math

m_funcs = {
	'sin': lambda x: math.sin(x),
	'cos': lambda x: math.cos(x),
	'tan': lambda x: math.tan(x),
	'asin': lambda x: math.asin(x),
	'acos': lambda x: math.acos(x),
	'atan': lambda x: math.atan(x),
	'log': lambda x: math.log(x)
}

class CalcLexer(Lexer):
	tokens = {
		PLUS,
		MINUS,
		TIMES,
		DIVIDE,
		POW,
		MOD,
		NROOT,
		ROUND,
		
		LPAREN,
		RPAREN,
		
		INT,
		FLOAT,
		ID,
		EQ
	}
	
	PLUS = r'\+'
	MINUS = r'-'
	TIMES = r'\*'
	DIVIDE  = r'/'
	POW = r'\^'
	MOD = r'\%'
	NROOT = r'~'
	ROUND = r'\$'
	
	LPAREN = r'\('
	RPAREN = r'\)'
	
	ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
	EQ = r'='
	
	ignore = ' \n'
	
	# FLOAT must be before INT because of the regexp.
	
	@_(r'\d*\.\d+')
	def FLOAT(self, t):
		t.value = float(t.value)
		return t
	
	@_(r'\d+')
	def INT(self, t):
		t.value = int(t.value)
		return t
		
	def error(self, t):
		print(f'Illegal character: {t.value}')
		self.index += 1
		
class CalcParser(Parser):
	tokens = CalcLexer.tokens
	
	precedence = (
		('left', PLUS, MINUS),
		('left', TIMES, DIVIDE),
		('right', POW, MOD, NROOT)
	)
	
	def __init__(self):
		self.env = {'pi': math.pi}
		
	@_('ID EQ expr')
	def statement(self, p):
		self.env[p.ID] = p.expr
		
	@_('expr')
	def statement(self, p):
		print(p.expr)
		
	@_('expr PLUS expr')
	def expr(self, p):
		return p.expr0 + p.expr1
		
	@_('expr MINUS expr')
	def expr(self, p):
		return p.expr0 - p.expr1
		
	@_('expr TIMES expr')
	def expr(self, p):
		return p.expr0 * p.expr1
		
	@_('expr DIVIDE expr')
	def expr(self, p):
		try:
			return p.expr0 / p.expr1
		except ZeroDivisionError:
			print('Division by zero! Returning 0 instead.')
			return 0
			
	@_('expr POW expr')
	def expr(self, p):
		return p.expr0 ** p.expr1
		
	@_('expr MOD expr')
	def expr(self, p):
		return p.expr0 % p.expr1
		
	@_('expr NROOT expr')
	def expr(self, p):
		try:
			return p.expr0 ** (1 / p.expr1)
		except ZeroDivisionError:
			print('Roots must be > 0! Returning 0 instead.')
			return 0
			
	@_('ID LPAREN expr RPAREN')
	def expr(self, p):
		try:
			return m_funcs[p.ID](p.expr)
		except LookupError:
			print(f'Invalid function \'{p.ID}\'! Returning 0 instead.')
			return 0
			
	@_('ROUND LPAREN expr RPAREN')
	def expr(self, p):
		return round(p.expr)
		
	@_('LPAREN expr RPAREN')
	def expr(self, p):
		return p.expr
		
	@_('INT')
	def expr(self, p):
		return p.INT
		
	@_('FLOAT')
	def expr(self, p):
		return p.FLOAT
		
	@_('ID')
	def expr(self, p):
		try:
			return self.env[p.ID]
		except LookupError:
			print(f'No variable \'{p.ID}\' defined! Returning 0 instead.')
			return 0
			
	def error(self, p):
		if p is not None:
			print(f'Syntax error: {p.value}')
		
lexer  = CalcLexer()
parser = CalcParser()

while True:
	parser.parse(lexer.tokenize(input('> ')))
