#!/usr/bin/python3

from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *


print("Syntax Error Handling tests:")
c = ModularCalculator('Computing')
hl = SyntaxHighlighter()

tests = [
    { 'test': r"1 2",                   'expected': { 'message': r"Could not parse: 2",                       'pos': 2,  'items': ['1', ' '] } },
    { 'test': r"1 + + 1",               'expected': { 'message': r"Invalid input for operator + - '+'",          'pos': 2,  'items': ['1',' '] } },
    { 'test': r"1+ + 1",                'expected': { 'message': r"Invalid input for operator + - '+'",          'pos': 1,  'items': ['1'] } },
    { 'test': r"+ 1",                   'expected': { 'message': r"Missing left operands for operator +",          'pos': 0,  'items': [] } },
    { 'test': r" + ",                   'expected': { 'message': r"Missing left operands for operator +",          'pos': 1,  'items': [' '] } },
    { 'test': r"+",                     'expected': { 'message': r"Missing left operands for operator +",          'pos': 0,  'items': [] } },
    { 'test': r"1 +",                   'expected': { 'message': r"Missing right operands for operator +",          'pos': 2,  'items': ['1',' '] } },

    { 'test': r"1 + (2 3)",             'expected': { 'message': r"Could not parse: 3)",                      'pos': 7,  'items': ['1',' ','+',' ','(','2',' '] } },
    { 'test': r"1 + (2  3)",            'expected': { 'message': r"Could not parse: 3)",                      'pos': 8,  'items': ['1',' ','+',' ','(','2',' ',' '] } },
    
    { 'test': r"min([1, 2, ''])",         'expected': { 'message': r"Function min parameter 1 must be of type(s) array[number]",   'pos': 0,  'items': [] } },
    { 'test': r"1 + (min([1, 2, '']))",   'expected': { 'message': r"Function min parameter 1 must be of type(s) array[number]",   'pos': 5,  'items': ['1',' ','+',' ','(',], 'next': 'min([1, 2, \'\'])' } },
    { 'test': r"1 + (min([1, 2, 3 +])",   'expected': { 'message': r"Inner expression missing close symbol",    'pos': 4,  'items': ['1',' ','+',' '] } },
    { 'test': r"1 + (min([1, 2, 3 +]))",  'expected': { 'message': r"Missing right operands for operator +",          'pos': 18, 'items': ['1',' ','+',' ','(','min','(','[','1',',',' ','2',',',' ','3',' '], 'next': '+' } },
    { 'test': r"1 + (min([1, 2, 3] +))",  'expected': { 'message': r"Missing right operands for operator +",          'pos': 19, 'items': ['1',' ','+',' ','(','min','(','[','1',',',' ','2',',',' ','3',']',' '], 'next': '+' } },
    { 'test': r"1 + (min([1, 2, (1 2)])", 'expected': { 'message': r"Could not parse: 2)])",                     'pos': 19, 'items': ['1',' ','+',' ','(','min','(','[','1',',',' ','2',',',' ','(','1',' '] } },
    { 'test': r"sort([1, 2, 3], [4, 5, 6])",         'expected': { 'message': r"Cannot pass multiple arrays to an operation that returns an array",   'pos': 0,  'items': [] } },

    { 'test': r"1 / 0",                 'expected': { 'message': r"Could not execute operator / with operands: '1', '0' - Could not execute Operator /",     'pos': 2,  'items': ['1',' '] } },
    { 'test': r"2 + (1 / 0) + 3",       'expected': { 'message': r"Could not execute operator / with operands: '1', '0' - Could not execute Operator /",     'pos': 7,  'items': ['2',' ','+',' ','(','1',' '] } },
    { 'test': "(2 + #comment\n(1 / 0) + 3)",       'expected': { 'message': r"Could not execute operator / with operands: '1', '0' - Could not execute Operator /",      'pos': 17,  'items': ['(','2',' ','+',' ','#comment',"\n",'(','1',' '] } },
    { 'test': r"(2 + (((1 / 0)) + 3))", 'expected': { 'message': r"Could not execute operator / with operands: '1', '0' - Could not execute Operator /",     'pos': 10, 'items': ['(','2',' ','+',' ','(','(','(','1',' '] } },
    { 'test': r"1 + ''",                'expected': { 'message': r"Could not execute operator + with operands: '1', '' - Operator + parameter 2 must be of type(s) number",      'pos': 2,  'items': ['1',' '] } },

    { 'test': r"true then 1 else 2 3",        'expected': { 'message': r"Could not parse: 3",                       'pos': 19, 'items': ['true',' ','then',' ','1',' ','else',' ','2',' '] } },
    { 'test': r"true then 1 2 else 3",        'expected': { 'message': r"Could not parse: 2 else 3",                   'pos': 12,  'items': ['true',' ','then',' ','1',' '] } },
    { 'test': r"false then 1 else (+)",        'expected': { 'message': r"Missing left operands for operator +",          'pos': 19, 'items': ['false',' ','then',' ','1',' ','else',' ','('] } },
    { 'test': r"false then 1 else ( +)",       'expected': { 'message': r"Missing left operands for operator +",          'pos': 20, 'items': ['false',' ','then',' ','1',' ','else',' ','(',' '] } },
    { 'test': r"true then 1 else 2 else 3",      'expected': { 'message': r"Could not execute operator: else",   'pos': 19,  'items': ['true',' ','then',' ','1',' ','else',' ','2',' '] } },
    { 'test': r"true else false then 1 else 2",  'expected': { 'message': r"Could not execute operator: else",    'pos': 5, 'items': ['true',' '] } },
    
    { 'test': r"(1 hectare to 2)^0.5",  'expected': { 'message': r"Could not execute operator to with operands: '1 hectares^1', '2' - Operator to parameter 2 must be of type(s) unit",  'pos': 11, 'items': ['(','1',' ','hectare',' '] } },
    { 'test': r"(1 hectare to 2) ^ 0.5",  'expected': { 'message': r"Could not execute operator to with operands: '1 hectares^1', '2' - Operator to parameter 2 must be of type(s) unit",  'pos': 11, 'items': ['(','1',' ','hectare',' '] } },
    { 'test': "(1 hectare to 2)#comment\n^ 0.5",  'expected': { 'message': r"Could not execute operator to with operands: '1 hectares^1', '2' - Operator to parameter 2 must be of type(s) unit",  'pos': 11, 'items': ['(','1',' ','hectare',' '] } },
    { 'test': "#comment\n(1 hectare to 2) ^ 0.5",  'expected': { 'message': r"Could not execute operator to with operands: '1 hectares^1', '2' - Operator to parameter 2 must be of type(s) unit",  'pos': 20, 'items': ['#comment',"\n",'(','1',' ','hectare',' '] } },
    
    { 'test': "dateadd('2017-01-01', 3)",  'expected': { 'message': r"Function dateadd parameter 2 must have unit dimensions: time^1",  'pos': 0, 'items': [] } },

    { 'test': "(1/0) else",  'expected': { 'message': r"Could not execute operator: else",  'pos': 6, 'items': ['(','1','/','0',')',' '] } },

    { 'test': "f = './tests/externalfunctions/does_not_exist'\n@f(1, 2)", 'expected': { 'exception': ParsingException, 'message': r"Could not read file './tests/externalfunctions/does_not_exist'", 'pos': 47, 'items': ['f',' ','=',' ',"'./tests/externalfunctions/does_not_exist'","\n"] } },
    { 'test': "f = './tests/externalfunctions/ext_func_addition2'\n@f(1, 2)", 'expected': { 'exception': ParsingException, 'message': r"Could not execute operator + with operands: '3', 'None' - Operator + parameter 2 must be of type(s) number", 'pos': 51, 'items': ['f',' ','=',' ',"'./tests/externalfunctions/ext_func_addition2'","\n"] } },

    { 'test': "round((+))",  'expected': { 'message': r"Missing left operands for operator +",  'pos': 7, 'items': ['round','(','('] } },
    { 'test': "(1/0) +",  'expected': { 'message': r"Missing right operands for operator +",  'pos': 6, 'items': ['(','1','/','0',')',' '], 'next': '+' } },
    
    { 'test': "[1, 2 / 0]",  'expected': { 'message': r"Could not execute operator / with operands: '2', '0' - Could not execute Operator /",  'pos': 6, 'items': ['[','1',',',' ','2',' '] } },
    { 'test': "[1, (2 / 0)]",  'expected': { 'message': r"Could not execute operator / with operands: '2', '0' - Could not execute Operator /",  'pos': 7, 'items': ['[','1',',',' ','(','2',' '] } },
    { 'test': "[1 .. 2 / 0 step 2]",  'expected': { 'message': r"Could not execute operator / with operands: '2', '0' - Could not execute Operator /",  'pos': 8, 'items': ['[','1',' ','..',' ','2',' '] } },    
    { 'test': "[1 .. (2 / 0) step 2]",  'expected': { 'message': r"Could not execute operator / with operands: '2', '0' - Could not execute Operator /",  'pos': 9, 'items': ['[','1',' ','..',' ','(','2',' '] } },    
    { 'test': "[1 .. 2 step 2 / 0]",  'expected': { 'message': r"Could not execute operator / with operands: '2', '0' - Could not execute Operator /",  'pos': 15, 'items': ['[','1',' ','..',' ','2',' ','step',' ','2',' '] } },
    { 'test': "[1 .. 2 step (2 / 0)]",  'expected': { 'message': r"Could not execute operator / with operands: '2', '0' - Could not execute Operator /",  'pos': 16, 'items': ['[','1',' ','..',' ','2',' ','step',' ','(','2',' '] } },
    { 'test': "[1 .. 2 step -1]",  'expected': { 'message': r"Can't get from 1 to 2 with step -1",  'pos': 15, 'items': ['[','1',' ','..',' ','2',' ','step',' ','-1'] } },
    { 'test': "[1 step 2]",  'expected': { 'message': r"Parsing error in array",  'pos': 3, 'items': ['[','1',' '] } },
    { 'test': "@mean([",  'expected': { 'message': r"Array missing close symbol",  'pos': 6, 'items': ['@mean','('] } },

    { 'test': "simplefunc = './tests/externalfunctions/simplefunc'\n@simplefunc(@simplefunc(*))",  'expected': { 'message': r"Missing left operands for operator *",  'pos': 76, 'items': ['simplefunc',' ','=',' ',"'./tests/externalfunctions/simplefunc'",'\n','@simplefunc','(','@simplefunc','('] } },

#    { 'test': r"", 'expected': { 'exception': ParsingException, 'message': r"", 'pos': 0, 'items': [] } },
]

