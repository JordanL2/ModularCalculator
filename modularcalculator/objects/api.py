#!/usr/bin/python3


def get_last_result(results):
    return [r for r in results if r.has_result()][-1]


class CalculatorResponse:

    def __init__(self):
        self.results = []
        self.items = []

    def add_result(self, result):
        self.results.append(result)

    def copy(self):
        response = CalculatorResponse()
        response.results = self.results.copy()
        response.items = self.items.copy()
        return response


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

    def set_state(self, state):
        self.state = state

    def has_result(self):
        return hasattr(self, 'value')

    def has_state(self):
        return hasattr(self, 'state')
