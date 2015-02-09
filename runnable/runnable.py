import argparse
import types

import django
from django import forms

from .cli import _run_cli

class Runnable(forms.Form):
    """
    Runnable objects are subclasses of a django Form that can be executed.

    - A bound form can be executed using the .run() method
    - An unbound form can be executed using the .call(...) method
    - The class method run_cli() parses sys.argv and calls the method or displays help

    By default, .call calls self.target with the assigned arguments, so a subclass should
    either override call or create a target class variable pointing to an external function
    """

    def __init__(self, *args, **kargs):
        check_django_settings()
        super(Runnable, self).__init__(*args, **kargs)

    def call(self, *args, **kargs):
        """Do the actual work. Override this function or provide a .target attribute"""
        # note: we assume that target points to a function
        # since python automatically converts class members to methods
        # we need to revert the method to a function - if it is from this class
        target = self.target
        if isinstance(target, types.MethodType) and target.im_class == self.__class__:
            target = target.im_func
        return target(*args, **kargs)

    def run(self):
        """Run a bound Runnable"""
        if not self.is_bound:
            raise ValueError("Cannot call run() on an unbound Runnable")
        if not self.is_valid():
            raise ValueError(repr(self.errors))
        return self.call(**self.cleaned_data)

    def clean(self):
        """Populate non-required field from initial values"""
        for f, val in self.cleaned_data.iteritems():
            if val is None and f not in self.data:
                self.cleaned_data[f] = self.fields[f].initial

    @classmethod
    def run_cli(cls, *args):
        """Handle command line interface invocation of this script"""
        check_django_settings()
        return _run_cli(cls, *args)


def check_django_settings():
    """
    Provide default django settings if no settings are specified
    Note: This will silently ignore improperly configured settings
    """
    try:
        django.setup()
    except django.core.exceptions.ImproperlyConfigured:
        django.conf.settings.configure()
        django.setup()
