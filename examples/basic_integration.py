#!/usr/bin/python3

from modularcalculator.modularcalculator import ModularCalculator

# Initialise calculator with a preset name
c = ModularCalculator('Advanced')

# Send an expression to the calculator, get a response object
response = c.calculate('3 ^ 2')

# Display the value of the first result in the response (there will be only one).
# Take a look at objects/api.py for other information in the response, such as
# result units, items parsed, time taken etc.
print(response.results[0].value)

# Empty calculator with features manually installed
c = ModularCalculator()
c.add_features(['numerical.basicarithmetic', 'numerical.decimalnumbers', 'structure.operators'])
response = c.calculate('2+3')
print(response.results[0].value)
