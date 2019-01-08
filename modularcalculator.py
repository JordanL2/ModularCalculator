#!/usr/bin/python3

from modularcalculator.objects import *
from modularcalculator.numericalengine import NumericalEngine
import modularcalculator.features.layout
import modularcalculator.features.list
from modularcalculator.features.feature import *


class ModularCalculator(NumericalEngine):

    def __init__(self, preset=None):
        super().__init__()

        self.preset_list = modularcalculator.features.list.presets
        self.feature_list = modularcalculator.features.list.feature_list
        self.parser_map = modularcalculator.features.layout.parser_map
        self.op_map = modularcalculator.features.layout.op_map
        self.number_caster_map = modularcalculator.features.layout.number_caster_map

        self.installed_features = set()
        self.features_to_install = set()
        self.feature_options = {}
        if preset is not None:
            self.load_preset(preset)

    def list_presets(self):
        return self.preset_list.keys()

    def load_preset(self, preset):
            self.add_features(self.preset_list[preset])
            self.setup()

    def list_features(self):
        return self.feature_list

    def add_features(self, names, debug=False):
        if isinstance(names, str):
            names = [names]
        
        for name in names:
            self.add_feature_to_be_installed(name)
        
        if debug:
            print("Installing {0} features".format(len(names)))
        for name in names:
            if debug:
                print("Installing {0}".format(name))
            if name in self.installed_features:
                if debug:
                    print("... Skipping {0} as it is already installed".format(name))
            elif name not in self.feature_list:
                raise CalculatorException("Feature {0} not found".format(name))
            else:
                do_befores = self.feature_list[name].after()
                for do_before in do_befores:
                    if do_before not in self.installed_features and do_before in self.features_to_install:
                        if debug:
                            print("... Must install after {0}, installing now".format(do_before))
                        self.add_features(do_before, debug)
                dependencies = self.feature_list[name].dependencies()
                for dependency in dependencies:
                    if dependency not in self.installed_features:
                        if debug:
                            print("... Missing dependency {0}, installing now".format(dependency))
                        self.add_features(dependency, debug)
                self.feature_list[name].install(self)
                self.installed_features.add(name)

    def add_feature_to_be_installed(self, name):
        if name in self.features_to_install:
            return
        self.features_to_install.add(name)
        feature = self.feature_list[name]
        dependencies = feature.dependencies()
        for dependency in dependencies:
            self.add_feature_to_be_installed(dependency)
        if isinstance(feature, MetaFeature):
            for subfeature in feature.subfeatures():
                self.add_feature_to_be_installed(subfeature)

    def add_parser(self, name, ref):
        if self.parser_map is None:
            raise CalculatorException('Can\'t add parser before setting parser_map')
        self.parsers.append({'name': name, 'ref': ref})
        parser_names = dict([(p['name'], p) for p in self.parsers])
        self.parsers = [parser_names[p] for p in self.parser_map if p in parser_names]

    def add_op(self, op, extra=None):
        sym = op.symbol
        if extra is not None:
            for k, v in extra.items():
                if hasattr(op, k):
                    setattr(op, k, v)
                else:
                    raise CalculatorException("Don't recognise operator option {0}".format(k))
        if self.op_map is None:
            raise CalculatorException('Can\'t add operator before setting op_map')
        found = False
        after = set()
        target_prec = None
        for prec in self.op_map:
            if sym in prec:
                target_prec = prec
                found = True
            elif found:
                after = after.union(prec)
        for i, prec in enumerate(self.ops):
            for this_op_sym, this_op_info in prec.items():
                if this_op_sym in target_prec:
                    if op.rtl != this_op_info.rtl:
                        raise CalculatorException("Attempt to insert op {0} with rtl={1} into set where rtl={2}".format(sym, op.rtl, this_op_info.rtl))
                    prec[sym] = op
                    return
                elif this_op_sym in after:
                    self.ops.insert(i, {sym: op})
                    return
        self.ops.append({sym: op})

    def add_number_caster(self, name, ref):
        if self.number_caster_map is None:
            raise CalculatorException('Can\'t add number caster before setting number_caster_map')
        self.number_casters.append({'name': name, 'ref': ref})
        caster_names = dict([(c['name'], c) for c in self.number_casters])
        self.number_casters = [caster_names[c] for c in self.number_caster_map if c in caster_names]
