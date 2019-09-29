#!/usr/bin/python3

from modularcalculator.modularcalculator import ModularCalculator
from modularcalculator.features.feature import Feature
from modularcalculator.objects.items import *

from decimal import *


class ExampleCustomFeature(Feature):

    def id():
        return 'example.hello'

    def category():
        return 'Numerical'

    def title():
        return 'Example Custom Feature'

    def desc():
        return 'Parses "hello" as the number 123'

    def dependencies():
        return ['numerical.decimalnumbers']

    @classmethod
    def install(cls, calculator):
        # This also requires adding the parser to its list of parsers, so it knows when to execute the parser.
        # In this case, it's important to insert it before the 'var' parser, which will just accept any string,
        # swallowing the 'hello' before our parser gets a chance to parse it. Take a look at the parser_map in
        # features/layout.py.
        calculator.parser_map.insert(calculator.parser_map.index('var'), 'hello')

        calculator.add_parser('hello', cls.parse_hello)
    
    def parse_hello(self, expr, i, items, flags):
        next = expr[i:]
        # If the next 5 characters are 'hello':
        if len(next) >= 5 and next.startswith('hello'):
        	# Returns one item, with original text = 'hello', value is the decimal number 123. Total parse length is 5. No return flags.
            return [LiteralItem('hello', Decimal('123'))], 5, None
        # Otherwise, nothing found by the parser this time
        return None, None, None
