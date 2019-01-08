#!/usr/bin/python3

from modularcalculator.modularcalculator import ModularCalculator

# Initialised with a preset name
c = ModularCalculator('Advanced')
response = c.calculate('3 ^ 2')
print(response.results[0].value)

# Empty calculator with features manually installed
c = ModularCalculator()
c.add_features(['numerical.basicarithmetic', 'numerical.decimalnumbers', 'structure.operators'])
c.setup()
response = c.calculate('2+3')
print(response.results[0].value)
