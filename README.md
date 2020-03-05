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
