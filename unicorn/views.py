# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('unicorn/index.html', {})

def about(request):
    return render_to_response('unicorn/about.html', {})


def blog(request):
    return render_to_response('unicorn/blog.html', {})