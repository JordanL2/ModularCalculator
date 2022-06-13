#!/usr/bin/python3

from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestComputingCalculator(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': '123 + 456', 'expected': Number(579) },
        { 'test': '123 + (1 * 3) - 456', 'expected': Number(-330) },
        { 'test': '2 + 3 * 4', 'expected': Number(14) },
        { 'test': '2+-3/4', 'expected': Number('1.25') },
        { 'test': '2 + 3^3', 'expected': Number(29) },
        { 'test': '4 * (2 + (3)) - 3', 'expected': Number(17) },
        { 'test': '14 % 3', 'expected': Number(2) },
        { 'test': r"stdev([1, 2, 3, 4])", 'expected': Number('645497224367902814196544233297066601805486950881931804431262294352247181989496505586547896143112253', '500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000') },
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
        { 'test': r"('12' +$ '3') - 100", 'expected': Number(23) },
        { 'test': r"'123.45' * 2", 'expected': Number('246.9') },
        { 'test': r"10 / 3", 'expected': Number(10, 3) },
        { 'test': r"(10 / 3) * 3", 'expected': Number('10') },
        { 'test': r"10 / 3 +$ ''", 'expected': '3.333333333333333333333333333333' },
        { 'test': r"((10 / 3 +$ '') *$ 1) * 3", 'expected': Number('9.999999999999999999999999999999') },

        { 'test': r"0b10", 'cast': str, 'expected': '0b10' },
        { 'test': r"0B10", 'cast': str, 'expected': '0b10' },
        { 'test': r"-0b11", 'cast': str, 'expected': '-0b11' },
        { 'test': r"0b10.1", 'cast': str, 'expected': '0b10.1' },
        { 'test': r"0b0", 'cast': str, 'expected': '0b0' },
        { 'test': r"0b000", 'cast': str, 'expected': '0b000' },
        { 'test': r"dec(0b10)", 'expected': Number('2') },
        { 'test': r"dec(0B10)", 'expected': Number('2') },
        { 'test': r"dec(-0b11)", 'expected': Number('-3') },
        { 'test': r"dec(0b10.1)", 'expected': Number('2.5') },
        { 'test': r"0b10 + 0b1", 'cast': str, 'expected': '0b11' },
        { 'test': r"bin(0b10 + 0b1)", 'cast': str, 'expected': '0b11' },
        { 'test': r"0b10 * 0b10", 'cast': str, 'expected': '0b100' },
        { 'test': r"0b1000 / 0b10", 'cast': str, 'expected': '0b0100' },
        { 'test': r"bin(0b10 * 0b10)", 'cast': str, 'expected': '0b100' },
        { 'test': r"bin(0b10 * -0B10)", 'cast': str, 'expected': '-0b100' },
        { 'test': r"dec(bin(0b10 * -0B10))", 'expected': Number('-4') },
        { 'test': r"bin(0.5)", 'cast': str, 'expected': '0b0.1' },
        { 'test': r"bin(3.5)", 'cast': str, 'expected': '0b11.1' },
        { 'test': r"bin(-3.5)", 'cast': str, 'expected': '-0b11.1' },
        { 'test': r"bin(0)", 'cast': str, 'expected': '0b0' },
        { 'test': r"bin(0x1A)", 'cast': str, 'expected': '0b11010' },
        { 'test': r"0b10 / 0b11", 'cast': str, 'expected': '0b00.10101010101010101010101010101' },
        { 'test': r"0b1 / 0b10", 'cast': str, 'expected': '0b0.1' },
        { 'test': "a = (0b10 / 0b11)\na * 0b11", 'cast': str, 'expected': '0b10' },
        { 'test': r"((0b10 / 0b11) * 0b11)", 'cast': str, 'expected': '0b10' },
        { 'test': r"fact(0b101)", 'cast': str, 'expected': '0b1111000' },

        { 'test': r"oct(63)", 'cast': str, 'expected': '0o77' },
        { 'test': r"dec(oct(63))", 'expected': Number('63') },
        { 'test': r"0o77", 'cast': str, 'expected': '0o77' },
        { 'test': r"0o77.4", 'cast': str, 'expected': '0o77.4' },
        { 'test': r"0o0", 'cast': str, 'expected': '0o0' },
        { 'test': r"0o000", 'cast': str, 'expected': '0o0' },
        { 'test': r"dec(0o77)", 'expected': Number('63') },
        { 'test': r"dec(0o77.4)", 'expected': Number('63.5') },
        { 'test': r"oct(63.5)", 'cast': str, 'expected': '0o77.4' },
        { 'test': r"oct(-63.5)", 'cast': str, 'expected': '-0o77.4' },
        { 'test': r"oct(0)", 'cast': str, 'expected': '0o0' },
        { 'test': r"oct(0b10101)", 'cast': str, 'expected': '0o25' },

        { 'test': r"hex(255)", 'cast': str, 'expected': '0xFF' },
        { 'test': r"dec(hex(255))", 'expected': Number('255') },
        { 'test': r"0xff", 'cast': str, 'expected': '0xFF' },
        { 'test': r"0xf.88", 'cast': str, 'expected': '0xF.88' },
        { 'test': r"0x0", 'cast': str, 'expected': '0x0' },
        { 'test': r"0x000", 'cast': str, 'expected': '0x0' },
        { 'test': r"dec(0xff)", 'expected': Number('255') },
        { 'test': r"dec(0xf.88)", 'expected': Number('15.53125') },
        { 'test': r"0xff + 0XFF", 'cast': str, 'expected': '0x1FE' },
        { 'test': r"hex(15.125)", 'cast': str, 'expected': '0xF.2' },
        { 'test': r"hex(0b10101)", 'cast': str, 'expected': '0x15' },
        { 'test': r"hex(-15.125)", 'cast': str, 'expected': '-0xF.2' },
        { 'test': r"hex(0)", 'cast': str, 'expected': '0x0' },
        { 'test': r"0xF + 4", 'cast': str, 'expected': '0x13' },
        { 'test': r"4 + 0xF", 'expected': Number('19') },
        { 'test': r"0x1 / 0x2", 'cast': str, 'expected': '0x0.8' },
        { 'test': r"0x2 / 0x3", 'cast': str, 'expected': '0x0.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' },

        { 'test': r"base(71, 36)", 'cast': str, 'expected': '36z1Z' },
        { 'test': r"base(0, 36)", 'cast': str, 'expected': '36z0' },
        { 'test': r"base(7, 10)", 'cast': str, 'expected': '10z7' },
        { 'test': r"dec(base(71, 36))", 'expected': Number('71') },
        { 'test': r"36z1Z", 'cast': str, 'expected': '36z1Z' },
        { 'test': r"-36z1Z", 'cast': str, 'expected': '-36z1Z' },
        { 'test': r"dec(-36z1Z)", 'expected': Number('-71') },
        { 'test': r"36Z1z", 'cast': str, 'expected': '36z1Z' },
        { 'test': r"4z1.2", 'cast': str, 'expected': '4z1.2' },
        { 'test': r"dec(4z1.2)", 'expected': Number('1.5') },
        { 'test': r"2z100", 'cast': str, 'expected': '2z100' },
        { 'test': r"2Z100", 'cast': str, 'expected': '2z100' },
        { 'test': r"2Z0", 'cast': str, 'expected': '2z0' },
        { 'test': r"02Z0", 'cast': str, 'expected': '2z0' },
        { 'test': r"002Z0", 'cast': str, 'expected': '2z0' },
        { 'test': r"2Z000", 'cast': str, 'expected': '2z0' },
        { 'test': r"dec(36z1Z)", 'expected': Number('71') },
        { 'test': r"dec(36Z1z)", 'expected': Number('71') },
        { 'test': r"dec(2z100)", 'expected': Number('4') },
        { 'test': r"dec(2Z100)", 'expected': Number('4') },

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
        { 'test': r"true * true", 'expected': Number(1) },
        { 'test': r"true * false", 'expected': Number(0) },

        { 'test': r"not true", 'expected': False },
        { 'test': r"not false", 'expected': True },
        { 'test': r"not(not true)", 'expected': True },
        { 'test': r"not not true", 'expected': True },
        { 'test': r"not(true == false)", 'expected': True },
        { 'test': "\n((1 + 3)\n/ 2)\n", 'expected': Number(2) },

        { 'test': r"True then 1 else 2", 'expected': Number(1) },
        { 'test': r"False then 1 else 2", 'expected': Number(2) },
        { 'test': r"True then (False then 3 else 4) else 2", 'expected': Number(4) },
        { 'test': r"(3 > 2) then ((2 > 3) then 3 else 4) else 2", 'expected': Number(4) },
        { 'test': r"3 > 2 then (2 > 3 then 3 else 4) else 2", 'expected': Number(4) },
        { 'test': r"true then not(true or false) else true", 'expected': False },
        { 'test': r"true then 1 + 2 else true", 'expected': Number(3) },
        { 'test': "a = 1\nb = 2\ntrue then a else b = 3\na - b", 'expected': Number(1) },
        { 'test': "a = 1\nb = 2\nfalse then a else b = 3\na - b", 'expected': Number(-2) },
        { 'test': r"false then (1/0) else 2", 'expected': Number(2) },
        { 'test': r"false then 1/0 else 2", 'expected': Number('2') },
        { 'test': r"false and (1/0)", 'expected': False },
        { 'test': r"true or (1/0)", 'expected': True },

        { 'test': "1 +\n2", 'expected': Number('3') },
        { 'test': "1 + 2\n3 + 4", 'expected': Number('7') },
        { 'test': "1 + 2 + \n3 + 4", 'expected': Number('10') },
        { 'test': "true then\n1\nelse\n2", 'expected': Number('1') },
        { 'test': "true then\n1 + 3\nelse\n2", 'expected': Number('4') },
        { 'test': "true then\n1\nelse\n2\n456", 'expected': Number('456') },
        { 'test': "a = [0, 1]\n(a > 0) then 1 / a else 0", 'expected': [Number('0'), Number('1')] },
        { 'test': "a = [0, 1]\nb = 1 / a\nfilter(b, a > 0)", 'expected': [Number('1')] },

        { 'test': r"0b10101 & 0b110", 'cast': str, 'expected': '0b00100' },
        { 'test': r"0b10101 | 0b110", 'cast': str, 'expected': '0b10111' },
        { 'test': r"0b10101 ^^ 0b110", 'cast': str, 'expected': '0b10011' },
        { 'test': r"~0b1011101", 'cast': str, 'expected': '0b0100010' },
        { 'test': r"~0b00111100", 'cast': str, 'expected': '0b11000011' },
        { 'test': r"~60", 'expected': Number('3') },
        { 'test': r"0b10101 << 1", 'cast': str, 'expected': '0b101010' },
        { 'test': r"0b10101 << 2", 'cast': str, 'expected': '0b1010100' },
        { 'test': r"0b10101 << 8", 'cast': str, 'expected': '0b1010100000000' },
        { 'test': r"0b10010 >> 1", 'cast': str, 'expected': '0b01001' },
        { 'test': r"0b10010 >> 3", 'cast': str, 'expected': '0b00010' },
        { 'test': r"0b10010 >> 4", 'cast': str, 'expected': '0b00001' },
        { 'test': r"0b10010 >> 5", 'cast': str, 'expected': '0b00000' },

        { 'test': r"'ABC' =~ '\\w'", 'expected': True },
        { 'test': r"'ABC' =~ '\\d'", 'expected': False },
        { 'test': r"'ABC123abc' =~ '\\d{3}'", 'expected': True },
        { 'test': r"'ABC123abc' =~ '\\d{4}'", 'expected': False },
        { 'test': r"'ABC123abc' =~ '^\\w{3}\\d{3}\\w{3}$'", 'expected': True },
        { 'test': r"'ABC123abc' =~ '^\\w{3}\\d{3}\\w{2}$'", 'expected': False },
        { 'test': r"'ABC' !~ '\\w'", 'expected': False },
        { 'test': r"'ABC' !~ '\\d'", 'expected': True },
        { 'test': r"regexget('123ABC123DEF123GHI123', '[A-Z]+')", 'expected': ['ABC', 'DEF', 'GHI'] },
        { 'test': r"regexget('123ABC456', '\\d+', 2)", 'expected': '456' },
        { 'test': r"regexsub('123ABC123', '[A-Z]+', 'defg')", 'expected': '123defg123' },
        { 'test': r"regexsub('123ABC456XYZ789', '[A-Z]+', 'defg')", 'expected': '123defg456defg789' },
        { 'test': r"regexsub('123ABC456XYZ789', '[A-Z]+', 'defg', 1)", 'expected': '123defg456XYZ789' },
        { 'test': r"regexsub('123456789', '[A-Z]+', 'defg')", 'expected': '123456789' },
        { 'test': r"regexcount('1abc2def3ghi4', '[a-z]{3}')", 'expected': Number(3) },
        { 'test': r"regexsplit('123ABC456XYZ789', '[A-Z]+')", 'expected': ['123', '456', '789'] },
        { 'test': r"regexsplit('123A456XY789', '[A-Z]')", 'expected': ['123', '456', '', '789'] },
        { 'test': r"regexsplit('123A456XY789Z', '[A-Z]')", 'expected': ['123', '456', '', '789', ''] },
        { 'test': r"regexsplit('Z123A456XY789Z', '[A-Z]')", 'expected': ['', '123', '456', '', '789', ''] },
        { 'test': r"regexsplit('Z123A456XY789Z', '[A-Z]+')", 'expected': ['', '123', '456', '789', ''] },

        { 'test': r"length('ABCabc')", 'expected': Number(6) },
        { 'test': r"lower('ABCabc')", 'expected': 'abcabc' },
        { 'test': r"upper('ABCabc')", 'expected': 'ABCABC' },
        { 'test': r"lstrip('   ABCabc   ', ' ')", 'expected': 'ABCabc   ' },
        { 'test': r"rstrip('   ABCabc   ', ' ')", 'expected': '   ABCabc' },
        { 'test': r"strip('   ABCabc   ', ' ')", 'expected': 'ABCabc' },
        { 'test': r"find('ABCabc', 'ab')", 'expected': Number(3) },
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

        { 'test': r"join(['ab', 'b', 'c'], '||')", 'expected': 'ab||b||c' },
        { 'test': r"join(['ab', 'b', 2], '||')", 'expected': 'ab||b||2' },
        { 'test': r"join(['ab', 'b', 2])", 'expected': 'abb2' },
        { 'test': r"split('ab||b||2', '||')", 'expected': ['ab', 'b', '2'] },
        { 'test': r"split(12345367, 3)", 'expected': ['12', '45', '67'] },

        { 'test': "123 + (#comment\n456)", 'expected': Number(579) },
        { 'test': "123 + 456#comment", 'expected': Number(579) },

        { 'test': r"false then 1m else 2cm", 'expected': (Number('2'), 'centimeters') },

        { 'test': "orbitheight = 36000km\nearthmass = 5.97237e24kg\nearthradius = 6378.1km\ngm = G earthmass\norbitradius = earthradius + orbitheight\ntime = 2 pi (orbitradius^3 / gm)^0.5\ntime to hours",
            'expected': (Number(24224627632301628480899537366063915829476650214457110900687610652121970296857515944613469683003093000, 1004469089982613651157596952472639188035748634295889087727188244396625333452077251111878745939773897), 'hours') },
        { 'test': r"gm = G * 5.97237e24kg", 'expected': (Number('398600751696000'), 'meters^3/second^2') },

        { 'test': "dateformat('2012-01-02')", 'expected': 'Monday, 02-Jan-2012' },
        { 'test': "dateformat('2012-01-02T11:45:56')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56' },
        { 'test': "dateformat('2012-01-02T11:45:56.123456')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56.123456' },
        { 'test': "dateformat('2012-01-02+0100')", 'expected': 'Monday, 02-Jan-2012 (+0100)' },
        { 'test': "dateformat('2012-01-02T11:45:56-0430')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56 (-0430)' },
        { 'test': "dateformat('2012-01-02T11:45:56.123456+1256')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56.123456 (+1256)' },
        { 'test': "dateadd('2012-01-02T11:45:56', 5 seconds)", 'expected': '2012-01-02T11:46:01' },
        { 'test': "dateadd('2012-01-02T11:45:56', 0.123456 seconds)", 'expected': '2012-01-02T11:45:56.123456' },
        { 'test': "dateadd('2012-01-02T11:45:56', 5 hours)", 'expected': '2012-01-02T16:45:56' },
        { 'test': "dateadd('2012-01-02T11:45:56', 5 weeks)", 'expected': '2012-02-06T11:45:56' },
        { 'test': "dateadd(dateadd('0900-01-01', 1 year), 1 year)", 'expected': '0902-01-01T11:38:24' },
        { 'test': "datesubtract('2012-01-02T11:45:56', 5 seconds)", 'expected': '2012-01-02T11:45:51' },
        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-04T11:45:56', days)", 'expected': (Number('2'), 'days') },
        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-01T11:45:56', hours)", 'expected': (Number('24'), 'hours') },
        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-02T11:45:56.123456', seconds)", 'expected': (Number('0.123456'), 'seconds') },
        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-02T11:45:56.123456')", 'expected': (Number('0.123456'), 'seconds') },
        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-02T11:45:56.123456', microseconds)", 'expected': (Number('123456'), 'microseconds') },
        { 'test': "datedifference('2012-01-02-0200', '2012-01-02T04:00:00+0100', hours)", 'expected': (Number('1'), 'hour') },
        { 'test': "datedifference('2012-01-02T11:45:56-0200', '2012-01-02T11:45:56+0100', hours)", 'expected': (Number('3'), 'hours') },
        { 'test': "datedifference('2012-01-02-0200', '2012-01-02T11:45:56.123456+0100', microseconds)", 'expected': (Number('31556123456'), 'microseconds') },

        { 'test': "'2012-01-02T11:45:56' +% 5 seconds", 'expected': '2012-01-02T11:46:01' },
        { 'test': "'2012-01-02T11:45:56' -% 5 seconds", 'expected': '2012-01-02T11:45:51' },

        { 'test': r"[1, 4, 9] < 5", 'expected': [True, True, False] },
        { 'test': "a = [1, 4, 9]\n a < 5", 'expected': [True, True, False] },
        { 'test': "a = [1, 4, 9]\n a < 5 then a else 25", 'expected': [Number('1'), Number('4'), Number('25')] },
        { 'test': "a = [1 .. 7]\nfilter(a, a % 2 == 0)", 'expected': [Number('2'), Number('4'), Number('6')] },
        { 'test': r"mean([5, 0xF])", 'expected': Number('10') },
        { 'test': r"mean([0xF, 5])", 'cast': str, 'expected': '0xA' },

        { 'test': "f = './tests/externalfunctions/ext_func_addition'\n@f(5 - 4, 2)", 'expected': Number('3') },
        { 'test': "x=1 \nf = './tests/externalfunctions/ext_func_addition'\n@f(5 - 4, 2) \nx", 'expected': Number('1') },
        { 'test': "f = './tests/externalfunctions/mean'\n@f([1 .. 10])", 'expected': Number('5.5') },

        { 'test': "f = './tests/externalfunctions/acceleration'\n@f(20s, 5m/s^2)", 'expected': (Number('100'), 'meters/second') },

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
        length(regexget(str, '^(0+)', 1))
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
            'expected': (Number(24224627632301628480899537366063915829476650214457110900687610652121970296857515944613469683003093000, 1004469089982613651157596952472639188035748634295889087727188244396625333452077251111878745939773897), 'hours') },

        { 'test': "f = './tests/externalfunctions/distance'\n@f([0, 0], [3, 4])", 'expected': Number('5') },

    #    { 'test': r"", 'expected': '' },
    ]

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestComputingCalculator.prepare_tests()

if __name__ == '__main__':
    execute_tests()
