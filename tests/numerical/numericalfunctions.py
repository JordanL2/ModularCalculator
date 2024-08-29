#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalNumericalFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"abs(-4)", 'expected': Number('4') },

        { 'test': r"floor(1.4)", 'expected': Number('1') },
        { 'test': r"floor(1.5)", 'expected': Number('1') },
        { 'test': r"floor(1.599, 1)", 'expected': Number('1.5') },
        { 'test': r"floor(1.599, 2)", 'expected': Number('1.59') },

        { 'test': r"ceil(1.4)", 'expected': Number('2') },
        { 'test': r"ceil(1.5)", 'expected': Number('2') },
        { 'test': r"ceil(1.234, 1)", 'expected': Number('1.3') },
        { 'test': r"ceil(1.234, 2)", 'expected': Number('1.24') },

        { 'test': r"round(1.1)", 'expected': Number('1') },
        { 'test': r"round(1.5)", 'expected': Number('2') },
        { 'test': r"round(1.11, 1)", 'expected': Number('1.1') },
        { 'test': r"round(1.16, 1)", 'expected': Number('1.2') },

        { 'test': r"fact(5)", 'expected': Number('120') },
        { 'test': r"fact(-5)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute fact with parameters: -5 - fact parameter 1 must be of type(s) positive integer" } },
        { 'test': r"fact(5.5)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute fact with parameters: 5.5 - fact parameter 1 must be of type(s) positive integer" } },

        { 'test': r"exp(2)", 'expected':  Number('2955622439572260090892170984230003125272126228220718107667878170569356139218703132986928341992252001', '400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000') },

        { 'test': r"log(5)", 'expected': Number('1.609437912434100374600759333226187639525601354268517721912647891474178987707657764630133878093179611') },
        { 'test': r"log(5, 10)", 'expected': Number('0.6989700043360188047862611052755069732318101185378914586895725388728918107255754905130727478818138281') },
        { 'test': r"log(1.5, 2.5)", 'expected': Number('4425070493497599327014292680916407655627227037413818231546927105877211294771800184434107969520952601', '10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000') },
        { 'test': r"log(1, 0)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute log with parameters: 1, 0" } },
        { 'test': r"log(1, -0.5)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute log with parameters: 1, -0.5" } },

        { 'test': r"lcm(4, 5)", 'expected': Number('20') },
        { 'test': r"lcm(4, -5)", 'expected': Number('20') },
        { 'test': r"lcm(0.5, 1)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute lcm with parameters: 0.5, 1 - lcm parameter 1 must be of type(s) integer" } },
        { 'test': r"lcm(1, 0.5)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute lcm with parameters: 1, 0.5 - lcm parameter 2 must be of type(s) integer" } },

        { 'test': r"gcd(54, 60)", 'expected': Number('6') },
        { 'test': r"gcd(10, -5)", 'expected': Number('5') },
        { 'test': r"gcd(0.5, 1)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute gcd with parameters: 0.5, 1 - gcd parameter 1 must be of type(s) integer" } },
        { 'test': r"gcd(1, 0.5)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute gcd with parameters: 1, 0.5 - gcd parameter 2 must be of type(s) integer" } },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalNumericalFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
