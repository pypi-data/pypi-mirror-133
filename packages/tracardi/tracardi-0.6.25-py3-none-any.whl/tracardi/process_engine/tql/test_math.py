from tracardi.process_engine.tql.equation import MathEquation
from tracardi_dot_notation.dot_accessor import DotAccessor

dot = DotAccessor(payload={"id": "100.09"})
equation = MathEquation(dot)
x = equation.evaluate(['p =1 ', '-p'])
print(x)
print(dot.payload)
print(equation.get_variables())
