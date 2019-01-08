# Description

A powerful, modular calculator engine written in Python.

Designed to make it easy to add a calculator into another Python application, with the specific features required.

Also has a Qt interface, allowing it to be used as a desktop app. The supported features are aimed at making a tool useful for scientific, engineering or computing work.

# Usage

Requires Linux (probably), Python 3.4+, Qt 5 (not sure specifically which minor version is minimum), PyQt5.

Run the "run" shell script to launch the interface. This can also be symlinked to, for example from /usr/bin.

# To Do

ENGINE
* Unit normalisation - make it possible to configure to use right-most unit as standard rather than left-most

FEATURES
* User defined functions - external files which can be called and passed parameters, last statement in file is the return value for the function
* Dates:
	* Timezones?
	* Adding years/months to dates issue:
		* Date function to increment a particular element of the date, eg dateincrement('2017-01-01', 3, 'year') => '2020-01-01' (also: datedecrement)
		* Alternatively, dateadd checks if the unit is year or month, and number is integer, and increments year/month in that case - too much black magic

OPERATORS
* forceto - changes the units, with no value conversion or unit compatibility checking

FUNCTIONS
* Functions for orbital mechanics
* Function to convert lumens and frequency to watts

UNITS
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
* Questions to look into:
	* Connection between angle and solid angle (solid angle = angle * angle ?)
	* Should systems preference be a feature_option? Also other unitnormaliser options?
	* Can kWh become recognisable? Also all other prefixes

CONSTANTS

GUI
* Functionality:
	* Ability to reorder unit system preference
	* Ability to select features calculator has, screen to customise calculator, if calculator fails to init display error message
	* Show available information for the Insert dialogs:
		* Insert Unit dialog categoried by system (in order of system preference), then dimension
			* Checkbox to hide prefixed units
		* Insert Function / Operator dialogs categoried by category
		* Way of seeing possible inputs for an operator or function - number of inputs, types allowed for each input
	* Dialog that allows editing of feature options
	* Scientific notation number display option
	* Auto-select dark theme if needed

* Usability / quality of life:
	* Remember what file was loaded, display in title, Save saves to it, add Save As
	* Hotkeys:
		* Ctrl+C - clear output
		* Ctrl+N - clear input, unset filename
		* Ctrl+S - save
		* Ctrl+O - open
	* Option to autoformat date results
	* Insert Date - easily add a date into the calculation
	* Option to disable syntax highlighting
	* Option to clear input on execute
	* Tabs

* Stability:
	* Restoring state should be able to cope with exceptions and reset the state if found
	* Auto-save state occasionally

* Performance:
	* When editing input, only statement edited onwards gets reparsed and reexecuted

* Aesthetics and polish:
	* Icon
	* When units are in short form, no space between value and unit in answer display


GENERAL / CODE QUALITY

DOCUMENTATION
