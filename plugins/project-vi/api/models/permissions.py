class Permissions:
    # Base permissions using bit flags
    NONE        = 0
    FILE        = 1 << 0
    SQLITE      = 1 << 1
    # Resered for future use

    OBSIDIAN    = 1 << 6
    # Resered for future use

    MEMORY      = 1 << 11
    # Resered for future use

    USER        = 1 << 16
    # Resered for future use
    
    ADMIN       = (1 << 20)-1

    @staticmethod
    def has_permission(user_permissions: int, required_permission: int) -> bool:
        return (user_permissions & required_permission) == required_permission

    @staticmethod
    def get_permission_names(permissions: int) -> list:
        names = []
        if permissions & Permissions.SQLITE:
            names.append('sqlite')
        if permissions & Permissions.FILE:
            names.append('file')
        if permissions & Permissions.OBSIDIAN:
            names.append('obsidian')
        if permissions & Permissions.MEMORY:
            names.append('memory')
        if permissions & Permissions.USER:
            names.append('user')
        if permissions == Permissions.ADMIN:
            names.append('admin')
        return names
