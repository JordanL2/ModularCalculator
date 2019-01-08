#!/usr/bin/python3


# TEMPLATE

# from modularcalculator.features.feature import Feature

# class ***Feature(Feature):

#     def id():
#         return ''

#     def category():
#         return ''

#     def title():
#         return ''

#     def desc():
#         return ''

#     def dependencies():
#         return []

#     @classmethod
#     def install(cls, calculator):

class Feature:

    def id():
        raise Exception("Override this method")

    def category():
        raise Exception("Override this method")

    def title():
        raise Exception("Override this method")

    def desc():
        raise Exception("Override this method")

    def dependencies():
        raise Exception("Override this method")

    def after():
        return []

    @classmethod
    def install(cls, calculator):
        raise Exception("Override this method")


# TEMPLATE

# from modularcalculator.features.feature import MetaFeature

# class ***MetaFeature(MetaFeature):

#     def id():
#         return ''

#     def category():
#         return ''

#     def title():
#         return ''

#     def desc():
#         return ''

#     def dependencies():
#         return []

#     def subfeatures():
#         return []

class MetaFeature(Feature):

    @classmethod
    def install(cls, calculator):
        calculator.add_features(cls.subfeatures())
        
    def subfeatures():
        raise Exception("Override this method")
