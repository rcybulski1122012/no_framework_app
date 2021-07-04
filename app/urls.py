from app.auth.views import create_user_view, login_user_view
from app.todolists.views import create_todolist_view, todolists_list_view
from app.views import index, static

urls = {
    "/": index,
    "/static/<file_name>": static,
    "/register": create_user_view,
    "/login": login_user_view,
    "/todolists": todolists_list_view,
    "/create_todolist": create_todolist_view,
}
