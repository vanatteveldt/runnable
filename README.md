# Runnable

A 'Runnable' is a subclass of django Form with a run() method. 
Since this defines both the arguments in a standard way (using the Form) and a way to call it, it can be used for creating plugins or easily exposing functionality to an external interface such as a web service, web form, or command line script. 

Installation
====

You can directly install runnable using pip from the github repository: 

```{bash}
pip install git+git://github.com/vanatteveldt/runnable
```

Usage 
====

Simple Runnable example
----

The following code defines a trivial 'Adder' Runnable:

```{python}
from runnable import Runnable
from django import forms

class Adder(Runnable):
  a = forms.IntegerField()
  b = forms.IntegerField()
  def call(self, a, b):
    return a + b
```

Using a Runnable from python
----

Like a django form, a Runnable object can be created with the form arguments (in which case it is bound) or without any arguments. 
A bound Runnable can be called using the no-arguments `.run()` method.
So, the Adder defined above can be used as follows:

```{python}
a = Adder(dict(a=1, b=2))
if a.is_valid():
  result = a.run()
```

An (unbound) Runnable can also be called using the `.call(**kargs)` method, where the arguments should be provided in the method call.

```{python}
result = Adder().call(a=1, b=2)
```

Note that calling `.call` does not necessarily instantiate the form, the arguments for `.call()` can be more flexible than the arguments in the form.  

Using a Runnable from the command-line 
----

Since a Runnable knows what kind of arguments it needs, it can easily create an interface on the command line or web. 

For a command-line call, simply call `.run_cli()` class method in the script:

```{python}
from django import forms
from runnable import Runnable

class Adder(Runnable):
    """Simple runnable script that adds two numbers"""
    first = forms.IntegerField(help_text="The first number")
    second = forms.IntegerField(initial=1, help_text="An optional second number")

    def call(self, first, second):
        return first + second

if __name__ == '__main__':
  Adder.run_cli()
```

This will create a command line interface as expected:

```{sh}
$ python adder.py
usage: adder.py [-h] [--second second] first
adder.py: error: too few arguments

$ python adder.py --help
usage: adder.py [-h] [--second second] first

Simple runnable script that adds two numbers

positional arguments:
  first                 (number). The first number

optional arguments:
  -h, --help            show this help message and exit
  --second second, -s second
                        (number). An optional second number. Default: 1
$ python adder.py 13
14
$ python adder.py --second 4 13
17
$ python adder.py --second 4 notanumber
usage: adder.py [-h] [--second second] first
adder.py: error: argument first: invalid int value: 'notanumber'
```


Using a Runnable as a django view
----

runnable.views provides a RunnableMixin and RunnableView (inheriting from FormMixin and ProcessFormView+TemplateResponseMixin, respectively) that make it easy to create a simple web page to access the functionality of a Runnable.

For example, if we have the following view:

```{python}
from django import forms
from runnable import Runnable
from runnable.views import RunnableView

class Duplicator(Runnable):
    """This is an extremely useful Runnable that allows you to duplicate arbitrary integers"""
    a = forms.IntegerField(help_text="This is the number that will be duplicated")
    def call(self, a):
        return a*2

class TestView(RunnableView):
    template_name = "template.html"
    form_class = Duplicator
    def form_valid(self, form):
        """Prevent default redirection"""
        self.run(form)
        return self.form_invalid(form)
```

And a template like:

```{python}
<html>
 <head>
  <link href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet" />
 </head>
 <body>
  <div class="container">
   <div class="jumbotron" style="margin-top: 2em">
    <h1>{{form_name}}</h1>
    <p>{{form_doc}}</p>
    <form action='#' method='POST'>
     <table>
      {{form.as_table}}
      <tr><td /><td><input type='submit'></td></tr>
     </table>
    </form>
{% if result %}
    <hr/>
    <h2>The result is: <strong>{{result}}</strong></h2>
{% endif %}
   </div>
  </div>
 </body>
</html>
```

Will yield a view with a form that works as expected, performing validation and (in this case) rendering the result below the form:

![Runnable Result](http://i.imgur.com/nWvleU1.png)

Defining a 'Runnable'
----

Essentially, a Runnable is a django form with a function to be invoked.
This function can be specified in two ways, either by pointing to an external function
or by overriding the call method:

```
class PlusOne(Runnable):
  a = forms.IntegerField()
  def call(self, a):
    return a + 1
    
def external_plus(a): 
  return a + 2
  
class PlusTwo(Runnable)
  a = forms.IntegerField()
  target = external_plus
```
