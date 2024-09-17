#!/usr/bin/python3


TYPE_CHECKING_OPTIONS = {
    'enabled': False
}



def enable_type_checking():
    TYPE_CHECKING_OPTIONS['enabled'] = True

def disable_type_checking():
    TYPE_CHECKING_OPTIONS['enabled'] = False


def assert_class(clas, *vals):
    if not TYPE_CHECKING_OPTIONS['enabled']:
        return
    for val in vals:
        if type(clas) in (list, tuple):
            for t in clas:
                if isinstance(val, t):
                    break
            else:
                assert False, "'{}' not in {}".format(val.__class__.__name__, ', '.join(["'" + t.__name__ + "'" for t in clas]))
        else:
            assert isinstance(val, clas), "'{}' != '{}'".format(val.__class__.__name__, clas.__name__)

def assert_optional_class(clas, *vals):
    if not TYPE_CHECKING_OPTIONS['enabled']:
        return
    for val in vals:
        if val is not None:
            if type(clas) in (list, tuple):
                for t in clas:
                    if isinstance(val, t):
                        break
                else:
                    assert False, "'{}' not in {}".format(val.__class__.__name__, ', '.join(["'" + t.__name__ + "'" for t in clas]))
            else:
                assert isinstance(val, clas), "'{}' != '{}'".format(val.__class__.__name__, clas.__name__)

def assert_classname(classname, *vals):
    if not TYPE_CHECKING_OPTIONS['enabled']:
        return
    for val in vals:
        if type(classname) in (list, tuple):
            for cn in classname:
                if val.__class__.__name__ == cn:
                    break
            else:
                assert False, "'{}' not in {}".format(val.__class__.__name__, ', '.join(["'" + str(t) + "'" for t in classname]))
        else:
            assert val.__class__.__name__ == classname, "'{}' != '{}'".format(val.__class__.__name__, classname)

def assert_optional_classname(classname, *vals):
    if not TYPE_CHECKING_OPTIONS['enabled']:
        return
    for val in vals:
        if val is not None:
            if type(classname) in (list, tuple):
                for cn in classname:
                    if val.__class__.__name__ == cn:
                        break
                else:
                    assert False, "'{}' not in {}".format(val.__class__.__name__, ', '.join(["'" + str(t) + "'" for t in classname]))
            else:
                assert val.__class__.__name__ == classname, "'{}' != '{}'".format(val.__class__.__name__, classname)
