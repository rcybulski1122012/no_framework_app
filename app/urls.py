from app.views import *

urls = {
    "/hello/<name>": hello,
    "/json": json_response_view,
}
