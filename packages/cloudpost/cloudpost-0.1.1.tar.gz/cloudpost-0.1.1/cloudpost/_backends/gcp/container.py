

class Container:
    type = 'container'
    def __init__(self, name, *, path=None, mount=None):
        self.name = name
        self.path = path
        self.mount = mount
        if mount:
            mount.mounted = self

