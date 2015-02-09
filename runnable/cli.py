"""Helper code for command-line interfaces"""

import argparse

from django import forms

def _run_cli(cls, *args):
    """Handle command line interface invocation of this script"""

    # Create argument parser from fields
    parser = argparse.ArgumentParser(description=cls.__doc__)
    used_prefixes = set("-h") # keep track of -X options used; -h -> help
    for name, field in cls.declared_fields.items():
        _add_argument_from_field(parser, name, field)

    # Parse arguments, instantiate and call script
    args = parser.parse_args(*args)
    instance = cls(args.__dict__)
    result = instance.run()
    print(result)
    return result

def _add_argument_from_field(parser, name, field):
    """
    Call parser.add_argument with the appropriate parameters
    to add this django.forms.Field to the argparse.ArgumentParsers parser.
    """
    # set options name to lowercase variant, remember name for storage
    optname = name.lower()
    if field.required and field.initial is None: # positional argument
        argname = [optname]
    else: # optional argument
        argname = ["--"+optname]
        prefix = "-" + optname[0]
        if prefix not in parser._option_string_actions:
            argname.append("-"+optname[0])
    # determine help text from label, help_text, and default
    helpfields = [x for x in [field.label, field.help_text] if x]
    if field.initial is not None: helpfields.append("Default: {field.initial}".format(**locals()))
    if isinstance(field, forms.ChoiceField):
        if len(field.choices) > 10:
            helpfields.append("(>10 possible values)")
        else:
            helpfields.append("Possible values are %s" % "; ".join("%s (%s)" % (kv) for kv in field.choices))
    elif type(field) in _FIELD_HELP_MAP:
        helpfields.insert(0, _FIELD_HELP_MAP[type(field)])

    help = ". ".join(unicode(f) for f in helpfields)

    # set type OR action_const as extra arguments depending on type
    args = {} # flexible parameters to add_argument
    if isinstance(field, forms.ModelMultipleChoiceField) or isinstance(field, forms.MultipleChoiceField):
        args["nargs"] = '+'
        argname = ['--' + optname] # problem: now the field appears to be optional, but at least it knows which values belong to this argument
    if isinstance(field, forms.BooleanField) and field.initial is not None:
        args["action"] = "store_const"
        args["const"] = not field.initial
    else:
        args["type"] = _argument_type_from_field(field)

    if [name] != argname:
        args["dest"] =  name

    parser.add_argument(*argname, help = help, default=field.initial, metavar=name, **args)


_FIELD_MAP = {
    forms.IntegerField : int,
    forms.BooleanField : bool,
    forms.FileField : lambda fn:  django.core.files.File(open(fn))
    }
_FIELD_HELP_MAP = {
    forms.IntegerField : "(number)",
    forms.FileField : "(filename)",
    }

def _argument_type_from_field(field):
    """Get the proper python type to parse a command line option"""
    for (ftype, type) in _FIELD_MAP.iteritems():
        if isinstance(field, ftype): return type
    return str
