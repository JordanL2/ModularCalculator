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
* Multi-thread calculation?
	* Multiple runners, external processes running listening to a queue that gives them jobs
	* Number of runners set with argument when Calculator is created
	* Runners initialised on Calculator creation
	* execute method:
		* Loop to execute operands passes each operand into the input queue
		* When all operand results are received from the output queue, execute continues
			* Since the output queue can be getting read by runners, we need a way of reading the output queue without removing the results, only removing results that are relevant to the execute instance
			* Or, should each execute instance have its own output queue? Placed inside the job as a reference
	* Runner:
		* Listens to input queue for jobs
		* When a job received, splits a interpreter thread to execute the operand
		* When thread finishes, it writes the result to the output queue

## Features
* Date timezones

## Functions

## Units

## Constants

## Graphical Interface
* Functionality:

* Usability / quality of life:
	* Save state any time it changes

* Stability:

* Performance:

* Aesthetics and polish:

## Other
* Comment code
* Move to do / bug list to github page
* Add code license - Apache 2 or LGPL 2
* Wiki
* Make flatpak


# Bugs

* Unit normalisation: "1 joule / 1 m^3" gets simplified to "1 pascal" - Even Google has this issue
