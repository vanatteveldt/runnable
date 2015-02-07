# Runnable

A 'Runnable' is an object that has a well-defined interface and run() method. 
This makes it easy to create a command-line interface, web form, or web service for the object.

Installation
----

Usage 
----

Defining a 'Runnable'
====

Every runnable uses a django Form to define the arguments that it requires. 
For example, lets make a runnable that allows us to add two numbers. 
The form is quite simple:

```{python}
from django import forms
class AdderForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()
```

With this form, there are three equivalent ways to define a 'runnable'. You can subclass the runnable:

```{python}
from runnable import Runnable
class Adder(Runnable):
    form = AdderForm
    def run(self, a, b):
      return a+b
```
    
Alternatively, you can make a class that points to both the form and the method:
```{python}
from runnable import Runnable
def add(a, b):
    return a+b

class Adder(Runnable):
    form = AdderForm
    run = add
```

Or finally, you can call the create_runnable function with the form and target as arguments:
```{python}
from runnable import create_runnable
def add(a, b):
    return a+b
Adder = Runnable(target=add, form=AdderForm)
```


