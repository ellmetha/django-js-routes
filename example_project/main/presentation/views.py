from django.views.generic import TemplateView


class HomeView(TemplateView):
    """ Main home view class. """

    template_name = 'home.html'
