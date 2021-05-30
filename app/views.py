from core.shortcuts import json_response, render_template


def hello(request, name):
    return render_template(request, "index.html", title=f"Hello {name}!")


def json_response_view(request):
    result = {"j": "s", "o": ["n"]}
    return json_response(request, result)
