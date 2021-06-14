from app.auth.views import create_user_view, login_user_view
from app.todolists.views import todolists_list_view

urls = {
    "/register": create_user_view,
    "/login": login_user_view,
    "/users/<user_id>/todolists": todolists_list_view,
}
