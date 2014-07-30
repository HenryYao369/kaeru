from django.conf.urls.defaults import *
from django.conf import settings

# Gun had a more dynamic way of loading/reading plugins. See virtualnotary if yer curious.
# plugins = []
import kaeru.plugins.login

def main(request):
    return django.shortcuts.render_to_response('index.html', {'index' : True})

class DirectTemplateView(django.views.generic.TemplateView):
    # Ugly how this is only used once (ben)
    extra_context = None
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value
        return context

def about(request, page):
    try:
        if page == 'faq' :
            context = {'faq': True}
        elif page == 'about':
            context = {'people': True}
        return DirectTemplateView.as_view(template_name = ("%s.html" % page),
                                          extra_context = context)(request)
    except django.template.TemplateDoesNotExist:
        raise django.http.Http404()

# def dispatch(request, sourcename, methodname, arg1=None):
#     if sourcename not in plugins:
#         raise django.http.Http404()
# 
#     m = getattr(django.utils.importlib.import_module("vnotary.plugins."+sourcename), methodname)
#     if arg1 is not None:
#          return m(request, arg1, False)
#     else:
#          return m(request, False)
#     try:
#         # XXX this needs to be around the whole thing
#         pass
#     except Exception as e:
#         raise Http500()

