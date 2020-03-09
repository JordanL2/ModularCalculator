#!/usr/bin/python3

from decimal import *
import statistics

class TestRunner:

    exception = None

    def __init__(self, exception=None):
        self.exception = exception
    
    def test(self, call, tests):
        failed = []
        timings = {}
        for num, test in enumerate(tests):
            question = test['test']
            expected = test['expected']
            actual = None
            try:
                response = call(question)
                #TODO this logic shouldn't be in here, pass in an answer resolution method
                last_result = [r for r in response.results if r.has_result()][-1]
                value = last_result.value
                unit = last_result.unit
                if type(value) == list:
                    new_value = []
                    for v in value:
                        if v.unit is None:
                            new_value.append(v.value)
                        else:
                            if v.value == Decimal('1'):
                                new_value.append((v.value, v.unit.singular()))
                            else:
                                new_value.append((v.value, v.unit.plural()))
                    value = new_value
                if unit is None:
                    actual = value
                else:
                    if value == Decimal('1'):
                        actual = (value, unit.singular())
                    else:
                        actual = (value, unit.plural())
                for result in response.results:
                    for stage in result.timings.keys():
                        if stage not in timings:
                            timings[stage] = {}
                        timings[stage][result.expression] = result.timings[stage]
            except self.exception as err:
                failed.append({ 'num': num, 'test': question, 'expected': expected, 'actual': 'Exception: ' + err.message })
                continue
            except Exception as err:
                print("Failed on test", num + 1, " - ", question)
                raise err
            if actual != expected:
                failed.append({ 'num': num, 'test': question, 'expected': expected, 'actual': actual })

        if len(failed) > 0:
            print("*** FAILED ***")
            for test in failed:
                print()
                print("        # {0}".format(test['num'] + 1))
                print("    Test: '{0}'".format(test['test']))
                print("Expected: {0}".format(repr(test['expected'])))
                print("  Actual: {0}".format(repr(test['actual'])))
            print()
            print("{0} / {1} tests passed".format(len(tests) - len(failed), len(tests)))
        else:
            print("All tests passed.")

        total_avgtime = 0
        for stage in timings.keys():
            avgtime = statistics.mean(timings[stage].values())
            total_avgtime += avgtime
            avgtime = self.format_timing(statistics.mean(timings[stage].values()))
            maxtime = max(timings[stage].values())
            maxexpr = [expr for expr, t in timings[stage].items() if t == maxtime][0]
            maxtime = self.format_timing(maxtime)
            print("Stage: {0:9} Average Time: {1:12} Longest Time: {2:12} Longest Expression: {3}".format(stage, avgtime, maxtime, self.format_test(maxexpr)))
        print("Total:           Average Time: {0:12}".format(self.format_timing(total_avgtime)))
        print()

    def format_timing(self, timing):
        return "{0} ms".format(round(timing * 1000, 3))

    def format_test(self, test):
        return test.replace("\n", "\\n")
