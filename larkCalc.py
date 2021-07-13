from lark import Lark, Transformer, v_args

grammar = '''
?start : sum

?sum : product
	 | sum "+" product			-> add
	 | sum "-" product			-> sub

?product : value
		 | product "*" value	-> mul
		 | product "/" value	-> div

?value : NUMBER					-> number
	   | "-" value				-> neg
	   | "(" sum ")"

%import common.NUMBER
%import common.WS_INLINE

%ignore WS_INLINE
'''

@v_args(inline=True)
class CalcTree(Transformer):
	from operator import add, sub, mul, truediv as div, neg
	number = float

parser = Lark(grammar, parser='lalr', transformer=CalcTree())
calc = parser.parse

while True:
	print(calc(input('> ')))
