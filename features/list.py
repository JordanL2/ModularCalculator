#!/usr/bin/python3

import modularcalculator.features.boolean.booleanfunctions
import modularcalculator.features.boolean.booleans

import modularcalculator.features.dates.datefunctions
import modularcalculator.features.dates.dateoperators
import modularcalculator.features.dates.dates

import modularcalculator.features.nonfunctional.comments
import modularcalculator.features.nonfunctional.space

import modularcalculator.features.numerical.advancedarithmetic
import modularcalculator.features.numerical.arbitrarybasenumbers
import modularcalculator.features.numerical.bases
import modularcalculator.features.numerical.basicarithmetic
import modularcalculator.features.numerical.binarynumbers
import modularcalculator.features.numerical.decimalnumbers
import modularcalculator.features.numerical.expnumbers
import modularcalculator.features.numerical.hexadecimalnumbers
import modularcalculator.features.numerical.numericalconstants
import modularcalculator.features.numerical.numericalfunctions
import modularcalculator.features.numerical.octalnumbers
import modularcalculator.features.numerical.statisticalfunctions
import modularcalculator.features.numerical.trigonometryfunctions

import modularcalculator.features.state.assignment
import modularcalculator.features.state.assignmentfunctions
import modularcalculator.features.state.assignmentoperators
import modularcalculator.features.state.constants

import modularcalculator.features.strings.regex
import modularcalculator.features.strings.stringcomparison
import modularcalculator.features.strings.stringfunctions
import modularcalculator.features.strings.strings

import modularcalculator.features.structure.externalfunctions
import modularcalculator.features.structure.functions
import modularcalculator.features.structure.innerexpressions
import modularcalculator.features.structure.operators
import modularcalculator.features.structure.terminator

import modularcalculator.features.unitdefinitions.allunitdefinitions
import modularcalculator.features.unitdefinitions.absorbeddose
import modularcalculator.features.unitdefinitions.acceleration
import modularcalculator.features.unitdefinitions.angle
import modularcalculator.features.unitdefinitions.area
import modularcalculator.features.unitdefinitions.capacitance
import modularcalculator.features.unitdefinitions.catalyticactivity
import modularcalculator.features.unitdefinitions.data
import modularcalculator.features.unitdefinitions.distance
import modularcalculator.features.unitdefinitions.electricalconductance
import modularcalculator.features.unitdefinitions.electricalpotential
import modularcalculator.features.unitdefinitions.electriccharge
import modularcalculator.features.unitdefinitions.electriccurrent
import modularcalculator.features.unitdefinitions.energy
import modularcalculator.features.unitdefinitions.equivalentdose
import modularcalculator.features.unitdefinitions.force
import modularcalculator.features.unitdefinitions.frequency
import modularcalculator.features.unitdefinitions.illuminance
import modularcalculator.features.unitdefinitions.inductance
import modularcalculator.features.unitdefinitions.luminousflux
import modularcalculator.features.unitdefinitions.luminousintensity
import modularcalculator.features.unitdefinitions.magneticflux
import modularcalculator.features.unitdefinitions.magneticfluxdensity
import modularcalculator.features.unitdefinitions.mass
import modularcalculator.features.unitdefinitions.power
import modularcalculator.features.unitdefinitions.pressure
import modularcalculator.features.unitdefinitions.radioactivity
import modularcalculator.features.unitdefinitions.resistance
import modularcalculator.features.unitdefinitions.solidangle
import modularcalculator.features.unitdefinitions.substance
import modularcalculator.features.unitdefinitions.temperature
import modularcalculator.features.unitdefinitions.time
import modularcalculator.features.unitdefinitions.velocity
import modularcalculator.features.unitdefinitions.volume

import modularcalculator.features.unitfunctions.allunitfunctions
import modularcalculator.features.unitfunctions.generalunitfunctions
import modularcalculator.features.unitfunctions.orbitalmechanicsfunctions

import modularcalculator.features.units.systems
import modularcalculator.features.units.unitconstants
import modularcalculator.features.units.units
import modularcalculator.features.units.basicunitprefixes
import modularcalculator.features.units.advancedunitprefixes


