from django.shortcuts import render


def testhome(request):
	context = {}
	template = "test.html"
	return render(request, template, context)