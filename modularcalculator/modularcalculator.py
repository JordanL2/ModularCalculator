#!/usr/bin/python3

from modularcalculator.objects import *
from modularcalculator.numericalengine import NumericalEngine
import modularcalculator.features.layout
import modularcalculator.features.presets
from modularcalculator.features.feature import *

import sys
import inspect
import pkgutil
import os.path
from importlib import import_module


class ModularCalculator(NumericalEngine):

    def __init__(self, preset=None):
        super().__init__()

        self.feature_list = {}
        self.scan_feature_files()

        self.preset_list = modularcalculator.features.presets.presets
        self.parser_map = modularcalculator.features.layout.parser_map
        self.op_map = modularcalculator.features.layout.op_map

        self.installed_features = set()
        self.features_to_install = set()
        self.feature_options = {}
        if preset is not None:
            self.load_preset(preset)

    def scan_feature_files(self):
        topdir = os.path.dirname(__file__) + '/features'
        for dirname in next(os.walk(topdir))[1]:
            feature_category = dirname.split('/')[-1]
            if feature_category != '__pycache__':
                for (_, module_name, _) in pkgutil.iter_modules([topdir + '/' + dirname]):
                    package_name = 'modularcalculator.features.' + feature_category
                    self.import_feature(module_name, package_name)

    def import_feature(self, module_name, package_name=None):
        ids = []
        if package_name is not None:
            imported_module = import_module("{}.{}".format(package_name, module_name))
        else:
            imported_module = import_module(module_name)
        for i in dir(imported_module):
            feature = getattr(imported_module, i)
            if inspect.isclass(feature) and issubclass(feature, Feature):
                try:
                    feature_id = feature.id()
                    self.feature_list[feature_id] = feature
                    ids.append(feature_id)
                except Exception:
                    pass
        return ids

    def import_feature_file(self, file_path):
        feature_dir = os.path.dirname(file_path)
        feature_module = os.path.basename(file_path)
        feature_module = os.path.splitext(feature_module)[0]
        if feature_dir not in sys.path:
            sys.path.append(feature_dir)
        return self.import_feature(feature_module)

    def list_presets(self):
        return self.preset_list.keys()

    def load_preset(self, preset):
        self.install_features(self.preset_list[preset])

    def list_features(self):
        return self.feature_list

    def install_features(self, names, debug=False, skipMissing=False):
        if isinstance(names, str):
            names = [names]

        if skipMissing:
            new_names = []
            for name in names:
                if name in self.feature_list:
                    new_names.append(name)
                elif debug:
                    print("!!! Skipping {} as it is not found !!!".format(name))
            names = new_names

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
                        self.install_features(do_before, debug)
                dependencies = self.feature_list[name].dependencies()
                for dependency in dependencies:
                    if dependency not in self.installed_features:
                        if debug:
                            print("... Missing dependency {0}, installing now".format(dependency))
                        self.install_features(dependency, debug)
                self.feature_list[name].install(self)
                self.installed_features.add(name)
        self.setup()

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

    def add_number_type(self, number_type):
        self.number_types[number_type.name()] = number_type
