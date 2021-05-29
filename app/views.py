from core.shortcuts import render_template, json_response


def hello(request, name):
    return render_template("index.html", title=f"Hello {name}!")


def json_response_view(request):
    result = {"j": "s", "o": ["n"]}
    return json_response(result)
