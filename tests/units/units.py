#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *

from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *
from modularcalculator.objects.units import *


class TestUnitsUnits(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"3 meters to feet", 'expected': (Number(1250, 127), 'feet') },
        { 'test': r"3.5 meters to feet", 'expected': (Number(4375, 381), 'feet') },
        { 'test': r"0.035 meters to feet", 'expected': (Number(175, 1524), 'feet') },
        { 'test': r"-0.035 meters to feet", 'expected': (Number(-175, 1524), 'feet') },
        { 'test': r"3.5 feet to meters", 'expected': (Number('1.0668'), 'meters') },
        { 'test': r"35000000 feet to meters", 'expected': (Number('10668000'), 'meters') },
        { 'test': r"123 meters", 'expected': (Number('123'), 'meters') },
        { 'test': r"1 meters + 2 meters", 'expected': (Number('3'), 'meters') },
        { 'test': r"1 meters * 2", 'expected': (Number('2'), 'meters') },
        { 'test': r"6 meters / 2", 'expected': (Number('3'), 'meters') },
        { 'test': r"1 metre", 'expected': (Number('1'), 'meter') },

        { 'test': r"meters * meters", 'expected': UnitPowerList([UnitPower(c.unit_normaliser.get_unit('metre'), Number(2))]) },
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
        { 'test': r"0.004563084645220168834131873146 TW to TW h / yr", 'expected': (Number(999979466119096509240246406516743, 25000000000000000000000000000000), 'terawatt hours/year') },
        { 'test': r"40 TW h / yr to MW", 'expected': (Number(2000000000, 438291), 'megawatts') },
        { 'test': r"40 TW h / yr to W", 'expected': (Number(2000000000000000, 438291), 'watts') },

        { 'test': r"1 kW to J/s", 'expected': (Number('1000'), 'joules/second') },
        { 'test': r"kW to J/s", 'expected': (Number('1000'), 'joules/second') },
        { 'test': r"1 meters^3 to l", 'expected': (Number('1000'), 'liters') },
        { 'test': r"1 kW + 23 J/s", 'expected': (Number('1.023'), 'kilowatts') },
        { 'test': r"1 J/h + 2 kW", 'expected': (Number('7200001'), 'joules/hour') },
        { 'test': r"1l / 10cm^2", 'expected': (Number('1'), 'meter') },
        { 'test': r"1 km J/h + 2 m kW", 'expected': (Number('7201'), 'kilometer joules/hour') },
        { 'test': r"1 km W + 2 m W", 'expected': (Number('1.002'), 'kilometer watts') },
        { 'test': r"1 kW / (100 J/s)", 'expected': Number('10') },
        { 'test': r"10 W s + 23 J", 'expected': (Number('33'), 'watt seconds') },
        { 'test': r"100J / 2W", 'expected': (Number('50'), 'seconds') },
        { 'test': r"(100 W h) / (10 J/s)", 'expected': (Number('10'), 'hours') },
        { 'test': r"1000000 liters / 1 hectare", 'expected': (Number('10'), 'centimeters') },
        { 'test': r"1 hectare * 1 cm", 'expected': (Number('100000'), 'liters') },
        { 'test': r"10 W s / 2J", 'expected': Number('5') },
        { 'test': r"100 mi / 2 knots", 'expected': (Number(100584, 2315), 'hours') },
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
        { 'test': r"10 kg m^2/s^3/W^2", 'expected': (Number('10'), 'kilogram meters^2/(second^3 watt^2)') },

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

        { 'test': r"round(2.567s, 2)", 'expected': (Number('2.57'), 'seconds') },

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
        { 'test': r"1m/s + 2", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator + with parameters: 1 meters^1, seconds^-1, 2 - From unit is not set" } },
        { 'test': """R = 8.31446261815324 J / (Kelvin * moles)
                     volume = 1m^3
                     critical_temp = 33.2K
                     critical_pressure = 1290000 Pa
                     mass = 1kg
                     molar_mass = 0.00100794*2 kg/mol
                     n = (mass / molar_mass)
                     a = (27/64) * (R^2 * critical_temp^2 / critical_pressure)
                     a * n^2 / volume^2""",
             'cast': str,
             'expected': ('6.132100516412516904893858164421', 'kilopascals') },
        { 'test': "(0.001m^3) ^ (7/5)", 'cast': str, 'expected': ('0.000063095734448019324943436014', 'meters^4.2') },
        { 'test': "1g^0.5 * 1kg^0.5", 'cast': str, 'expected': ('31.622776601683793319988935444327', 'grams') },
        { 'test': "2g^1.5 * 4kg^1.5", 'cast': str, 'expected': ('252982.212813470346559911483554617483', 'grams^3') },

        { 'test': "orbitheight = 36000km\nearthmass = 5.97237e24kg\nearthradius = 6378.1km\ngm = G earthmass\norbitradius = earthradius + orbitheight\ntime = 2 pi (orbitradius^3 / gm)^0.5\ntime to hours",
            'cast': str,
            'expected': ('2.411684727174723952983470211019E1', 'hours') },

        { 'test': r"gm = G * 5.97237e24kg", 'expected': (Number('398600751696000'), 'meters^3/second^2') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestUnitsUnits.prepare_tests()

if __name__ == '__main__':
    execute_tests()
