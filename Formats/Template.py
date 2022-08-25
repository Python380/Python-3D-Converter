class Template:
    def __init__(self):
        self.inner_files = {}
        self.bodies = []
        self.verts = {}
        self.textures = {}
        self.normals = {}
        self.faces = {}
        self.obj_ready = False
        self.units = "millimeter"

    def load(self, filename):
        pass

    def save(self, filename):
        offset = 0 if self.obj_ready else 1  # is the model "obj-ready", or ready to be saved in a .obj file as it is?
        pass

    def load_from_data(self, bodies, vertices, textures, normals, indices, obj_ready=False, units="millimeter"):
        self.bodies = bodies
        self.verts = vertices
        self.textures = textures
        self.normals = normals
        self.faces = indices
        self.obj_ready = obj_ready
        self.units = units

    def return_data(self):
        return self.bodies, self.verts, self.textures, self.normals, self.faces, False, self.units
