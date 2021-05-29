from core.templates import render_template


def index(request, name):
    return render_template("index.html", title=f"Hello {name}!")
