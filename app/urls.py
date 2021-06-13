from app.auth.views import create_user_view, login_user_view

urls = {"/register": create_user_view, "/login": login_user_view}
