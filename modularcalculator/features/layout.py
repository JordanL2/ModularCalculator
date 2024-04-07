#!/usr/bin/python3


parser_map = [
    'terminator',
    'space',
    'comment',
    'boolean',
    'number_bin',
    'number_oct',
    'number_hex',
    'number_arbbase',
    'numberexp',
    'percentagenumber',
    'number',
    'operator',
    'string',
    'ext_function',
    'function',
    'function_param',
    'function_end',
    'inner_expr',
    'inner_expr_end',
    'constant',
    'units',
    'unitsystems',
    'numericalrepresentation',
    'array',
    'array_range',
    'array_step',
    'array_param',
    'array_end',
    'var',
]

op_map = [
    { '^', },
    { 'not', '~' },
    { '=~', '!~' },
    { 'UNIT_MULTIPLY', 'UNIT_DIVIDE' },
    { 'UNIT_ASSIGNMENT' },
    { 'IMPLICIT_MULTIPLY' },
    { '*', '/', '%', '*$', '\\' },
    { '+', '-', '+$', '+%', '-%' },
    { '<<', '>>' },
    { '<', '>', '<=', '>=', '<$', '>$', '<=$', '>=$', '<~', '>~', '<=~', '>=~' },
    { '==', '!=', '==$', '!=$', '==~', '!=~' },
    { '&' },
    { '|', '^^' },
    { 'and', 'or', 'xor' },
    { 'then' },
    { 'to', 'as' },
    { '=', '++', '--', '+=', '-=', '*=', '/=', '^=', '%=', '\\=', '||=' },
]

number_type_map = [
    'decimal',
    'arbitrarybase',
    'binary',
    'hexadecimal',
    'octal',
    'scientific',
    'boolean',
    'percentage',
]
