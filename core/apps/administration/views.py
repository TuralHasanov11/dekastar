# from django.http import HttpRequest
# from django.shortcuts import render
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "administration/index.html"

