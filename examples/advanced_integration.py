#!/usr/bin/python3

from modularcalculator.modularcalculator import ModularCalculator
from modularcalculator.features.feature import Feature
from modularcalculator.objects.items import *
#from modularcalculator.examples.examplecustomfeature import ExampleCustomFeature

from decimal import *


# An example custom feature, which interprets 'hello' as the number 123


# Make an empty calculator
c = ModularCalculator()

# Import the custom feature to its list of known features
feature_ids = c.import_feature('examplecustomfeature', 'modularcalculator.examples')
print("ID of imported feature:", feature_ids)
# If the file is outside of the python path, you could import it this way instead:
# c.import_feature_file('/path/to/examplecustomfeature.py')

# Install the feature, and basic arithmetic operators
c.install_features(feature_ids + ['numerical.basicarithmetic'])

# The feature interprets 'hello' as the number 123, so this should return 126
response = c.calculate('hello+3')
print(response.results[0].value)
