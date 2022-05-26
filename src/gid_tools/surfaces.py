class NurbsSurface:
    def __init__(self, parent):
        self.parent = parent
        self.lines = []
        parent.surfaces.append(self)

    def add_line(self, id_: int) -> None:
        self.lines.append(id_)

    def gid_command(self):
        s = "Geometry Create NurbsSurface "
        s += " ".join(str(p) for p in self.lines)
        return s + " Mescape\n"