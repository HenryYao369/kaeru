from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html', {'index': True})

def login(request):
    return HttpResponse("goatse")

# egs had a more dynamic way of loading/reading plugins. See virtualnotary if yer curious.
# plugins = []
# import kaeru.plugins.login

# def main(request):
#     return django.shortcuts.render_to_response('index.html', {'index' : True})
# 
# class DirectTemplateView(django.views.generic.TemplateView):
#     # Ugly how this is only used once (ben)
#     extra_context = None
#     def get_context_data(self, **kwargs):
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         if self.extra_context is not None:
#             for key, value in self.extra_context.items():
#                 if callable(value):
#                     context[key] = value()
#                 else:
#                     context[key] = value
#         return context
# 
# def about(request, page):
#     try:
#         if page == 'faq' :
#             context = {'faq': True}
#         elif page == 'about':
#             context = {'people': True}
#         return DirectTemplateView.as_view(template_name = ("%s.html" % page),
#                                           extra_context = context)(request)
#     except django.template.TemplateDoesNotExist:
#         raise django.http.Http404()

