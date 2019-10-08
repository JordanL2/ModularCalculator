#!/usr/bin/python3


class CalculatorResponse:

    def __init__(self):
        self.results = []
        self.items = []

    def add_result(self, expression, items):
        result = CalculatorResult(expression, items)
        self.results.append(result)
        return result


class CalculatorResult:

    def __init__(self, expression, items):
        self.expression = expression
        self.items = items
        self.timings = {}

    def set_answer(self, value, unit):
        self.value = value
        self.unit = unit

    def set_timing(self, stage, time):
        self.timings[stage] = time
