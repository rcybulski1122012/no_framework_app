from app.auth.views import create_user_view, login_user_view
from app.todolists.tasks_views import tasks_list_view
from app.todolists.todolists_views import (create_todolist_view,
                                           delete_todolist_view,
                                           edit_todolist_view,
                                           todolists_list_view,
                                           update_todolist_view)
from app.views import index, static

urls = {
    "/": index,
    "/static/<file_name>": static,
    "/register": create_user_view,
    "/login": login_user_view,
    "/todolists": todolists_list_view,
    "/create_todolist": create_todolist_view,
    "/delete_todolist/<id_>": delete_todolist_view,
    "/edit_todolist/<id_>": edit_todolist_view,
    "/update_todolist/<id_>": update_todolist_view,
    "/tasks/<todolist_id>": tasks_list_view,
}
