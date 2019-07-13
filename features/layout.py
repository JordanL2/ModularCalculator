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
    'var',
]

op_map = [
    { '!' },
    { '^', },
    { '=~', '!~' },
    { 'UNIT_MULTIPLY', 'UNIT_DIVIDE' },
    { 'UNIT_ASSIGNMENT' },
    { 'IMPLICIT_MULTIPLY', '*', '/', '%', '*$', '\\' },
    { '+', '-', '+$', '+%', '-%' },
    { '<', '>', '<=', '>=', '<$', '>$', '<=$', '>=$', '<~', '>~', '<=~', '>=~' },
    { '==', '!=', '==$', '!=$', '==~', '!=~' },
    { '&', '|' },
    { '?' },
    { 'to' },
    { '=', '++', '--', '+=', '-=', '*=', '/=', '^=', '%=', '\\=', '||=' },
]

number_caster_map = [
    'decimal',
    'arbitrarybase',
    'binary',
    'hexadecimal',
    'octal',
    'boolean',
    'string',
]