failed = []
for num, test in enumerate(tests):
    expr = test['test']
    expected = test['expected']

    try:
        c.calculate(expr)
    except CalculatorException as err:
        try:
            if err.message != expected['message']:
                failed.append({'num': num, 'test': expr, 'stage': 'Exception message', 'expected': expected['message'], 'actual': err.message})
                continue
            if 'next' in expected:
                if err.next != expected['next']:
                    failed.append({'num': num, 'test': expr, 'stage': 'Next', 'expected': expected['next'], 'actual': err.next})
                    continue
            i = err.find_pos(expr)
            if i != expected['pos']:
                failed.append({'num': num, 'test': expr, 'stage': 'Exception position', 'expected': expected['pos'], 'actual': i})
                continue
            statements = hl.highlight_statements(err.statements)
            count = 0
            items = [item for items in statements for item in items]
            for item in items:
                if item[0] != 'default':
                    count += 1
                    if count > len(expected['items']):
                        failed.append({'num': num, 'test': expr, 'stage': 'Exception items', 'expected': expected['items'], 'actual': items})
                        break
                    expecteditem = expected['items'][count - 1]
                    if item[1] != expecteditem:
                        failed.append({'num': num, 'test': expr, 'stage': 'Exception items', 'expected': expected['items'], 'actual': items})
                        break
            else:
                if count != len(expected['items']):
                    failed.append({'num': num, 'test': expr, 'stage': 'Exception items', 'expected': expected['items'], 'actual': items})
        except Exception as err:
            print("Failed on test {} |{}|".format(num + 1, expr))
            raise err
    except Exception as err:
        print("Failed on test {} |{}|".format(num + 1, expr))
        raise err
    else:
        failed.append({'num': num, 'test': expr, 'stage': 'Exception type', 'expected': 'Exception', 'actual': 'No exception'})

if len(failed) > 0:
    print("*** FAILED ***")
    for test in failed:
        print()
        print("        # {0}".format(test['num'] + 1))
        print("    Test: '{0}'".format(test['test']))
        print("   Stage: {0}".format(test['stage']))
        print("Expected: {0}".format(test['expected']))
        print("  Actual: {0}".format(test['actual']))
else:
    print("All tests passed.")
