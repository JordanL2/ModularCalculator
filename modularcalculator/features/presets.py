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
    'arrays.arrays',
    'arrays.arrayfunctions',
    'numerical.decimalfunction',
    'numerical.numericalrepresentation',
    'numerical.expnumbers',
    'numerical.percentagenumbers',
    'numerical.numericalconstants',
    'numerical.numericalfunctions',
    'numerical.specialfunctions',
    'numerical.statisticalfunctions',
    'numerical.trigonometryfunctions',
    'state.assignmentfunctions',
    'state.constants',
    'structure.functions',
    'unitdefinitions.allunitdefinitions',
    'units.advancedunitprefixes',
    'units.basicunitprefixes',
    'units.systems',
    'units.unitconstants',
    'units.unitfunctions',
    'units.units',
    'units.unitsymbols',
]

presets['Computing'] = presets['Scientific'] + [
    'boolean.booleans',
    'numerical.bitwiseoperators',
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
    'strings.stringarrayfunctions',
    'strings.stringcomparison',
    'strings.stringfunctions',
    'strings.strings',
    'structure.externalfunctions',
]
