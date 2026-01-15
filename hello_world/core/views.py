from django.shortcuts import render

def index(request):
    context = {
        "title": "Medical Research Database",
    }
    return render(request, "landing.html", context)
