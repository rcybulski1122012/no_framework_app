from app.core.http.response import HttpResponse


def test_dunder_str_contains_all_data():
    headers = {"Content-Type": "text/html", "Content-Length": 10}
    response = HttpResponse("HTTP/1.1", 200, "OK", headers, "*" * 10)
    expected = (
        "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 10\n\n**********\n"
    )

    assert str(response) == expected


def test_dunder_str_with_lack_of_body_and_headers():
    response = HttpResponse("HTTP/1.0", 404, "Not Found")
    expected = "HTTP/1.0 404 Not Found\n"

    assert str(response) == expected
