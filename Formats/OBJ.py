class OBJ:
    def __init__(self):
        self.bodies = ["default"]
        self.verts = {"default": []}
        self.textures = {"default": []}
        self.normals = {"default": []}
        self.faces = {"default": []}
        self.units = "millimeter"
        self.obj_ready = False

    def load(self, filename):
        self.__init__()
        self.obj_ready = True
        with open(filename, "r") as file:
            for line in file:
                prefix = line.split(" ")[0]
                if prefix == "g":
                    bodyName = " ".join(line.split(" ")[1:]).strip()
                    self.verts[bodyName] = []
                    self.normals[bodyName] = []
                    self.textures[bodyName] = []
                    self.faces[bodyName] = []
                    self.bodies.append(bodyName)
                if prefix == "v":
                    self.verts["default"].append([x.strip() for x in line.split(" ")[1:]])
                if prefix == "vt":
                    self.textures["default"].append([x.strip() for x in line.split(" ")[1:]])
                if prefix == "vn":
                    self.normals["default"].append([x.strip() for x in line.split(" ")[1:]])
                if prefix == "f":
                    self.faces["default"].append([x.strip().split("/") for x in line.split(" ")[1:]])

            file.close()

    def save(self, filename):
        file_contents = ""
        offset = 0 if self.obj_ready else 1
        vert_offset, text_offset, normal_offset = 0, 0, 0
        for body in self.bodies:
            file_contents += "\n"
            file_contents += f"g {body}\n"

            file_contents += "\n"
            for vert in self.verts[body]:
                file_contents += f"v {vert[0]} {vert[1]} {vert[2]}\n"

            file_contents += "\n"
            for text in self.textures[body]:
                file_contents += f"vt {text[0]} {text[1]} {text[2]}\n"

            file_contents += "\n"
            for normal in self.normals[body]:
                file_contents += f"vn {normal[0]} {normal[1]} {normal[2]}\n"

            file_contents += "\n"
            for face in self.faces[body]:
                file_contents += f"f {int(face[0][0]) + offset + vert_offset}/{int(face[0][1]) + offset + text_offset}/{int(face[0][2]) + offset + normal_offset} " \
                                 f"{int(face[1][0]) + offset + vert_offset}/{int(face[1][1]) + offset + text_offset}/{int(face[1][2]) + offset + normal_offset} " \
                                 f"{int(face[2][0]) + offset + vert_offset}/{int(face[2][1]) + offset + text_offset}/{int(face[2][2]) + offset + normal_offset}\n"

            file_contents += "\n"

            vert_offset += len(self.verts[body])
            text_offset += len(self.textures[body])
            normal_offset += len(self.normals[body])

        with open(filename, "w") as file:
            file.write(file_contents)
            file.close()

    def load_from_data(self, bodies, vertices, textures, normals, indices, obj_ready=False, units="millimeter"):
        self.bodies = bodies
        self.verts = vertices
        self.textures = textures
        self.normals = normals
        self.faces = indices
        self.obj_ready = obj_ready
        self.units = units

    def return_data(self):
        return self.bodies, self.verts, self.textures, self.normals, self.faces, self.obj_ready
