from functools import wraps
from flask import g, request, url_for

breadcrumbs = {}

def register_breadcrumbs(blueprint, route_key, title, dynamic_callback=None):
    def decorator(func):
        breadcrumbs[route_key] = {"title": title, "url": f"{blueprint.url_prefix or ''}{func.__name__}", "callback": dynamic_callback}

        @wraps(func)
        def wrapped(*args, **kwargs):
            g.breadcrumbs = get_breadcrumbs(blueprint.name)
            return func(*args, **kwargs)
        return wrapped
    return decorator


def get_breadcrumbs(blueprint_name):
    current_path = request.path
    crumbs = []
    for key, value in breadcrumbs.items():
        if value["url"] in current_path:
            crumb = value.copy()
            crumb["url"]= get_breadcrumbs_url(blueprint_name, key)

            if crumb.get("callback"):
                crumb["title"] = crumb["callback"]
            crumbs.append(crumb)
    return crumbs

def get_breadcrumbs_url(blueprint_name, key):
    # blueprint_name: dashboard + key: .user.id
    if ".id" in key:
        req_id = request.view_args["id"]
        url = key.split(".id")
        url = url_for(blueprint_name + url[0] , id=req_id)
    else:
        url = url_for(blueprint_name + key)
    return url