#!/usr/bin/python3

from modularcalculator.tests.testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *


print("ComputingCalculator tests:")
c = ModularCalculator('Computing')
hl = SyntaxHighlighter()

tests = [
    { 'test': '123 + 456', 'expected': Decimal(579) },
    { 'test': '123 + (1 * 3) - 456', 'expected': Decimal(-330) },
    { 'test': '2 + 3 * 4', 'expected': Decimal(14) },
    { 'test': '2+-3/4', 'expected': Decimal(1.25) },
    { 'test': '2 + 3^3', 'expected': Decimal(29) },
    { 'test': '4 * (2 + (3)) - 3', 'expected': Decimal(17) },
    { 'test': '14 % 3', 'expected': Decimal(2) },
    { 'test': r"stdev([1, 2, 3, 4])", 'expected': Decimal('1.290994448735805628393088466594') },
    { 'test': "'hello' +$ 'goodbye'", 'expected': 'hellogoodbye' },
    { 'test': r"'hello' +$ 'good\'bye\\'", 'expected': "hellogood'bye\\" },
    { 'test': r"123 +$ 'abc'", 'expected': '123abc' },
    { 'test': r"'123' +$ '456'", 'expected': '123456' },
    { 'test': r"'0b10' +$ '101'", 'expected': '0b10101' },
    { 'test': r"0b10 +$ 101", 'expected': '0b10101' },
    { 'test': r"'abc' *$ 3", 'expected': 'abcabcabc' },
    { 'test': r"'123' *$ 2", 'expected': '123123' },
    { 'test': r"'123' *$ 0b10", 'expected': '123123' },
    { 'test': r"'abc' *$ '3'", 'expected': 'abcabcabc' },
    { 'test': r"('12' +$ '3') - 100", 'expected': Decimal(23) },
    { 'test': r"'123.45' * 2", 'expected': Decimal('246.9') },
    { 'test': r"10 / 3", 'expected': Decimal('3.333333333333333333333333333333') },
    { 'test': r"(10 / 3) * 3", 'expected': Decimal('10') },
    { 'test': r"10 / 3 +$ ''", 'expected': '3.333333333333333333333333333333' },
    { 'test': r"((10 / 3 +$ '') *$ 1) * 3", 'expected': Decimal('9.999999999999999999999999999999') },

    { 'test': r"0b10", 'expected': '0b10' },
    { 'test': r"0B10", 'expected': '0b10' },
    { 'test': r"-0b11", 'expected': '-0b11' },
    { 'test': r"0b10.1", 'expected': '0b10.1' },
    { 'test': r"0b0", 'expected': '0b0' },
    { 'test': r"0b000", 'expected': '0b000' },
    { 'test': r"dec(0b10)", 'expected': Decimal('2') },
    { 'test': r"dec(0B10)", 'expected': Decimal('2') },
    { 'test': r"dec(-0b11)", 'expected': Decimal('-3') },
    { 'test': r"dec(0b10.1)", 'expected': Decimal('2.5') },
    { 'test': r"0b10 + 0b1", 'expected': '0b11' },
    { 'test': r"bin(0b10 + 0b1)", 'expected': '0b11' },
    { 'test': r"0b10 * 0b10", 'expected': '0b100' },
    { 'test': r"0b1000 / 0b10", 'expected': '0b0100' },
    { 'test': r"bin(0b10 * 0b10)", 'expected': '0b100' },
    { 'test': r"bin(0b10 * -0B10)", 'expected': '-0b100' },
    { 'test': r"dec(bin(0b10 * -0B10))", 'expected': Decimal('-4') },
    { 'test': r"bin(3.5)", 'expected': '0b11.1' },
    { 'test': r"bin(-3.5)", 'expected': '-0b11.1' },
    { 'test': r"bin(0)", 'expected': '0b0' },
    
    { 'test': r"oct(63)", 'expected': '0o77' },
    { 'test': r"dec(oct(63))", 'expected': Decimal('63') },
    { 'test': r"0o77", 'expected': '0o77' },
    { 'test': r"0o77.4", 'expected': '0o77.4' },
    { 'test': r"0o0", 'expected': '0o0' },
    { 'test': r"0o000", 'expected': '0o0' },
    { 'test': r"dec(0o77)", 'expected': Decimal('63') },
    { 'test': r"dec(0o77.4)", 'expected': Decimal('63.5') },
    { 'test': r"oct(63.5)", 'expected': '0o77.4' },
    { 'test': r"oct(-63.5)", 'expected': '-0o77.4' },
    { 'test': r"oct(0)", 'expected': '0o0' },
    
    { 'test': r"hex(255)", 'expected': '0xFF' },
    { 'test': r"dec(hex(255))", 'expected': Decimal('255') },
    { 'test': r"0xff", 'expected': '0xFF' },
    { 'test': r"0xf.88", 'expected': '0xF.88' },
    { 'test': r"0x0", 'expected': '0x0' },
    { 'test': r"0x000", 'expected': '0x0' },
    { 'test': r"dec(0xff)", 'expected': Decimal('255') },
    { 'test': r"dec(0xf.88)", 'expected': Decimal('15.53125') },
    { 'test': r"0xff + 0XFF", 'expected': '0x1FE' },
    { 'test': r"hex(15.125)", 'expected': '0xF.2' },
    { 'test': r"hex(-15.125)", 'expected': '-0xF.2' },
    { 'test': r"hex(0)", 'expected': '0x0' },

    { 'test': r"base(71, 36)", 'expected': '036z1Z' },
    { 'test': r"base(0, 36)", 'expected': '036z0' },
    { 'test': r"dec(base(71, 36))", 'expected': Decimal('71') },
    { 'test': r"036z1Z", 'expected': '036z1Z' },
    { 'test': r"-036z1Z", 'expected': '-036z1Z' },
    { 'test': r"dec(-036z1Z)", 'expected': Decimal('-71') },
    { 'test': r"036Z1z", 'expected': '036z1Z' },
    { 'test': r"04z1.2", 'expected': '04z1.2' },
    { 'test': r"dec(04z1.2)", 'expected': Decimal('1.5') },
    { 'test': r"02z100", 'expected': '02z100' },
    { 'test': r"02Z100", 'expected': '02z100' },
    { 'test': r"02Z0", 'expected': '02z0' },
    { 'test': r"02Z000", 'expected': '02z0' },
    { 'test': r"dec(036z1Z)", 'expected': Decimal('71') },
    { 'test': r"dec(036Z1z)", 'expected': Decimal('71') },
    { 'test': r"dec(02z100)", 'expected': Decimal('4') },
    { 'test': r"dec(02Z100)", 'expected': Decimal('4') },
    
    { 'test': r"true", 'expected': True },
    { 'test': r"false", 'expected': False },
    { 'test': r"TRUE ", 'expected': True },
    { 'test': r"false and false", 'expected': False },
    { 'test': r"false and true", 'expected': False },
    { 'test': r"true and false", 'expected': False },
    { 'test': r"true and true", 'expected': True },
    { 'test': r"false or false", 'expected': False },
    { 'test': r"false or true", 'expected': True },
    { 'test': r"true or false", 'expected': True },
    { 'test': r"true or true", 'expected': True },

    { 'test': r"true xor true", 'expected': False },
    { 'test': r"true xor false", 'expected': True },
    { 'test': r"false xor true", 'expected': True },
    { 'test': r"false xor false", 'expected': False },

    { 'test': r"true ==$ 'True'", 'expected': True },
    { 'test': r"true ==$ 'TRUE'", 'expected': False },
    { 'test': r"true ==~ 'TRUE'", 'expected': True },
    { 'test': r"true == true", 'expected': True },
    { 'test': r"false == false", 'expected': True },
    { 'test': r"true == false", 'expected': False },
    { 'test': r"true == 1", 'expected': True },
    { 'test': r"true == 0", 'expected': False },
    { 'test': r"false == 0", 'expected': True },
    { 'test': r"123.00 == 123", 'expected': True },
    { 'test': r"'123' == 123", 'expected': True },
    { 'test': r"'123.00' == 123", 'expected': True },
    { 'test': r"('123' + 0) == 123", 'expected': True },
    { 'test': r"'123' == (123 +$ '')", 'expected': True },
    { 'test': r"'123' ==$ 123", 'expected': True },
    { 'test': r"'abc' ==$ 'ABC'", 'expected': False },
    { 'test': r"'abc' ==~ 'ABC'", 'expected': True },
    { 'test': r"'abc' !=~ 'ABC'", 'expected': False },
    { 'test': r"'a' <$ 'b'", 'expected': True },
    { 'test': r"'a' <=$ 'A'", 'expected': False },
    { 'test': r"'a' <=~ 'A'", 'expected': True },
    { 'test': r"'a' >$ 'b'", 'expected': False },
    { 'test': r"123 < 14", 'expected': False },
    { 'test': r"123 <$ 14", 'expected': True },
    { 'test': r"true * true", 'expected': Decimal('1') },

    { 'test': r"not true", 'expected': False },
    { 'test': r"not false", 'expected': True },
    { 'test': r"not(not true)", 'expected': True },
    { 'test': r"not not true", 'expected': True },
    { 'test': r"not(true == false)", 'expected': True },
    { 'test': "\n((1 + 3)\n/ 2)\n", 'expected': Decimal(2) },

    { 'test': r"True then 1 else 2", 'expected': Decimal(1) },
    { 'test': r"False then 1 else 2", 'expected': Decimal(2) },
    { 'test': r"True then (False then 3 else 4) else 2", 'expected': Decimal(4) },
    { 'test': r"(3 > 2) then ((2 > 3) then 3 else 4) else 2", 'expected': Decimal(4) },
    { 'test': r"3 > 2 then (2 > 3 then 3 else 4) else 2", 'expected': Decimal(4) },
    { 'test': r"true then not(true or false) else true", 'expected': False },
    { 'test': r"true then 1 + 2 else true", 'expected': Decimal(3) },
    { 'test': "a = 1\nb = 2\ntrue then a else b = 3\na - b", 'expected': Decimal(1) },
    { 'test': "a = 1\nb = 2\nfalse then a else b = 3\na - b", 'expected': Decimal(-2) },
    { 'test': r"false then (1/0) else 2", 'expected': Decimal(2) },
    { 'test': r"false and (1/0)", 'expected': False },
    { 'test': r"true or (1/0)", 'expected': True },

    { 'test': "1 +\n2", 'expected': Decimal('3') },
    { 'test': "1 + 2\n3 + 4", 'expected': Decimal('7') },
    { 'test': "1 + 2 + \n3 + 4", 'expected': Decimal('10') },
    { 'test': "true then\n1\nelse\n2", 'expected': Decimal('1') },
    { 'test': "true then\n1 + 3\nelse\n2", 'expected': Decimal('4') },
    { 'test': "true then\n1\nelse\n2\n456", 'expected': Decimal('456') },

    { 'test': r"0b10101 & 0b110", 'expected': '0b00100' },
    { 'test': r"0b10101 | 0b110", 'expected': '0b10111' },
    { 'test': r"0b10101 ^^ 0b110", 'expected': '0b10011' },
    { 'test': r"~0b1011101", 'expected': '0b0100010' },
    { 'test': r"~0b00111100", 'expected': '0b11000011' },
    { 'test': r"~60", 'expected': Decimal('3') },
    { 'test': r"0b10101 << 1", 'expected': '0b101010' },
    { 'test': r"0b10101 << 2", 'expected': '0b1010100' },
    { 'test': r"0b10101 << 8", 'expected': '0b1010100000000' },
    { 'test': r"0b10010 >> 1", 'expected': '0b01001' },
    { 'test': r"0b10010 >> 3", 'expected': '0b00010' },
    { 'test': r"0b10010 >> 4", 'expected': '0b00001' },
    { 'test': r"0b10010 >> 5", 'expected': '0b00000' },

    { 'test': r"'ABC' =~ '\\w'", 'expected': True },
    { 'test': r"'ABC' =~ '\\d'", 'expected': False },
    { 'test': r"'ABC123abc' =~ '\\d{3}'", 'expected': True },
    { 'test': r"'ABC123abc' =~ '\\d{4}'", 'expected': False },
    { 'test': r"'ABC123abc' =~ '^\\w{3}\\d{3}\\w{3}$'", 'expected': True },
    { 'test': r"'ABC123abc' =~ '^\\w{3}\\d{3}\\w{2}$'", 'expected': False },
    { 'test': r"'ABC' !~ '\\w'", 'expected': False },
    { 'test': r"'ABC' !~ '\\d'", 'expected': True },
    { 'test': r"regexget('123ABC123', '[A-Z]+')", 'expected': 'ABC' },
    { 'test': r"regexget('123ABC456', '\\d+', 2)", 'expected': '456' },
    { 'test': r"regexsub('123ABC123', '[A-Z]+', 'defg')", 'expected': '123defg123' },
    { 'test': r"regexsub('123ABC456XYZ789', '[A-Z]+', 'defg')", 'expected': '123defg456defg789' },
    { 'test': r"regexsub('123ABC456XYZ789', '[A-Z]+', 'defg', 1)", 'expected': '123defg456XYZ789' },
    { 'test': r"regexsub('123456789', '[A-Z]+', 'defg')", 'expected': '123456789' },
    { 'test': r"regexcount('1abc2def3ghi4', '[a-z]{3}')", 'expected': Decimal(3) },

    { 'test': r"length('ABCabc')", 'expected': Decimal(6) },
    { 'test': r"lower('ABCabc')", 'expected': 'abcabc' },
    { 'test': r"upper('ABCabc')", 'expected': 'ABCABC' },
    { 'test': r"lstrip('   ABCabc   ', ' ')", 'expected': 'ABCabc   ' },
    { 'test': r"rstrip('   ABCabc   ', ' ')", 'expected': '   ABCabc' },
    { 'test': r"strip('   ABCabc   ', ' ')", 'expected': 'ABCabc' },
    { 'test': r"find('ABCabc', 'ab')", 'expected': Decimal(3) },
    { 'test': r"replace('ABCabc', 'BC', 'fgh')", 'expected': 'Afghabc' },
    { 'test': r"replace('ABCaBCbc', 'BC', 'fgh')", 'expected': 'Afghafghbc' },
    { 'test': r"substr('ABCabc', 3)", 'expected': 'abc' },
    { 'test': r"substr('ABCabc', -4)", 'expected': 'Cabc' },
    { 'test': r"substr('ABCabc', 3, 4)", 'expected': 'ab' },
    { 'test': r"substr('ABCabc', 4, 4)", 'expected': 'b' },
    { 'test': r"substr('ABCabc', 3, -1)", 'expected': 'abc' },
    { 'test': r"substr('ABCabc', 3, -2)", 'expected': 'ab' },
    { 'test': r"substr('ABCabc', -3, -2)", 'expected': 'ab' },
    { 'test': r"substr('123456', 4, 4)", 'expected': '5' },
    { 'test': r"substr('123456', 0b100, 0b100)", 'expected': '5' },

    { 'test': "123 + (#comment\n456)", 'expected': Decimal(579) },
    { 'test': "123 + 456#comment", 'expected': Decimal(579) },

    { 'test': r"false then 1m else 2cm", 'expected': (Decimal('2'), 'centimeters') },

    { 'test': "orbitheight = 36000km\nearthmass = 5.97237e24kg\nearthradius = 6378.1km\ngm = G earthmass\norbitradius = earthradius + orbitheight\ntime = 2 pi (orbitradius^3 / gm)^0.5\ntime to hours",
        'expected': (Decimal('24.116847271747239529834702110187'), 'hours') },
    { 'test': r"gm = G * 5.97237e24kg", 'expected': (Decimal('398600751696000'), 'meters^3/second^2') },

    { 'test': "datecreate(2001, 2, 3)", 'expected': '2001-02-03' },
    { 'test': "datecreate(2001, 2, 3, 12, 34, 56)", 'expected': '2001-02-03T12:34:56' },
    { 'test': "datecreate(2001, 2, 3, 12, 34, 56, 123456)", 'expected': '2001-02-03T12:34:56.123456' },
    { 'test': "datecreate(1, 2, 3)", 'expected': '0001-02-03' },
    { 'test': "datecreate(1, 2, 3, 9, 1, 2)", 'expected': '0001-02-03T09:01:02' },
    { 'test': "datecreate(1, 2, 3, 9, 1, 2, 3)", 'expected': '0001-02-03T09:01:02.000003' },
    { 'test': "dateformat('2012-01-02')", 'expected': 'Monday, 02-Jan-2012' },
    { 'test': "dateformat('2012-01-02T11:45:56')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56' },
    { 'test': "dateformat('2012-01-02T11:45:56.123456')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56.123456' },
    { 'test': "dateadd('2012-01-02T11:45:56', 5 seconds)", 'expected': '2012-01-02T11:46:01' },
    { 'test': "dateadd('2012-01-02T11:45:56', 0.123456 seconds)", 'expected': '2012-01-02T11:45:56.123456' },
    { 'test': "dateadd('2012-01-02T11:45:56', 5 hours)", 'expected': '2012-01-02T16:45:56' },
    { 'test': "dateadd('2012-01-02T11:45:56', 5 weeks)", 'expected': '2012-02-06T11:45:56' },
    { 'test': "dateadd(dateadd('0900-01-01', 1 year), 1 year)", 'expected': '0902-01-01T11:38:24' },
    { 'test': "datesubtract('2012-01-02T11:45:56', 5 seconds)", 'expected': '2012-01-02T11:45:51' },
    { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-04T11:45:56', days)", 'expected': (Decimal('2'), 'days') },
    { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-01T11:45:56', hours)", 'expected': (Decimal('24'), 'hours') },
    { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-02T11:45:56.123456', seconds)", 'expected': (Decimal('0.123456'), 'seconds') },
    { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-02T11:45:56.123456', microseconds)", 'expected': (Decimal('123456'), 'microseconds') },

    { 'test': "'2012-01-02T11:45:56' +% 5 seconds", 'expected': '2012-01-02T11:46:01' },
    { 'test': "'2012-01-02T11:45:56' -% 5 seconds", 'expected': '2012-01-02T11:45:51' },

    { 'test': r"[1, 4, 9] < 5", 'expected': [True, True, False] },
    { 'test': "a = [1, 4, 9]\n a < 5", 'expected': [True, True, False] },
    { 'test': "a = [1, 4, 9]\n a < 5 then a else 25", 'expected': [Decimal('1'), Decimal('4'), Decimal('25')] },
    { 'test': "a = [1 .. 7]\nfilter(a, a % 2 == 0)", 'expected': [Decimal('2'), Decimal('4'), Decimal('6')] },

    { 'test': "f = './examples/ext_func_addition'\n@f(5 - 4, 2)", 'expected': Decimal('3') },
    { 'test': "x=1 \nf = './examples/ext_func_addition'\n@f(5 - 4, 2) \nx", 'expected': Decimal('1') },

    { 'test': """#PARAM1 ||= 2^128
#PARAM1 = 0.0546
PARAM1 = 4

str = PARAM1
dec = find(str, '.')
decfound = dec > -1 then true else false

str = decfound then
    replace(str, '.', '')
    else str
leadingspaces = (str =~ '^(0+)') then
    length(regexget(str, '^(0+)'))
    else 0
dec = leadingspaces > 1 then
    (dec - (leadingspaces - 1))
    else dec
str = decfound then 
    substr(str, 0, 0) +$ '.' +$ substr(str, 1)
    else str
dec = decfound then
    dec - 1
    else length(str) - 2

str +$ '*10^' +$ dec""", 'expected': '4*10^-1' },

    { 'test': "orbitheight = 36000km\nearthmass = 5.97237e24kg\nearthradius = 6378.1km\ngm = G earthmass\norbitradius = earthradius + orbitheight\ntime = 2 pi (orbitradius^\n\n\n3 /\n\n\n\n gm\n\n\n\n\n\n\n\n)^\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n0.5\ntime to hours",
        'expected': (Decimal('24.116847271747239529834702110187'), 'hours') },

#    { 'test': r"", 'expected': '' },
]

tester = TestRunner(CalculatorException)
tester.test(c.calculate, tests)
