# Description

A powerful, modular calculator written in Python.

Designed to make it easy to add a calculator into another Python application, with the specific features required. Adding custom features is possible.

Also has a Qt interface, allowing it to be used as a desktop app. The supported features are aimed at making a tool useful for scientific, engineering or computing work.


# Requirements

* Linux (other operating systems not tested)
* Python 3.4+
* Qt 5 (todo - figure out precisely which minor version is minimum)
* PyQt5


# Usage

## As a Graphical App
Run the "run" shell script to launch the interface. This can also be symlinked to, for example from /usr/bin.

## As a Component in a Python App
Import the ModularCalculator class:
```
from modularcalculator.modularcalculator import ModularCalculator
```

You can initialise the object with the name of a preset, which will auto-install all features associated with the preset:
```
c = ModularCalculator('Advanced')
```
See what presets are available and their features in features/list.py.

Otherwise, initialise an empty ModularCalculator and add the features you want, using each feature's id field.
```
c = ModularCalculator()
c.add_features(['numerical.basicarithmetic', 'numerical.decimalnumbers', 'structure.operators'])
```
Each feature's dependencies will also be installed automatically. The order of the features doesn't matter, if each feature's dependencies and installation order hints have been defined correctly they will be installed in the correct order. Because installation order matters, it is best to install all your features in one call to add_features().

Then, call calculate() with the expression to be calculated. This returns a response object, containing a list of results. Since this is a single statement, there is only one result here.

```
response = c.calculate('2+3')
print(response.results[0].value)
```

These examples are available in examples/basic_integration.py. See examples/advanced_integration.py for a guide to adding custom features.


# To Do

## Engine

## Features
* Dates:
	* Timezones?
	* Adding years/months to dates issue:
		* Date function to increment a particular element of the date, eg dateincrement('2017-01-01', 3, 'year') => '2020-01-01' (also: datedecrement)
		* Alternatively, dateadd checks if the unit is year or month, and number is integer, and increments year/month in that case - too much black magic
* Feature to execute an arbitrary script as a function, with the parameters as command line arguments and STDOUT being the return value
	* Works like user defined functions but with @@ symbol to execute as default
* Ability to alter operator symbols as feature options
* Ability to rename functions as feature options
* Should bitwise not operator only allow positive integers, and throw error if something else?

## Functions
* Display operator/function syntax info on parameter validation error
* Function to remove leading zeros on binary numbers

## Units
* Pressure
	* PSI
	* Atmospheres
* Force
	* Pounds of force
	* Tonnes of force (long, short, metric?)
* Angles:
	Minute of arc
	Second of arc
	Milliradian
* Solid Angles - minutes and seconds
* Connection between angle and solid angle (solid angle = angle * angle ?)
* Can kWh become recognisable? Also all other prefixes, and "mph"
	* possibly a composite unit type eg "kWh" => ['kilowatt', 'hour']
	* allows simplification from the element units into the composite unit, eg "1 kW * 3 h" = "3 kWh"
	* alternatively just add "mph" and "kWh" etc as velocity and energy units, disable simplification to them

## Constants

## Graphical Interface
* Functionality:

* Usability / quality of life:
	* Improve Light theme, it's too dark and high contrast
	* Hotkeys for various insert operations, eg Ctrl+F = Insert Function
	* Check if unit, function, constant, date features are installed when you click their Insert
		* Alternatively, hide these options when features not installed
	* Should unit in answer be coloured same as the syntax highlight colour for units?
	* Option to switch between horizontal and vertical layout

* Stability:
	* Auto-save state occasionally

* Performance:
	* When editing input, check if its possible to reuse later statements from cached result

* Aesthetics and polish:

## Other
* Comment code
* Move to do / bug list to github page
* Add code license - GPL 2 or LGPL 2
* Wiki
* Make flatpak


# Bugs

* Unit normalisation: "1 joule / 1 m^3" gets simplified to "1 pascal" - Even Google has this issue
