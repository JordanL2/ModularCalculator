#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *

import statistics
import unittest


TEST_STATS = {}

__import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999


class CalculatorTestCase(unittest.TestCase):

    def generate_test(test):
        def do_test(self):
            try:
                expr = test['test']
                response = None

                if 'expected' in test:
                    expected = test['expected']
                    response = self.c.calculate(expr)
                    last_result = [r for r in response.results if r.has_result()][-1]
                    actual = self.extract_answer(test, last_result)
                    self.assertEqual(type(actual), type(expected), msg=expr)
                    self.assertEqual(actual, expected, msg=expr)

                elif 'expected_exception' in test:
                    expected = test['expected_exception']
                    try:
                        response = self.c.calculate(expr)
                        with self.assertRaises(CalculatorException, msg=expr):
                            response = self.c.calculate(expr)
                    except CalculatorException as err:
                        if 'exception' in expected:
                            self.assertEqual(type(err), expected['exception'], expr)
                        if 'message' in expected:
                            self.assertEqual(err.message, expected['message'], expr)
                        if 'next' in expected:
                            self.assertEqual(err.next, expected['next'], expr)
                        if 'pos' in expected:
                            i = err.find_pos(expr)
                            self.assertEqual(i, expected['pos'], expr)
                        if 'items' in expected:
                            statements = self.hl.highlight_statements(err.statements)
                            items = [item[1] for items in statements for item in items if item[0] != 'default']
                            self.assertEqual(items, expected['items'], expr)

                if response is not None:
                    testcase_name = self.category()
                    if testcase_name is not None:
                        if 'timings' not in TEST_STATS:
                            TEST_STATS['timings'] = {}
                        if testcase_name not in TEST_STATS['timings']:
                            TEST_STATS['timings'][testcase_name] = {}
                        for result in response.results:
                            for stage in result.timings.keys():
                                if stage not in TEST_STATS['timings'][testcase_name]:
                                    TEST_STATS['timings'][testcase_name][stage] = {}
                                TEST_STATS['timings'][testcase_name][stage][result.expression] = result.timings[stage]
            except Exception as err:
                if isinstance(err, AssertionError):
                    raise err
                raise TestCaseException(test, err)

        return do_test

    def extract_answer(self, test, result):
        value = result.value
        unit = result.unit
        if type(value) == list:
            new_value = []
            for v in value:
                new_value.append(self.extract_answer(test, v))
            value = new_value
        elif 'cast' in test:
            if test['cast'] == str and isinstance(value, Number):
                value = value.to_string(self.c)
            else:
                value = test['cast'](value)
        if unit is None:
            return value
        else:
            if isinstance(value, Number) and value == Number(1):
                return (value, unit.singular())
            else:
                return (value, unit.plural())

    def category(self):
        raise Exception("Category has not been set")

    @classmethod
    def prepare_tests(test_class):
        for i, test in enumerate(test_class.tests):
            test_name = "test_{}".format(str(i))
            test_call = CalculatorTestCase.generate_test(test)
            setattr(test_class, test_name, test_call)


def execute_tests():
    unittest.main(exit=False)

    if 'timings' in TEST_STATS:
        for testcase in TEST_STATS['timings']:
            print()
            print(testcase)
            timings = TEST_STATS['timings'][testcase]
            total_avgtime = 0
            for stage in timings.keys():
                avgtime = statistics.mean(timings[stage].values())
                total_avgtime += avgtime
                avgtime = format_timing(statistics.mean(timings[stage].values()))
                maxtime = max(timings[stage].values())
                maxexpr = [expr for expr, t in timings[stage].items() if t == maxtime][0]
                maxtime = format_timing(maxtime)
                print("Stage: {0:9} Average Time: {1:12} Longest Time: {2:12} Longest Expression: {3}".format(stage, avgtime, maxtime, format_test(maxexpr)))
            print("Total:           Average Time: {0:12}".format(format_timing(total_avgtime)))

def format_timing(timing):
    return "{0} ms".format(round(timing * 1000, 3))

def format_test(test):
    return test.replace("\n", "\\n")


class TestCaseException(Exception):

    def __init__(self, test, err):
        self.test = test
