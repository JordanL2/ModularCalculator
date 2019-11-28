#!/usr/bin/python3

from modularcalculator.tests.testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *

import argparse


print("ScientificCalculator tests:")
c = ModularCalculator('Scientific')
hl = SyntaxHighlighter()

parser = argparse.ArgumentParser()
parser.add_argument('times', metavar='n', nargs='?', type=int, default=1, help='number of times to run the tests')
args = parser.parse_args()
times = args.times

tests = [
    { 'test': 'min([1, 2, 3])', 'expected': Decimal('1') },
    { 'test': '1 + (( min([ 2, -1,  3 ])))', 'expected': Decimal('0') },
    { 'test': '( min([ min([4,5,6]), min([2,8,9]),  min([3,7,8]) ]))', 'expected': Decimal('2') },
    { 'test': '( min([ min([4,5,6]), min([2,8,9])+1,  min([3,7,8]) ]))', 'expected': Decimal('3') },
    { 'test': '( min([ min([4,5,6]), 2 * min([2,8,9]) - 3,  min([3,7,8]) ]))', 'expected': Decimal('1') },
    { 'test': '( min([ min([4,5,6]), 2 * min([2,8,9])-3,  min([3,7,8]) ]))', 'expected': Decimal('1') },
    { 'test': '(min([min([4,5,6]),((2 * min([2,8,9])-(3 + 1))),min([3,7,8]) ]))', 'expected': Decimal('0') },
    
    { 'test': r"abs(-4)", 'expected': Decimal('4') },
    { 'test': r"fact(5)", 'expected': Decimal('120') },
    { 'test': r"log(5)", 'expected': Decimal('1.609437912434100281799942422367') },
    { 'test': r"log(5, 10)", 'expected': Decimal('0.698970004336018746471381746233') },
    
    { 'test': r"max([3, 5, 7])", 'expected': Decimal('7') },
    { 'test': r"mean([2, 3, 5, 6])", 'expected': Decimal('4') },
    { 'test': r"median([6, 1, 9])", 'expected': Decimal('6') },
    { 'test': r"mode([1, 1, 2, 4])", 'expected': Decimal('1') },
    { 'test': r"stdev([1, 2, 3, 4])", 'expected': Decimal('1.290994448735805628393088466594') },
    { 'test': r"sum([1, 2, 3, 4])", 'expected': Decimal('10') },
    { 'test': r"sum(([10]))", 'expected': Decimal('10') },
    { 'test': r"sum([(10)])", 'expected': Decimal('10') },
    { 'test': r"sum([(1), 2, 3])", 'expected': Decimal('6') },
    { 'test': r"sum(([(1), 2, 3]))", 'expected': Decimal('6') },
    { 'test': r"sum([1, (2), 3])", 'expected': Decimal('6') },
    { 'test': r"sum([1, 2, (3)])", 'expected': Decimal('6') },
    { 'test': r"sum([1, 2, (3) + 2])", 'expected': Decimal('8') },
    { 'test': r"sum([(1), 2, 3 + 2])", 'expected': Decimal('8') },
    { 'test': r"sum([ (10) ])", 'expected': Decimal('10') },
    { 'test': r"sum( [ (10) ] )", 'expected': Decimal('10') },
    { 'test': r"sum([( 10 )])", 'expected': Decimal('10') },
    { 'test': r"sum( [( 10 )] )", 'expected': Decimal('10') },
    
    { 'test': r"floor(1.4)", 'expected': Decimal('1') },
    { 'test': r"floor(1.5)", 'expected': Decimal('1') },
    { 'test': r"ceil(1.4)", 'expected': Decimal('2') },
    { 'test': r"ceil(1.5)", 'expected': Decimal('2') },
    { 'test': r"round(1.1)", 'expected': Decimal('1') },
    { 'test': r"round(1.5)", 'expected': Decimal('2') },
    { 'test': r"round(1.11, 1)", 'expected': Decimal('1.1') },
    { 'test': r"round(1.16, 1)", 'expected': Decimal('1.2') },

    { 'test': r"dec(1.234e1)", 'expected': Decimal('12.34') },
    { 'test': r"dec(1.234e10)", 'expected': Decimal('12340000000') },
    { 'test': r"dec(1.234e2)", 'expected': Decimal('123.4') },
    { 'test': r"dec(1.234e0)", 'expected': Decimal('1.234') },
    { 'test': r"dec(1.234e-1)", 'expected': Decimal('0.1234') },
    { 'test': r"dec(1.234e-2)", 'expected': Decimal('0.01234') },
    { 'test': r"dec(5.97237e24 kg)", 'expected': (Decimal('5972370000000000000000000'), 'kilograms') },
    { 'test': r"1.23e2 + 1.2e1", 'expected': '1.35E2' },
    { 'test': r"1.23e2kg + 1.2e1kg", 'expected': ('1.35E2', 'kilograms') },
    { 'test': r"dec(1.23e2 + 1.2e1)", 'expected': Decimal('135') },

    { 'test': r"scientific(123.456789)", 'expected': '1.23456789E2' },
    { 'test': r"scientific(123.45678900000)", 'expected': '1.23456789E2' },
    { 'test': r"scientific(12345678900000)", 'expected': '1.23456789E13' },
    { 'test': r"scientific(123.456789, 3)", 'expected': '1.235E2' },
    { 'test': r"scientific(123.456789, 5)", 'expected': '1.23457E2' },
    { 'test': r"scientific(0.000123456789, 5)", 'expected': '1.23457E-4' },
    { 'test': r"scientific(123.456789 miles)", 'expected': ('1.23456789E2', 'miles') },

    { 'test': r"3 meters to feet", 'expected': (Decimal('9.842519685039370078740157480315'), 'feet') },
    { 'test': r"3.5 meters to feet", 'expected': (Decimal('11.482939632545931758530183727034'), 'feet') },
    { 'test': r"0.035 meters to feet", 'expected': (Decimal('0.11482939632545931758530183727'), 'feet') },
    { 'test': r"-0.035 meters to feet", 'expected': (Decimal('-0.11482939632545931758530183727'), 'feet') },
    { 'test': r"3.5 feet to meters", 'expected': (Decimal('1.0668'), 'meters') },
    { 'test': r"35000000 feet to meters", 'expected': (Decimal('10668000'), 'meters') },
    { 'test': r"-200 °C to K", 'expected': (Decimal('73.15'), 'kelvin') },
    { 'test': r"20 °C to °F", 'expected': (Decimal('68'), 'Fahrenheit') },
    { 'test': r"20000 °C to °F", 'expected': (Decimal('36032'), 'Fahrenheit') },
    { 'test': r"68 °F to °C", 'expected': (Decimal('20'), 'Celsius') },

    { 'test': r"123 meters", 'expected': (Decimal('123'), 'meters') },
    { 'test': r"1 meters + 2 meters", 'expected': (Decimal('3'), 'meters') },
    { 'test': r"1 meters * 2", 'expected': (Decimal('2'), 'meters') },
    { 'test': r"6 meters / 2", 'expected': (Decimal('3'), 'meters') },
    { 'test': r"1 metre", 'expected': (Decimal('1'), 'meter') },
    { 'test': r"1 meter + 23 cm", 'expected': (Decimal('1.23'), 'meters') },
    { 'test': r"1 meter + 23 µm", 'expected': (Decimal('1.000023'), 'meters') },
    { 'test': r"1 meter + 23 nm", 'expected': (Decimal('1.000000023'), 'meters') },
    { 'test': r"1K + 1K", 'expected': (Decimal('2'), 'kelvin') },
    { 'test': r"1°C + 1°C", 'expected': (Decimal('2'), 'Celsius') },
    { 'test': r"1K + 1°C", 'expected': (Decimal('2'), 'kelvin') },
    { 'test': r"1°C + 1K", 'expected': (Decimal('2'), 'Celsius') },

    { 'test': r"2 meters * 3 meters", 'expected': (Decimal('6'), 'meters^2') },
    { 'test': r"20 meters / 5 meters", 'expected': Decimal('4') },
    { 'test': r"12 meters * 3°C", 'expected': (Decimal('36'), 'meter Celsius') },
    { 'test': r"2 meters * 3 meters * 4 meters", 'expected': (Decimal('24'), 'meters^3') },
    { 'test': r"(2 meters * 3 meters * 4 meters) / 2 meters", 'expected': (Decimal('12'), 'meters^2') },
    { 'test': r"(2 meters * 3 meters * 4 meters) / (2 meters * 4 meters)", 'expected': (Decimal('3'), 'meters') },
    { 'test': r"(2 meters * 3 meters) / 2 feet", 'expected': (Decimal('9.842519685039370078740157480315'), 'meters') },
    { 'test': r"(2 meters * 3 meters * 4 meters) / (5 feet * 6 feet)", 'expected': (Decimal('8.61112833336777784666680444472'), 'meters') },
    { 'test': r"2 m/s", 'expected': (Decimal('2'), 'meters/second') },
    { 'test': r"2 m/s + 3 m/s", 'expected': (Decimal('5'), 'meters/second') },
    { 'test': r"2 m/s + 3 miles/hour", 'expected': (Decimal('3.34112'), 'meters/second') },
    { 'test': r"2 m/s to miles/hour", 'expected': (Decimal('4.473872584108804581245526127416'), 'miles/hour') },
    { 'test': r"2 m^2", 'expected': (Decimal('2'), 'meters^2') },
    { 'test': r"2 m^3", 'expected': (Decimal('2'), 'meters^3') },
    { 'test': r"2 m^2 to feet^2", 'expected': (Decimal('21.5278208334194446166670111118'), 'feet^2') },

    { 'test': r"40 * (meters*meters) / (seconds*seconds) * 2 meters", 'expected': (Decimal('80'), 'meters^3/second^2') },
    { 'test': r"12 meters °C / s", 'expected': (Decimal('12'), 'meter Celsius/second') },
    { 'test': r"0.625 meters/(second^2 celsius) * 4°C", 'expected': (Decimal('2.5'), 'meters/second^2') },
    { 'test': r"40 TW h / yr", 'expected': (Decimal('40'), 'terawatt hours/year') },
    { 'test': r"compact(40 TW h / yr)", 'expected': (Decimal('4.563178344980846058896942898668'), 'gigawatts') },
    { 'test': r"0.004563084645220168834131873146 TW to TW h / yr", 'expected': (Decimal('39.99917864476386036960985626067'), 'terawatt hours/year') },
    { 'test': r"40 TW h / yr to MW", 'expected': (Decimal('4563.17834498084605889694289866778'), 'megawatts') },
    { 'test': r"40 TW h / yr to W", 'expected': (Decimal('4563178344.980846058896942898667780082183'), 'watts') },

    { 'test': r"1 kW to J/s", 'expected': (Decimal('1000'), 'joules/second') },
    { 'test': r"1 meters^3 to l", 'expected': (Decimal('1000'), 'liters') },
    { 'test': r"1 kW + 23 J/s", 'expected': (Decimal('1.023'), 'kilowatts') },
    { 'test': r"1 J/h + 2 kW", 'expected': (Decimal('7200001'), 'joules/hour') },
    { 'test': r"1l / 10cm", 'expected': (Decimal('100'), 'centimeters^2') },
    { 'test': r"1l / 10cm^2", 'expected': (Decimal('1'), 'meter') },
    { 'test': r"1 km J/h + 2 m kW", 'expected': (Decimal('7201'), 'kilometer joules/hour') },
    { 'test': r"1 km W + 2 m W", 'expected': (Decimal('1.002'), 'kilometer watts') },
    { 'test': r"1 kW / (100 J/s)", 'expected': Decimal('10') },
    { 'test': r"10 W s + 23 J", 'expected': (Decimal('33'), 'watt seconds') },
    { 'test': r"100J / 2W", 'expected': (Decimal('50'), 'seconds') },
    { 'test': r"(100 W h) / (10 J/s)", 'expected': (Decimal('10'), 'hours') },
    { 'test': r"1000000 liters / 1 hectare", 'expected': (Decimal('10'), 'centimeters') },
    { 'test': r"(1l) / (10cm °C)", 'expected': (Decimal('100'), 'centimeters^2/Celsius') },
    { 'test': r"1 hectare * 1 cm", 'expected': (Decimal('100000'), 'liters') },
    { 'test': r"10 W s / 2J", 'expected': Decimal('5') },
    { 'test': r"100 mi / 2 knots", 'expected': (Decimal('43.448812095032397408207343412527'), 'hours') },
    { 'test': r"100 nmi / 2 knots", 'expected': (Decimal('50'), 'hours') },
    { 'test': r"0 nmi / 2 knots", 'expected': (Decimal('0'), 'hours') },
    { 'test': r"(100 mi) / (2 mi/h)", 'expected': (Decimal('50'), 'hours') },
    { 'test': r"1 UK pint + 2 UK pints", 'expected': (Decimal('3'), 'UK pints') },
    { 'test': r"1 liter + 2 UK pints", 'expected': (Decimal('2.1365225'), 'liters') },
    { 'test': r"1N + 2kg m/s/s", 'expected': (Decimal('3'), 'newtons') },
    { 'test': r"2 gee * 10 s", 'expected': (Decimal('196.133'), 'meters/second') },
    { 'test': r"10W to kg m^2 s^-3", 'expected': (Decimal('10'), 'kilogram meters^2/second^3') },
    { 'test': r"10 kg m^2/s^3 to J/s", 'expected': (Decimal('10'), 'joules/second') },
    { 'test': r"10 kg m^2/s^3", 'expected': (Decimal('10'), 'kilogram meters^2/second^3') },
    { 'test': r"20 kg m^2 / 2s^3", 'expected': (Decimal('10'), 'watts') },

    { 'test': r"1 kW / 100 J/s", 'expected': Decimal('10') },
    { 'test': r"1 GRAM to kg", 'expected': (Decimal('0.001'), 'kilograms') },
    { 'test': r"(2kg)^1", 'expected': (Decimal('2'), 'kilograms') },
    { 'test': r"(2kg)^0", 'expected': Decimal('1') },
    { 'test': r"3m s^-1", 'expected': (Decimal('3'), 'meters/second') },
    { 'test': r"3m s^-2", 'expected': (Decimal('3'), 'meters/second^2') },
    { 'test': r"(4s^2)^0.5", 'expected': (Decimal('2'), 'seconds') },
    { 'test': r"(27s^3)^(1/3)", 'expected': (Decimal('3'), 'seconds') },
    { 'test': r"3 / 2s", 'expected': (Decimal('1.5'), 'hertz') },

    { 'test': r"min([1kg, 2g])", 'expected': (Decimal('0.002'), 'kilograms') },
    { 'test': r"mean([1g, 2kg])", 'expected': (Decimal('1000.5'), 'grams') },
    { 'test': r"min([2W, 1.5J/s])", 'expected': (Decimal('1.5'), 'watts') },
    { 'test': r"min([1kg, 2kg, 500g])", 'expected': (Decimal('0.5'), 'kilograms') },
    
    { 'test': r"5 kg m/s^2", 'expected': (Decimal('5'), 'kilogram meters/second^2') },
    { 'test': r"25 kg m / 5 s^2", 'expected': (Decimal('5'), 'newtons') },
    { 'test': r"5 (°C/kg/m)*s^2", 'expected': (Decimal('5'), 'Celsius/newton') },
    { 'test': r"1 m^2/s", 'expected': (Decimal('1'), 'meter^2/second') },
    
    { 'test': r"10N / 5kg", 'expected': (Decimal('2'), 'meters/second^2') },
    
    { 'test': r"80 mi/UK gallon", 'expected': (Decimal('80'), 'miles/UK gallon') },
    { 'test': r"1 / (80 mi/UK gallon)", 'expected': (Decimal('0.0125'), 'UK gallons/mile') },
    { 'test': r"1 / (80 mi/UK gallon) * 100 miles", 'expected': (Decimal('1.25'), 'UK gallons') },
    { 'test': r"10km/l", 'expected': (Decimal('10'), 'kilometers/liter') },
    { 'test': r"10km / 1l", 'expected': (Decimal('10'), 'millimeters^-2') },
    { 'test': r"1 / (10cm / 1l)", 'expected': (Decimal('100'), 'centimeters^2') },
    { 'test': r"10kg^20", 'expected': (Decimal('10'), 'kilograms^20') },

    { 'test': r"6 / 2s", 'expected': (Decimal('3'), 'hertz') },
    { 'test': r"6 / (2s^2)", 'expected': (Decimal('3'), 'hertz^2') },
    { 'test': r"6 / (2s^5)", 'expected': (Decimal('3'), 'hertz^5') },
    { 'test': r"6 / 2Hz", 'expected': (Decimal('3'), 'seconds') },
    { 'test': r"6 / 2s to Bq", 'expected': (Decimal('3'), 'becquerels') },
    { 'test': r"2 cd * 3 sr", 'expected': (Decimal('6'), 'lumens') },
    { 'test': r"2 cd * 3 sr / 4 m^2", 'expected': (Decimal('1.5'), 'lux') },
    { 'test': r"4 lux * 2 m^2", 'expected': (Decimal('8'), 'lumens') },
    { 'test': r"4 lm / 2 sr", 'expected': (Decimal('2'), 'candelas') },
    { 'test': r"10J / 2 kg to Gy", 'expected': (Decimal('5'), 'grays') },
    { 'test': r"10J / 2 kg to Sv", 'expected': (Decimal('5'), 'sieverts') },
    { 'test': r"10 mol / 2 s", 'expected': (Decimal('5'), 'katals') },
    
    { 'test': r"10A * 3s", 'expected': (Decimal('30'), 'coulombs') },
    { 'test': r"20W / 4A", 'expected': (Decimal('5'), 'volts') },
    { 'test': r"20C / 4V", 'expected': (Decimal('5'), 'farads') },
    { 'test': r"20V / 4A", 'expected': (Decimal('5'), 'ohms') },
    { 'test': r"1 / 2 ohms", 'expected': (Decimal('0.5'), 'siemens') },
    { 'test': r"1 / 2 siemens", 'expected': (Decimal('0.5'), 'ohms') },
    { 'test': r"6V * 2s", 'expected': (Decimal('12'), 'webers') },
    { 'test': r"8 Wb / 2 m^2", 'expected': (Decimal('4'), 'teslas') },
    { 'test': r"8 Wb / 2 A", 'expected': (Decimal('4'), 'henries') },

    { 'test': r"1 pint to ml", 'expected': (Decimal('473.176473'), 'milliliters') },
    
    { 'test': "tank = 17100\nthruster = 0.486/s\nformat((tank / (3 thruster)))", 'expected': '3 hours, 15 minutes, 28.395061728395061728395061728395 seconds' },
    
    { 'test': "x = 2 T m^2\nx", 'expected': (Decimal('2'), 'tesla meters^2') },
    #{ 'test': r"1m/s + 2", 'expected': (Decimal('3'), 'meters') }, # This should throw error
        
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
    { 'test': r"format(1.543 long tonnes)", 'expected': '1 long tonne, 86 stone, 12 pounds, 5 ounces, 52.5 grains' },
    { 'test': r"format(1.543 short tonnes)", 'expected': '1 short tonne, 1086 pounds' },
    { 'test': r"format(1.54467 short tonnes)", 'expected': '1 short tonne, 1089 pounds, 5 ounces, 192.5 grains' },
    { 'test': r"format(12345.6789kg)", 'expected': '12 tonnes, 345.6789 kilograms' },
    { 'test': r"format(1234 MB)", 'expected': '1.234 gigabytes' },
    { 'test': r"format(1234000000 bytes)", 'expected': '1.234 gigabytes' },
    { 'test': r"format(1234005000 bytes)", 'expected': '1.234005 gigabytes' },
    
    { 'test': r"round(2.567s, 2)", 'expected': (Decimal('2.57'), 'seconds') },
    
    { 'test': "x = 1\nreset()\nx", 'expected': None },

    { 'test': r"[1, 2, 3]", 'expected': [Decimal('1'), Decimal('2'), Decimal('3')] },
    { 'test': r"[1 .. 3]", 'expected': [Decimal('1'), Decimal('2'), Decimal('3')] },
    { 'test': r"[1.5 .. 3.5]", 'expected': [Decimal('1.5'), Decimal('2.5'), Decimal('3.5')] },
    { 'test': r"[1.5 .. 3.5 step 0.5]", 'expected': [Decimal('1.5'), Decimal('2'), Decimal('2.5'), Decimal('3'), Decimal('3.5')] },
    { 'test': r"[1 .. 4, 9, 14 .. 20 step 2]", 'expected': [Decimal('1'), Decimal('2'), Decimal('3'), Decimal('4'), Decimal('9'), Decimal('14'), Decimal('16'), Decimal('18'), Decimal('20')] },
    { 'test': r"[1 cm, 2 seconds, 3]", 'expected': [(Decimal('1') , 'centimeter'), (Decimal('2'), 'seconds'), Decimal('3')] },

    { 'test': "a = [1, 2, 3]\na", 'expected': [Decimal('1'), Decimal('2'), Decimal('3')] },
    { 'test': "a = [1, 2, 3]\na = [1, 2, 3]\na", 'expected': [Decimal('1'), Decimal('2'), Decimal('3')] },
    { 'test': r"[1, 2, 3] + 4", 'expected': [Decimal('5'), Decimal('6'), Decimal('7')] },
    { 'test': r"abs([-5, 2 * 3, -3 - 4])", 'expected': [Decimal('5'), Decimal('6'), Decimal('7')] },

    { 'test': r"mean([1, 2, 6])", 'expected': Decimal('3') },
    { 'test': r"mean([1 .. 100])", 'expected': Decimal('50.5') },
    { 'test': "a=[1 .. 100]\nmean(a)", 'expected': Decimal('50.5') },

    { 'test': r"[20 cm .. 1 meter step 20 cm]", 'expected': [(Decimal('20') , 'centimeters'), (Decimal('40') , 'centimeters'), (Decimal('60') , 'centimeters'), (Decimal('80') , 'centimeters'), (Decimal('100') , 'centimeters')] },

    { 'test': r"concat([1, 2, 3], [4, 5])", 'expected': [Decimal('1'), Decimal('2'), Decimal('3'), Decimal('4'), Decimal('5')] },
    { 'test': r"element([1, 2, 3], 2)", 'expected': Decimal('2') },
    { 'test': r"element([1, 2, 3, 4, 5], [2 .. 4])", 'expected': [Decimal('2'), Decimal('3'), Decimal('4')] },

    #{ 'test': "a = 1\nb = [a]\na += 1\nb", 'expected': [Decimal('2')] },

#    { 'test': r"", 'expected': Decimal('') },
]

tester = TestRunner(CalculatorException)
tester.test(c.calculate, tests * times)
