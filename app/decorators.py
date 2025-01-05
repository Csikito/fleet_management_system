import json
from functools import wraps
from flask import g, request, url_for, abort
from flask_login import current_user


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
    home_crumb = {
        "title": "Home",
        "url": url_for(f"{blueprint_name}.dashboard")
    }
    crumbs.append(home_crumb)
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


def permission_required(permission_key):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            permissions = json.loads(current_user.permissions.permissions) or {}
            if not permission_key in permissions:
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator
