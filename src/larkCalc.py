from lark import Lark, Transformer, v_args
import math

grammar = '''
?start : sum
	   | NAME "=" sum			-> assign

?sum : product
	 | sum "+" product			-> add
	 | sum "-" product			-> sub

?product : power
		 | product "*" power	-> mul
		 | product "/" power	-> div
		 | product "%" power	-> mod
		 
?power : value
	   | value "^" power		-> pow

?value : NUMBER					-> number
	   | FUNC value				-> func_call
	   | NAME					-> var
	   | "-" value				-> neg
	   | "(" sum ")"

FUNC.2 : "sin" | "cos" | "tan" | "asin" | "acos" | "atan" | "round"
NAME : CNAME

%import common.NUMBER
%import common.WS_INLINE
%import common.CNAME

%ignore WS_INLINE
'''

@v_args(inline=True)
class CalcTree(Transformer):
	from operator import add, sub, mul, truediv as div, neg, pow, mod
	number = float
	
	def __init__(self):
		self.env = {'pi': math.pi}
		
		self.funcs = {
			'sin': lambda x: math.sin(x),
			'cos': lambda x: math.cos(x),
			'tan': lambda x: math.tan(x),
			'asin': lambda x: math.asin(x),
			'acos': lambda x: math.acos(x),
			'atan': lambda x: math.atan(x),
			'round': lambda x: round(x)
		}
	
	def func_call(self, func, value):
		return self.funcs[func](value)
		
	def assign(self, name, value):
		self.env[name] = value
		return value
		
	def var(self, name):
		try:
			return self.env[name]
		except KeyError:
			return 0

parser = Lark(grammar, parser='lalr', transformer=CalcTree())
calc = parser.parse

while True:
	print(calc(input('> ')))
