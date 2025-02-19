# Changelog

## 1.5.0
- sp_sph_harm has been removed for now as it's deprecated in scipy
- Number Types and Unit Systems are actual objects, rather than strings
- Additional input number type checks (e.g. positivity, integers) for operations that need them
- Fixed the number type of an operation never being decimal, even when the first parameter is decimal
- Fixed setting the number of decimal places before decimal point, correctly sets the total precision so we don't have more decimal places than total size

## 1.4.5
- Fixed crash for operation exceptions with non-decimal numbers

## 1.4.4
- Fixed 'as' operator dropping value's unit
- exp function has increased precision
- fact, lcd, gcd functions and << and >> operators correctly check input for negativity/non-integers

## 1.4.3
- Fixed log function behaviour when base is non-integer, zero, or negative
- Refactored operator/function error messages to make them more helpful and consistent
- Fixed crash when fetching an element from an array that is an exception

## 1.4.2
- Fixed trigonometry functions not returning Number instances

## 1.4.1
- Fixed floor and ceil functions when passing the places parameter
- Fixed round, floor and ceil functions with percentage numbers
- Fixed boolean conditional operators returning value with unit, when inputs have units

## 1.4.0
- New functions: lcm (lowest common multiple) and gcd (greatest common divisor).
- Added many special functions from SciPy.
- Added 'as' operator that can convert a value's numerical type (e.g. convert to binary).
- Added percentage numerical type.
- Added inline functions.
- Nested arrays are now possible.
- Function names can now contain, but not start with, a number.
- Fixed a unit assignment not having higher precedence than multiply.

## 1.3.1
- Fixed displaying units - divisor in brackets now used closed bracket properly.
- Fixed potential infinite loop when simplifying units. This has slightly reduced the kind of simplification that can be done.
- Unit powers can now be non-integers.
- Assignment operators (e.g. +=) now return the new value of the variable.
- Number power operator is now more accurate when given negative powers.

## 1.3.0
- Ceil and floor functions now also have an optional places parameter.
- Numerical Engine has `number_set_rounding` function to set rounding mode, use names of `decimal` rounding modes.
- Numerical Engine has `number_size_set` function to set the maximum size of numbers (before decimal point).
- Number casters now includes a reference to the function to reverse the casting to Number.
- Various improvements for alternative-base numbers and scientific notation numbers:
	- Converting a number to an alternative-base number, or scientific notation number, respects the calculator's precision option.
	- Alternative-base numbers and scientific notation numbers now all stored internally as a Number, with 'number_cast' attribute storing a function reference to convert back to its original representation - this is done when casting to a string. This avoids converting between formats multiple times internally, potentially losing precision each time.
	- Fixing scientific notation number 0E0 being displayed as E0.
	- Round, ceil and floor functions now all work properly with alternative-base numbers when specifying places.
	- Binary numbers now preserve their width (e.g. number of leading zeros) on creation and after a bitwise operation, all other operations discard the width afterwards.
- Fixing error thrown when throwing a CalculateException.

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
