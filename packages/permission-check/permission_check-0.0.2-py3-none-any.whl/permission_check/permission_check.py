import os
from permission_check.utils import Permission


class PermissionCheck:
    def __init__(self, path):
        self.path = path
        self.stat = os.stat(self.path)
        self.permissions = oct(self.stat.st_mode)[-3:]
        self.owner = Permission(permission=self.permissions[0])
        self.group = Permission(permission=self.permissions[0])
        self.others = Permission(permission=self.permissions[0])
