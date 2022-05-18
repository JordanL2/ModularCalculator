#!/usr/bin/python3

from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *

import argparse


print("ScientificCalculator tests:")
c = ModularCalculator('Scientific')
hl = SyntaxHighlighter()

parser = argparse.ArgumentParser()
parser.add_argument('-n', dest='times', nargs='?', type=int, default=1, help='number of times to run the tests')
parser.add_argument('-t', dest='test',  nargs='?', type=int, default=0, help='test to run')
args = parser.parse_args()
times = args.times
test = args.test

tests = [
    { 'test': 'min([1, 2, 3])', 'expected': Number('1') },
    { 'test': '1 + (( min([ 2, -1,  3 ])))', 'expected': Number('0') },
    { 'test': '( min([ min([4,5,6]), min([2,8,9]),  min([3,7,8]) ]))', 'expected': Number('2') },
    { 'test': '( min([ min([4,5,6]), min([2,8,9])+1,  min([3,7,8]) ]))', 'expected': Number('3') },
    { 'test': '( min([ min([4,5,6]), 2 * min([2,8,9]) - 3,  min([3,7,8]) ]))', 'expected': Number('1') },
    { 'test': '( min([ min([4,5,6]), 2 * min([2,8,9])-3,  min([3,7,8]) ]))', 'expected': Number('1') },
    { 'test': '(min([min([4,5,6]),((2 * min([2,8,9])-(3 + 1))),min([3,7,8]) ]))', 'expected': Number('0') },

    { 'test': r"abs(-4)", 'expected': Number('4') },
    { 'test': r"fact(5)", 'expected': Number('120') },
    { 'test': r"log(5)", 'expected': Number('1.609437912434100374600759333226187639525601354268517721912647891474178987707657764630133878093179611') },
    { 'test': r"log(5, 10)", 'expected': Number('0.6989700043360188047862611052755069732318101185378914586895725388728918107255754905130727478818138281') },

    { 'test': r"max([3, 5, 7])", 'expected': Number('7') },
    { 'test': r"mean([2, 3, 5, 6])", 'expected': Number('4') },
    { 'test': r"median([6, 1, 9])", 'expected': Number('6') },
    { 'test': r"mode([1, 1, 2, 4])", 'expected': Number('1') },
    { 'test': r"stdev([1, 2, 3, 4])", 'expected': Number(645497224367902814196544233297066601805486950881931804431262294352247181989496505586547896143112253, 500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000) },
    { 'test': r"sum([1, 2, 3, 4])", 'expected': Number('10') },
    { 'test': r"sum(([10]))", 'expected': Number('10') },
    { 'test': r"sum([(10)])", 'expected': Number('10') },
    { 'test': r"sum([(1), 2, 3])", 'expected': Number('6') },
    { 'test': r"sum(([(1), 2, 3]))", 'expected': Number('6') },
    { 'test': r"sum([1, (2), 3])", 'expected': Number('6') },
    { 'test': r"sum([1, 2, (3)])", 'expected': Number('6') },
    { 'test': r"sum([1, 2, (3) + 2])", 'expected': Number('8') },
    { 'test': r"sum([(1), 2, 3 + 2])", 'expected': Number('8') },
    { 'test': r"sum([ (10) ])", 'expected': Number('10') },
    { 'test': r"sum( [ (10) ] )", 'expected': Number('10') },
    { 'test': r"sum([( 10 )])", 'expected': Number('10') },
    { 'test': r"sum( [( 10 )] )", 'expected': Number('10') },

    { 'test': r"floor(1.4)", 'expected': Number('1') },
    { 'test': r"floor(1.5)", 'expected': Number('1') },
    { 'test': r"ceil(1.4)", 'expected': Number('2') },
    { 'test': r"ceil(1.5)", 'expected': Number('2') },
    { 'test': r"round(1.1)", 'expected': Number('1') },
    { 'test': r"round(1.5)", 'expected': Number('2') },
    { 'test': r"round(1.11, 1)", 'expected': Number('1.1') },
    { 'test': r"round(1.16, 1)", 'expected': Number('1.2') },

    { 'test': r"dec(1.234e1)", 'expected': Number('12.34') },
    { 'test': r"dec(1.234e10)", 'expected': Number('12340000000') },
    { 'test': r"dec(1.234e2)", 'expected': Number('123.4') },
    { 'test': r"dec(1.234e0)", 'expected': Number('1.234') },
    { 'test': r"dec(1.234e-1)", 'expected': Number('0.1234') },
    { 'test': r"dec(1.234e-2)", 'expected': Number('0.01234') },
    { 'test': r"dec(5.97237e24 kg)", 'expected': (Number('5972370000000000000000000'), 'kilograms') },
    { 'test': r"1.23e2 + 1.2e1", 'expected': '1.35E2' },
    { 'test': r"1.23e2kg + 1.2e1kg", 'expected': ('1.35E2', 'kilograms') },
    { 'test': r"dec(1.23e2 + 1.2e1)", 'expected': Number('135') },
    { 'test': r"1E9 * 1", 'expected': '1E9' },
    { 'test': r"1 * 1E9", 'expected': Number('1000000000') },
    { 'test': r"dec(1E9)", 'expected': Number('1000000000') },
    { 'test': r"1E9 m", 'expected': ('1E9', 'meters') },
    { 'test': r"dec(1E9 m)", 'expected': (Number('1000000000'), 'meters') },
    { 'test': r"dec(1E9) m", 'expected': (Number('1000000000'), 'meters') },

    { 'test': r"scientific(123.456789)", 'expected': '1.23456789E2' },
    { 'test': r"scientific(123.45678900000)", 'expected': '1.23456789E2' },
    { 'test': r"scientific(12345678900000)", 'expected': '1.23456789E13' },
    { 'test': r"scientific(123.456789, 3)", 'expected': '1.235E2' },
    { 'test': r"scientific(123.456789, 5)", 'expected': '1.23457E2' },
    { 'test': r"scientific(0.000123456789, 5)", 'expected': '1.23457E-4' },
    { 'test': r"scientific(123.456789 miles)", 'expected': ('1.23456789E2', 'miles') },

    { 'test': r"3 meters to feet", 'expected': (Number(1250, 127), 'feet') },
    { 'test': r"3.5 meters to feet", 'expected': (Number(4375, 381), 'feet') },
    { 'test': r"0.035 meters to feet", 'expected': (Number(175, 1524), 'feet') },
    { 'test': r"-0.035 meters to feet", 'expected': (Number(-175, 1524), 'feet') },
    { 'test': r"3.5 feet to meters", 'expected': (Number('1.0668'), 'meters') },
    { 'test': r"35000000 feet to meters", 'expected': (Number('10668000'), 'meters') },
    { 'test': r"-200 °C to K", 'expected': (Number('73.15'), 'kelvin') },
    { 'test': r"20 °C to °F", 'expected': (Number('68'), 'Fahrenheit') },
    { 'test': r"20000 °C to °F", 'expected': (Number('36032'), 'Fahrenheit') },
    { 'test': r"68 °F to °C", 'expected': (Number('20'), 'Celsius') },

    { 'test': r"123 meters", 'expected': (Number('123'), 'meters') },
    { 'test': r"1 meters + 2 meters", 'expected': (Number('3'), 'meters') },
    { 'test': r"1 meters * 2", 'expected': (Number('2'), 'meters') },
    { 'test': r"6 meters / 2", 'expected': (Number('3'), 'meters') },
    { 'test': r"1 metre", 'expected': (Number('1'), 'meter') },
    { 'test': r"1 meter + 23 cm", 'expected': (Number('1.23'), 'meters') },
    { 'test': r"1 meter + 23 µm", 'expected': (Number('1.000023'), 'meters') },
    { 'test': r"1 meter + 23 nm", 'expected': (Number('1.000000023'), 'meters') },
    { 'test': r"1K + 1K", 'expected': (Number('2'), 'kelvin') },
    { 'test': r"1°C + 1°C", 'expected': (Number('2'), 'Celsius') },
    { 'test': r"1K + 1°C", 'expected': (Number('2'), 'kelvin') },
    { 'test': r"1°C + 1K", 'expected': (Number('2'), 'Celsius') },

    { 'test': r"meters * meters", 'expected': 'meters^2' },
    { 'test': r"2 meters * 3 meters", 'expected': (Number('6'), 'meters^2') },
    { 'test': r"20 meters / 5 meters", 'expected': Number('4') },
    { 'test': r"20 meters \ 5 meters", 'expected': Number('4') },
    { 'test': r"12 meters * 3°C", 'expected': (Number('36'), 'meter Celsius') },
    { 'test': r"2 meters * 3 meters * 4 meters", 'expected': (Number('24'), 'meters^3') },
    { 'test': r"(2 meters * 3 meters * 4 meters) / 2 meters", 'expected': (Number('12'), 'meters^2') },
    { 'test': r"(2 meters * 3 meters * 4 meters) / (2 meters * 4 meters)", 'expected': (Number('3'), 'meters') },
    { 'test': r"(2 meters * 3 meters) / 2 feet", 'expected': (Number(1250, 127), 'meters') },
    { 'test': r"(2 meters * 3 meters * 4 meters) / (5 feet * 6 feet)", 'expected': (Number(1250000, 145161), 'meters') },
    { 'test': r"2 m/s", 'expected': (Number('2'), 'meters/second') },
    { 'test': r"2 m/s + 3 m/s", 'expected': (Number('5'), 'meters/second') },
    { 'test': r"2 m/s + 3 miles/hour", 'expected': (Number('3.34112'), 'meters/second') },
    { 'test': r"2 m/s to miles/hour", 'expected': (Number(6250, 1397), 'miles/hour') },
    { 'test': r"2 m^2", 'expected': (Number('2'), 'meters^2') },
    { 'test': r"2 m^3", 'expected': (Number('2'), 'meters^3') },
    { 'test': r"2 m^2 to feet^2", 'expected': (Number(3125000, 145161), 'feet^2') },

    { 'test': r"40 * (meters*meters) / (seconds*seconds) * 2 meters", 'expected': (Number('80'), 'meters^3/second^2') },
    { 'test': r"12 meters °C / s", 'expected': (Number('12'), 'meter Celsius/second') },
    { 'test': r"0.625 meters/(second^2 celsius) * 4°C", 'expected': (Number('2.5'), 'meters/second^2') },
    { 'test': r"40 TW h / yr", 'expected': (Number('40'), 'terawatt hours/year') },
    { 'test': r"compact(40 TW h / yr)", 'expected': (Number(2000000, 438291), 'gigawatts') },
    { 'test': r"0.004563084645220168834131873146 TW to TW h / yr", 'expected': (Number(999979466119096509240246406516743, 25000000000000000000000000000000), 'terawatt hours/year') },
    { 'test': r"40 TW h / yr to MW", 'expected': (Number(2000000000, 438291), 'megawatts') },
    { 'test': r"40 TW h / yr to W", 'expected': (Number(2000000000000000, 438291), 'watts') },

    { 'test': r"1 kW to J/s", 'expected': (Number('1000'), 'joules/second') },
    { 'test': r"kW to J/s", 'expected': (Number('1000'), 'joules/second') },
    { 'test': r"1 meters^3 to l", 'expected': (Number('1000'), 'liters') },
    { 'test': r"1 kW + 23 J/s", 'expected': (Number('1.023'), 'kilowatts') },
    { 'test': r"1 J/h + 2 kW", 'expected': (Number('7200001'), 'joules/hour') },
    { 'test': r"1l / 10cm", 'expected': (Number('100'), 'centimeters^2') },
    { 'test': r"1l / 10cm^2", 'expected': (Number('1'), 'meter') },
    { 'test': r"1 km J/h + 2 m kW", 'expected': (Number('7201'), 'kilometer joules/hour') },
    { 'test': r"1 km W + 2 m W", 'expected': (Number('1.002'), 'kilometer watts') },
    { 'test': r"1 kW / (100 J/s)", 'expected': Number('10') },
    { 'test': r"10 W s + 23 J", 'expected': (Number('33'), 'watt seconds') },
    { 'test': r"100J / 2W", 'expected': (Number('50'), 'seconds') },
    { 'test': r"(100 W h) / (10 J/s)", 'expected': (Number('10'), 'hours') },
    { 'test': r"1000000 liters / 1 hectare", 'expected': (Number('10'), 'centimeters') },
    { 'test': r"(1l) / (10cm °C)", 'expected': (Number('100'), 'centimeters^2/Celsius') },
    { 'test': r"1 hectare * 1 cm", 'expected': (Number('100000'), 'liters') },
    { 'test': r"10 W s / 2J", 'expected': Number('5') },
    { 'test': r"100 mi / 2 knots", 'expected': (Number(55880000000000000000000000000000000000000000000000000000000000, 1286111111111111111111111111111111111111111111111111111111111), 'hours') },
    { 'test': r"100 nmi / 2 knots", 'expected': (Number('50'), 'hours') },
    { 'test': r"0 nmi / 2 knots", 'expected': (Number('0'), 'hours') },
    { 'test': r"(100 mi) / (2 mi/h)", 'expected': (Number('50'), 'hours') },
    { 'test': r"1 UK pint + 2 UK pints", 'expected': (Number('3'), 'UK pints') },
    { 'test': r"1 liter + 2 UK pints", 'expected': (Number('2.1365225'), 'liters') },
    { 'test': r"1N + 2kg m/s/s", 'expected': (Number('3'), 'newtons') },
    { 'test': r"2 gee * 10 s", 'expected': (Number('196.133'), 'meters/second') },
    { 'test': r"10W to kg m^2 s^-3", 'expected': (Number('10'), 'kilogram meters^2/second^3') },
    { 'test': r"10 kg m^2/s^3 to J/s", 'expected': (Number('10'), 'joules/second') },
    { 'test': r"10 kg m^2/s^3", 'expected': (Number('10'), 'kilogram meters^2/second^3') },
    { 'test': r"20 kg m^2 / 2s^3", 'expected': (Number('10'), 'watts') },

    { 'test': r"1 kW / 100 J/s", 'expected': Number('10') },
    { 'test': r"1 GRAM to kg", 'expected': (Number('0.001'), 'kilograms') },
    { 'test': r"(2kg)^1", 'expected': (Number('2'), 'kilograms') },
    { 'test': r"(2kg)^0", 'expected': Number('1') },
    { 'test': r"3m s^-1", 'expected': (Number('3'), 'meters/second') },
    { 'test': r"3m s^-2", 'expected': (Number('3'), 'meters/second^2') },
    { 'test': r"(4s^2)^0.5", 'expected': (Number('2'), 'seconds') },
    { 'test': r"(27s^3)^(1/3)", 'expected': (Number('3'), 'seconds') },
    { 'test': r"3 / 2s", 'expected': (Number('1.5'), 'hertz') },

    { 'test': r"min([1kg, 2g])", 'expected': (Number('2'), 'grams') },
    { 'test': r"mean([1g, 2kg])", 'expected': (Number('1000.5'), 'grams') },
    { 'test': r"min([2W, 1.5J/s])", 'expected': (Number('1.5'), 'joules/second') },
    { 'test': r"min([1kg, 2kg, 500g])", 'expected': (Number('500'), 'grams') },

    { 'test': r"5 kg m/s^2", 'expected': (Number('5'), 'kilogram meters/second^2') },
    { 'test': r"25 kg m / 5 s^2", 'expected': (Number('5'), 'newtons') },
    { 'test': r"5 (°C/kg/m)*s^2", 'expected': (Number('5'), 'Celsius/newton') },
    { 'test': r"1 m^2/s", 'expected': (Number('1'), 'meter^2/second') },
    { 'test': r"100m/s^2 / (1kN/ 1000000kg)", 'expected': Number('100000') },

    { 'test': r"10N / 5kg", 'expected': (Number('2'), 'meters/second^2') },

    { 'test': r"80 mi/UK gallon", 'expected': (Number('80'), 'miles/UK gallon') },
    { 'test': r"1 / (80 mi/UK gallon)", 'expected': (Number('0.0125'), 'UK gallons/mile') },
    { 'test': r"1 / (80 mi/UK gallon) * 100 miles", 'expected': (Number('1.25'), 'UK gallons') },
    { 'test': r"10km/l", 'expected': (Number('10'), 'kilometers/liter') },
    { 'test': r"10km / 1l", 'expected': (Number('10'), 'millimeters^-2') },
    { 'test': r"1 / (10cm / 1l)", 'expected': (Number('100'), 'centimeters^2') },
    { 'test': r"10kg^20", 'expected': (Number('10'), 'kilograms^20') },

    { 'test': r"6 / 2s", 'expected': (Number('3'), 'hertz') },
    { 'test': r"6 / (2s^2)", 'expected': (Number('3'), 'hertz^2') },
    { 'test': r"6 / (2s^5)", 'expected': (Number('3'), 'hertz^5') },
    { 'test': r"6 / 2Hz", 'expected': (Number('3'), 'seconds') },
    { 'test': r"6 / 2s to Bq", 'expected': (Number('3'), 'becquerels') },
    { 'test': r"2 cd * 3 sr", 'expected': (Number('6'), 'lumens') },
    { 'test': r"2 cd * 3 sr / 4 m^2", 'expected': (Number('1.5'), 'lux') },
    { 'test': r"4 lux * 2 m^2", 'expected': (Number('8'), 'lumens') },
    { 'test': r"4 lm / 2 sr", 'expected': (Number('2'), 'candelas') },
    { 'test': r"10J / 2 kg to Gy", 'expected': (Number('5'), 'grays') },
    { 'test': r"10J / 2 kg to Sv", 'expected': (Number('5'), 'sieverts') },
    { 'test': r"10 mol / 2 s", 'expected': (Number('5'), 'katals') },

    { 'test': r"10A * 3s", 'expected': (Number('30'), 'coulombs') },
    { 'test': r"20W / 4A", 'expected': (Number('5'), 'volts') },
    { 'test': r"20C / 4V", 'expected': (Number('5'), 'farads') },
    { 'test': r"20V / 4A", 'expected': (Number('5'), 'ohms') },
    { 'test': r"1 / 2 ohms", 'expected': (Number('0.5'), 'siemens') },
    { 'test': r"1 / 2 siemens", 'expected': (Number('0.5'), 'ohms') },
    { 'test': r"6V * 2s", 'expected': (Number('12'), 'webers') },
    { 'test': r"8 Wb / 2 m^2", 'expected': (Number('4'), 'teslas') },
    { 'test': r"8 Wb / 2 A", 'expected': (Number('4'), 'henries') },

    { 'test': r"1 / 10s", 'expected': (Number('100'), 'millihertz') },
    { 'test': "a = 1 / 10s\na", 'expected': (Number('100'), 'millihertz') },

    { 'test': r"0.002092531754169369520182468769 seconds^-1 * 0", 'expected': (Number('0'), 'hertz') },

    { 'test': r"1 pint to ml", 'expected': (Number('473.176473'), 'milliliters') },

    { 'test': "tank = 17100\nthruster = 0.486/s\nformat((tank / (3 thruster)))", 'expected': '3 hours, 15 minutes, 28.395061728395061728395061728395 seconds' },

    { 'test': "x = 2 T m^2\nx", 'expected': (Number('2'), 'tesla meters^2') },
    #{ 'test': r"1m/s + 2", 'expected': (Number('3'), 'meters') }, # This should throw error

    { 'test': r"format(1 hour + 23 minutes + 45 seconds)", 'expected': '1 hour, 23 minutes, 45 seconds' },
    { 'test': r"format(61s)", 'expected': '1 minute, 1 second' },
    { 'test': r"format(2 weeks + 3 hour + 23 minutes + 45 seconds)", 'expected': '14 days, 3 hours, 23 minutes, 45 seconds' },
    { 'test': r"format(1 hour + 23 minutes + 0.001 seconds)", 'expected': '1 hour, 23 minutes, 1 millisecond' },
    { 'test': r"format(456765.34533646 s)", 'expected': '5 days, 6 hours, 52 minutes, 45.34533646 seconds' },
    { 'test': r"format(456765.34533646 s, si)", 'expected': '456765.34533646 seconds' },
    { 'test': r"format(456765.34533646 minutes, si)", 'expected': '27405920.7201876 seconds' },
    { 'test': r"format(456765000.34533646 ms, gregorian)", 'expected': '5 days, 6 hours, 52 minutes, 45.00034533646 seconds' },
    { 'test': r"format(0.000000046 ms)", 'expected': '46 picoseconds' },
    { 'test': r"format(1.000000001 ms)", 'expected': '1.000000001 milliseconds' },
    { 'test': r"format(0.001000000001 ms)", 'expected': '1.000000001 microseconds' },
    { 'test': r"format(1000000001 ms, si)", 'expected': '1000000.001 seconds' },
    { 'test': r"format(1000000000 ms, si)", 'expected': '1000000 seconds' },
    { 'test': r"format(1000000000 ms)", 'expected': '11 days, 13 hours, 46 minutes, 40 seconds' },
    { 'test': r"format(456765.345336 ms, si)", 'expected': '456.765345336 seconds' },
    { 'test': r"format(1.543 miles)", 'expected': '1 mile, 955 yards, 2 feet, 0.48 inches' },
    { 'test': r"format(1.543 long tons)", 'expected': '1 long ton, 86 stone, 12 pounds, 5 ounces, 52.5 grains' },
    { 'test': r"format(1.543 short tons)", 'expected': '1 short ton, 1086 pounds' },
    { 'test': r"format(1.54467 short tons)", 'expected': '1 short ton, 1089 pounds, 5 ounces, 192.5 grains' },
    { 'test': r"format(1.543 tons)", 'expected': '1 short ton, 1086 pounds' },
    { 'test': r"format(12345.6789kg)", 'expected': '12 tonnes, 345.6789 kilograms' },
    { 'test': r"format(1234 MB)", 'expected': '1.234 gigabytes' },
    { 'test': r"format(1234000000 bytes)", 'expected': '1.234 gigabytes' },
    { 'test': r"format(1234005000 bytes)", 'expected': '1.234005 gigabytes' },

    { 'test': r"round(2.567s, 2)", 'expected': (Number('2.57'), 'seconds') },

    { 'test': "x = 1\nreset()\nx", 'expected': None },

    { 'test': r"[1, 2, 3]", 'expected': [Number('1'), Number('2'), Number('3')] },
    { 'test': r"[1 .. 3]", 'expected': [Number('1'), Number('2'), Number('3')] },
    { 'test': r"[-3 .. -1]", 'expected': [Number('-3'), Number('-2'), Number('-1')] },
    { 'test': r"[-1 .. -3 step -1]", 'expected': [Number('-1'), Number('-2'), Number('-3')] },
    { 'test': r"[3 .. 1]", 'expected': [Number('3'), Number('2'), Number('1')] },
    { 'test': r"[3 .. 1 step -1]", 'expected': [Number('3'), Number('2'), Number('1')] },
    { 'test': r"[-1 .. -3]", 'expected': [Number('-1'), Number('-2'), Number('-3')] },
    { 'test': r"[1.5 .. 3.5]", 'expected': [Number('1.5'), Number('2.5'), Number('3.5')] },
    { 'test': r"[1.5 .. 3.5 step 0.5]", 'expected': [Number('1.5'), Number('2'), Number('2.5'), Number('3'), Number('3.5')] },
    { 'test': r"[1 .. 4, 9, 14 .. 20 step 2]", 'expected': [Number('1'), Number('2'), Number('3'), Number('4'), Number('9'), Number('14'), Number('16'), Number('18'), Number('20')] },
    { 'test': r"[1 cm, 2 seconds, 3]", 'expected': [(Number('1') , 'centimeter'), (Number('2'), 'seconds'), Number('3')] },

    { 'test': "a = [1, 2, 3]\na", 'expected': [Number('1'), Number('2'), Number('3')] },
    { 'test': "a = [1, 2, 3]\na = [1, 2, 3]\na", 'expected': [Number('1'), Number('2'), Number('3')] },
    { 'test': r"[1, 2, 3] + 4", 'expected': [Number('5'), Number('6'), Number('7')] },
    { 'test': r"abs([-5, 2 * 3, -3 - 4])", 'expected': [Number('5'), Number('6'), Number('7')] },

    { 'test': r"mean([1, 2, 6])", 'expected': Number('3') },
    { 'test': r"mean([1 .. 100])", 'expected': Number('50.5') },
    { 'test': "a=[1 .. 100]\nmean(a)", 'expected': Number('50.5') },
    { 'test': "a=[1cm, 3 feet]", 'expected': [(Number('1'), 'centimeter'), (Number('3'), 'feet')] },
    { 'test': "a=[1cm, 3 feet]\nmean(a)\na", 'expected': [(Number('1'), 'centimeter'), (Number('3'), 'feet')] },

    { 'test': r"[20 cm .. 1 meter step 20 cm]", 'expected': [(Number('20') , 'centimeters'), (Number('40') , 'centimeters'), (Number('60') , 'centimeters'), (Number('80') , 'centimeters'), (Number('100') , 'centimeters')] },

    { 'test': r"concat([1, 2, 3], [4, 5])", 'expected': [Number('1'), Number('2'), Number('3'), Number('4'), Number('5')] },
    { 'test': r"element([1, 2, 3], 2)", 'expected': Number('2') },
    { 'test': r"element([1, 2, 3, 4, 5], [2 .. 4])", 'expected': [Number('2'), Number('3'), Number('4')] },
    { 'test': r"element([1 cm, 2 seconds, 3 metres], 2)", 'expected': (Number('2'), 'seconds') },
    { 'test': r"count([2 .. 6 step 2])", 'expected': Number('3') },
    { 'test': r"sort([4, 2, 3, 1])", 'expected': [Number('1'), Number('2'), Number('3'), Number('4')] },
    { 'test': r"sort([4 cm, 2 meters, 3 feet])", 'expected': [(Number('4'), 'centimeters'), (Number('3'), 'feet'), (Number('2'), 'meters')] },
    { 'test': r"reverse([4, 2, 3, 1])", 'expected': [Number('1'), Number('3'), Number('2'), Number('4')] },
    { 'test': r"min([1 metre, 40 cm])", 'expected': (Number('40'), 'centimeters') },
    { 'test': r"max([40 cm, 1 metre])", 'expected': (Number('1'), 'meter') },

    { 'test': r"min([0, 3, 6], [4, 2, 5])", 'expected': [Number('0'), Number('2'), Number('5')] },
    { 'test': r"min(3, [4, 2, 5])", 'expected': [Number('3'), Number('2'), Number('3')] },
    { 'test': r"min([0, 3, 6], 4)", 'expected': [Number('0'), Number('3'), Number('4')] },
    { 'test': r"min([0, 3, 6], [1, 2, 3], [6, 4, 1])", 'expected': [Number('0'), Number('2'), Number('1')] },
    { 'test': r"min(5, 2, 3, 1, 4)", 'expected': Number('1') },
    { 'test': r"sort(5, 2, 3, 1, 4)", 'expected': [Number('1'), Number('2'), Number('3'), Number('4'), Number('5')] },

    { 'test': r"day_usage = 1", 'expected': Number('1') },

    #{ 'test': "a = 1\nb = [a]\na += 1\nb", 'expected': [Number('2')] },

#    { 'test': r"", 'expected': Number('') },
]

if test != 0:
    tests = [tests[test - 1]]
tester = TestRunner(CalculatorException)
tester.test(c.calculate, tests * times)