feature_list = dict([(f.id(), f) for f in [

    modularcalculator.features.boolean.booleanfunctions.BooleanFunctionsFeature,
    modularcalculator.features.boolean.booleans.BooleansFeature,

    modularcalculator.features.dates.datefunctions.DateFunctionsFeature,
    modularcalculator.features.dates.dateoperators.DateOperatorsFeature,
    modularcalculator.features.dates.dates.DatesFeature,

    modularcalculator.features.nonfunctional.comments.CommentsFeature,
    modularcalculator.features.nonfunctional.space.SpaceFeature,

    modularcalculator.features.numerical.advancedarithmetic.AdvancedArithmeticFeature,
    modularcalculator.features.numerical.arbitrarybasenumbers.ArbitraryBaseFeature,
    modularcalculator.features.numerical.bases.BasesFeature,
    modularcalculator.features.numerical.basicarithmetic.BasicArithmeticFeature,
    modularcalculator.features.numerical.binarynumbers.BinaryNumbersFeature,
    modularcalculator.features.numerical.decimalnumbers.DecimalNumbersFeature,
    modularcalculator.features.numerical.expnumbers.ExpNumbersFeature,
    modularcalculator.features.numerical.hexadecimalnumbers.HexadecimalNumbersFeature,
    modularcalculator.features.numerical.numericalconstants.NumericalConstantsFeature,
    modularcalculator.features.numerical.numericalfunctions.NumericalFunctionsFeature,
    modularcalculator.features.numerical.octalnumbers.OctalNumbersFeature,
    modularcalculator.features.numerical.statisticalfunctions.StatisticalFunctionsFeature,
    modularcalculator.features.numerical.trigonometryfunctions.TrigonometryFunctionsFeature,

    modularcalculator.features.state.assignment.AssignmentFeature,
    modularcalculator.features.state.assignmentfunctions.AssignmentFunctionsFeature,
    modularcalculator.features.state.assignmentoperators.AssignmentOperatorsFeature,
    modularcalculator.features.state.constants.ConstantsFeature,

    modularcalculator.features.strings.regex.RegexFeature,
    modularcalculator.features.strings.stringcomparison.StringComparisonFeature,
    modularcalculator.features.strings.stringfunctions.StringFunctionsFeature,
    modularcalculator.features.strings.strings.StringsFeature,

    modularcalculator.features.structure.externalfunctions.ExternalFunctionsFeature,
    modularcalculator.features.structure.functions.FunctionsFeature,
    modularcalculator.features.structure.innerexpressions.InnerExpressionsFeature,
    modularcalculator.features.structure.operators.OperatorsFeature,
    modularcalculator.features.structure.terminator.TerminatorFeature,

    modularcalculator.features.unitdefinitions.allunitdefinitions.AllUnitDefinitionsMetaFeature,
    modularcalculator.features.unitdefinitions.absorbeddose.AbsorbedDoseUnitFeature,
    modularcalculator.features.unitdefinitions.acceleration.AccelerationUnitFeature,
    modularcalculator.features.unitdefinitions.angle.AngleUnitFeature,
    modularcalculator.features.unitdefinitions.area.AreaUnitFeature,
    modularcalculator.features.unitdefinitions.capacitance.CapacitanceUnitFeature,
    modularcalculator.features.unitdefinitions.catalyticactivity.CatalyticActivityUnitFeature,
    modularcalculator.features.unitdefinitions.data.DataUnitFeature,
    modularcalculator.features.unitdefinitions.distance.DistanceUnitFeature,
    modularcalculator.features.unitdefinitions.electricalconductance.ElectricalConductanceUnitFeature,
    modularcalculator.features.unitdefinitions.electricalpotential.ElectricalPotentialUnitFeature,
    modularcalculator.features.unitdefinitions.electriccharge.ElectricChargeUnitFeature,
    modularcalculator.features.unitdefinitions.electriccurrent.ElectricCurrentUnitFeature,
    modularcalculator.features.unitdefinitions.energy.EnergyUnitFeature,
    modularcalculator.features.unitdefinitions.equivalentdose.EquivalentDoseUnitFeature,
    modularcalculator.features.unitdefinitions.force.ForceUnitFeature,
    modularcalculator.features.unitdefinitions.frequency.FrequencyUnitFeature,
    modularcalculator.features.unitdefinitions.illuminance.IlluminanceUnitFeature,
    modularcalculator.features.unitdefinitions.inductance.InductanceUnitFeature,
    modularcalculator.features.unitdefinitions.luminousflux.LuminousFluxUnitFeature,
    modularcalculator.features.unitdefinitions.luminousintensity.LuminousIntensityUnitFeature,
    modularcalculator.features.unitdefinitions.magneticflux.MagneticFluxUnitFeature,
    modularcalculator.features.unitdefinitions.magneticfluxdensity.MagneticFluxDensityFeature,
    modularcalculator.features.unitdefinitions.mass.MassUnitFeature,
    modularcalculator.features.unitdefinitions.power.PowerUnitFeature,
    modularcalculator.features.unitdefinitions.pressure.PressureUnitFeature,
    modularcalculator.features.unitdefinitions.radioactivity.RadioactivityUnitFeature,
    modularcalculator.features.unitdefinitions.resistance.ResistanceUnitFeature,
    modularcalculator.features.unitdefinitions.solidangle.SolidAngleUnitFeature,
    modularcalculator.features.unitdefinitions.substance.SubstanceUnitFeature,
    modularcalculator.features.unitdefinitions.temperature.TemperatureUnitFeature,
    modularcalculator.features.unitdefinitions.time.TimeUnitFeature,
    modularcalculator.features.unitdefinitions.velocity.VelocityUnitFeature,
    modularcalculator.features.unitdefinitions.volume.VolumeUnitFeature,
    
    modularcalculator.features.unitfunctions.allunitfunctions.AllUnitFunctionsMetaFeature,
    modularcalculator.features.unitfunctions.generalunitfunctions.GeneralUnitFunctionsFeature,
    modularcalculator.features.unitfunctions.orbitalmechanicsfunctions.OrbitalMechanicsFunctionsFeature,
    
    modularcalculator.features.units.advancedunitprefixes.AdvancedUnitPrefixesFeature,
    modularcalculator.features.units.basicunitprefixes.BasicUnitPrefixesFeature,
    modularcalculator.features.units.systems.UnitSystemsFeature,
    modularcalculator.features.units.unitconstants.UnitConstantsFeature,
    modularcalculator.features.units.units.UnitsFeature,

]])


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
