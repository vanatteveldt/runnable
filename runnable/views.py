from django.views.generic.edit import FormMixin, ProcessFormView
from django.views.generic.base import TemplateResponseMixin

class RunnableMixin(FormMixin):
    """
    Django View mixin that is based on a Runnable
    It is based on a FormMixin, so provide the Runnable with
    form_class or by overriding get_form_class()
    """

    def run(self, form):
        """
        Run the runnable and provide the result in self.result.
        Since the default FormMixin behaviour is to redirect on success,
        you might need to store the result in e.g. the session as well.
        """
        self.form = form
        self.result =  self.form.run()

    def form_valid(self, form):
        self.run(form)
        return super(RunnableMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add the form_class and (if available) result to the template context
        """
        context = super(RunnableMixin, self).get_context_data(**kwargs)
        form = self.get_form_class()
        context['form_class'] = form
        context['form_doc'] = form.__doc__
        context['form_name'] = form.__name__
        if hasattr(self, 'result'):
            context['result'] = self.result
        return context


class RunnableView(ProcessFormView, RunnableMixin, TemplateResponseMixin):
    """
    Django View to process a runnable using a template
    Specify form_class, template_name, and success_url class attributes
    (or override form_valid, but call run(form) if you override)
    """
