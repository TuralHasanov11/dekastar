# from django.http import HttpRequest
# from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "main/index.html"


class PrivacyPolicyView(TemplateView):
    template_name = "main/privacy-policy.html"
