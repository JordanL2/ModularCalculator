# Changelog

## 1.3.0
- Big improvements for alternative-base numbers and scientific notation numbers:
	- Converting a number to an alternative-base number, or scientific notation number, respects the calculator's precision option.
	- Alternative-base numbers and scientific notation numbers now all stored internally as a Number, with 'number_cast' attribute storing a function reference to convert back to its original representation - this is done when casting to a string. This avoids converting between formats multiple times internally, potentially losing precision each time.
- Number casters now includes a reference to the function to reverse the casting to Number.
- Fixing error thrown when throwing a CalculateException.
- Fixing scientific notation number 0E0 being displayed as E0.

## 1.2.2
- Closing file handle in externalfunctions.
- Rewrote test framework to use unittest, now faster, and more coherant as all tests now use same framework.

## 1.2.1
- Precision improvement for Number.log.
- Minor performance improvement for Number.is_integer.

## 1.2.0
- Replaced internal number representiation with new Number class:
	- Stores all numbers as a ratio between two integers, allowing storing fractions (e.g. 1/3) perfectly without rounding errors.
	- Rounds number only when representing it as a string.
	- Can return number in integer+num/den fraction format.

## 1.1.0
- First version after splitting interface to its own repository.