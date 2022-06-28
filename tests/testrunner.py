#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *

import statistics
import unittest


TEST_STATS = {}


class CalculatorTestCase(unittest.TestCase):

    def generate_test(test):
        def do_test(self):
            expr = test['test']
            response = None

            if 'expected' in test:
                expected = test['expected']
                response = self.c.calculate(expr)
                last_result = [r for r in response.results if r.has_result()][-1]
                value = last_result.value
                unit = last_result.unit
                if type(value) == list:
                    new_value = []
                    for v in value:
                        if v.unit is None:
                            new_value.append(v.value)
                        else:
                            if v.value == Number(1):
                                new_value.append((v.value, v.unit.singular()))
                            else:
                                new_value.append((v.value, v.unit.plural()))
                    value = new_value
                elif 'cast' in test:
                    if test['cast'] == str and isinstance(value, Number):
                        value = value.to_string(self.c)
                    else:
                        value = test['cast'](value)
                if unit is None:
                    actual = value
                else:
                    if isinstance(value, Number) and value == Number(1):
                        actual = (value, unit.singular())
                    else:
                        actual = (value, unit.plural())
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
                if 'timings' not in TEST_STATS:
                    TEST_STATS['timings'] = {}
                testcase_name = type(self).__name__
                if testcase_name not in TEST_STATS['timings']:
                    TEST_STATS['timings'][testcase_name] = {}
                for result in response.results:
                    for stage in result.timings.keys():
                        if stage not in TEST_STATS['timings'][testcase_name]:
                            TEST_STATS['timings'][testcase_name][stage] = {}
                        TEST_STATS['timings'][testcase_name][stage][result.expression] = result.timings[stage]

        return do_test

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
