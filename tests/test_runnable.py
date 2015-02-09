from django import forms
from runnable import Runnable
from nose.tools import assert_equal, assert_in, raises, assert_raises
from cStringIO import StringIO
import sys


class SimpleRunnable(Runnable):
    "class docstring"
    string = forms.CharField(help_text="field docstring")
    repeat = forms.IntegerField(initial=1, required=False)
    def call(self, string, repeat=2):
        return string * repeat


def _test_add(a, b):
    return a+b

class ExternalRunnable(Runnable):
    a = forms.IntegerField()
    b = forms.IntegerField()
    target = _test_add


class SomeOtherClass(object):
    @classmethod
    def _test_add(cls, a, b):
        return a+b

class ExternalClassRunnable(Runnable):
    a = forms.IntegerField()
    b = forms.IntegerField()
    target = SomeOtherClass._test_add


def test_bound():
    "Can we call a bound runnable?"
    assert_equal(SimpleRunnable(dict(string="bla", repeat=2)).run(), "blabla")
    assert_equal(SimpleRunnable(dict(string="bla")).run(), "bla")

    assert_equal(ExternalRunnable(dict(a=1, b=2)).run(), 3)
    assert_equal(ExternalClassRunnable(dict(a=1, b=2)).run(), 3)


def test_unbound():
    "Can we call an unbound runnable?"
    assert_equal(SimpleRunnable().call("bla", 1), "bla")
    assert_equal(SimpleRunnable().call("bla", repeat=3), "blablabla")
    assert_equal(SimpleRunnable().call("bla"), "blabla")

    assert_equal(ExternalRunnable().call(a=1, b=2), 3)
    assert_equal(ExternalClassRunnable().call(a=1, b=2), 3)


def test_validation_error():
    "Do we get an exception on calling run on an unbound or invalid runnable?"
    assert_raises(Exception, SimpleRunnable().run)
    assert_raises(Exception, SimpleRunnable(dict(repeat=2)).run)
    assert_raises(Exception, SimpleRunnable(dict(repeat="bla", string="2")).run)


def test_cli():
    "Can we create and call a command line interface"
    assert_equal(SimpleRunnable.run_cli(["bla", "--repeat", "2"]), "blabla")
    assert_equal(SimpleRunnable.run_cli(["bla"]), "bla")


def test_cli_help():
    "Does the CLI help text render?"
    old_stdout, sys.stdout = sys.stdout, StringIO()
    try:
        assert_raises(SystemExit, SimpleRunnable.run_cli, ["--help"])
        help = sys.stdout.getvalue()
        assert_in("class docstring", help)
        assert_in("field docstring", help)
        assert_in("--repeat", help)
    finally:
        sys.stdout = old_stdout


def test_cli_usage():
    "Does the CLI usage / error text render?"
    old_stdout, sys.stderr = sys.stderr, StringIO()
    try:
        assert_raises(SystemExit, SimpleRunnable.run_cli, [])
        help = sys.stderr.getvalue()
        assert_in("usage:", help)
        assert_in("too few arguments", help)
    finally:
        sys.stderr = old_stdout
