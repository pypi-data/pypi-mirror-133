class Permission:
    def __init__(self, permission):
        self.permission = int(permission)

    def has_read(self):
        if self.has_all() or self.permission in (4, 6, 5):
            return True
        return False

    def has_write(self):
        if self.has_all() or self.permission in (2, 6, 3):
            return True
        return False

    def has_execute(self):
        if self.has_all() or self.permission in (1, 5, 3):
            return True
        return False

    def has_all(self):
        if self.permission == 7:
            return True
        return False
