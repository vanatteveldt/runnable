"""
A 'Runnable' is a subclass of django Form with a run() method.
Since this defines both the arguments in a standard way (using the Form) and a way to call it, it can be used for creating plugins or easily exposing functionality to an external interface such as a web service, web form, or command line script.

See the help text for the Runnable class and/or http://github.com/vanatteveldt/runnable
"""


from .runnable import Runnable
