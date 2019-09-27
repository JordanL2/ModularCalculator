#!/usr/bin/python3


presets = {}

presets['Basic'] = [
    'numerical.basicarithmetic',
    'numerical.decimalnumbers', 
    'structure.operators', 
]

presets['Advanced'] = presets['Basic'] + [
    'nonfunctional.space',
    'numerical.advancedarithmetic', 
    'state.assignment', 
    'state.assignmentoperators', 
    'structure.innerexpressions', 
    'structure.terminator', 
]

presets['Scientific'] = presets['Advanced'] + [
    'numerical.expnumbers',
    'numerical.numericalconstants',
    'numerical.numericalfunctions',
    'numerical.statisticalfunctions',
    'numerical.trigonometryfunctions',
    'state.assignmentfunctions',
    'state.constants',
    'structure.functions',
    'unitdefinitions.allunitdefinitions',
    'unitfunctions.allunitfunctions',
    'units.advancedunitprefixes',
    'units.basicunitprefixes',
    'units.systems',
    'units.unitconstants',
    'units.units',
]

presets['Computing'] = presets['Scientific'] + [
    'boolean.booleanfunctions',
    'boolean.booleans',
    'dates.datefunctions',
    'dates.dateoperators',
    'dates.dates',
    'nonfunctional.comments',
    'numerical.arbitrarybasenumbers',
    'numerical.bases',
    'numerical.binarynumbers',
    'numerical.hexadecimalnumbers',
    'numerical.octalnumbers',
    'strings.regex',
    'strings.stringcomparison',
    'strings.stringfunctions',
    'strings.strings',
    'structure.externalfunctions',
]