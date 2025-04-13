import json

def has_permission(user, permission_key):
    if not user.is_authenticated:
        return False
    if getattr(user, "is_admin", False):
        return True
    if not user.permissions:
        return False
    try:
        permission_list = json.loads(user.permissions.permissions)
    except:
        return False

    return permission_key in permission_list
