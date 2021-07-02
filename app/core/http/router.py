from app.core.errors import Http404


class Router:
    def __init__(self, routes):
        self.routes = routes

    def route(self, path):
        for key, value in self.routes.items():
            try:
                are_matching, kwargs = self._are_paths_matching(key, path)
            except IndexError:
                continue
            else:
                if are_matching:
                    return value, kwargs

        raise Http404

    @staticmethod
    def _are_paths_matching(route, path):
        route, path = route.split("/"), path.split("/")

        if len(route) != len(path):
            return False, None

        kwargs = {}

        for route_part, path_part in zip(route, path):
            if route_part == path_part:
                continue
            else:
                if _is_variable(route_part):
                    kwargs[_get_variable_name(route_part)] = path_part
                else:
                    return False, None
        return True, kwargs


def _is_variable(part):
    return part[0] == "<" and part[-1] == ">"


def _get_variable_name(part):
    return part[1:-1]
