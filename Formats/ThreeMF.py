from zipfile import *
from xml.etree import ElementTree
from utils import *
from os import mkdir, path, rmdir, remove
from Formats.DictXml import dict_to_xml


class ThreeMF:
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
        dirs = []
        with ZipFile(filename, mode="r") as file:
            for innerfile in file.namelist():
                if innerfile.split(".")[-1] in ["xml", "rels", "model"]:
                    with file.open(innerfile, "r") as file_:
                        self.inner_files[file_.name] = file_.read()
                        file_.close()

                    dirs.append(innerfile.replace("\\", "/").split("/")[:-1])

            file.close()

        tree = {}
        for folder in dirs:
            p = tree
            for x in folder:
                p = p.setdefault(x, {})

        tree = populate_file_tree(tree, self.inner_files)

        models = tree["3D"]
        relations = tree["_rels"][".rels"].decode("utf-8")
        types = tree["[Content_Types].xml"].decode("utf-8")

        for model_file in models.keys():
            models[model_file] = models[model_file].decode("utf-8")

        # [print(model) for key, model in models.items()]
        # print(relations)
        # print(types)

        model_found = False
        for name, model in models.items():
            model_xml = ElementTree.fromstring(model)
            model_xml = de_namespace(model_xml)

            self.units = model_xml.get('unit')
            for child in model_xml:
                if child.tag == "resources":
                    for objects in child:
                        if 'type' not in objects.attrib.keys():
                            objects.attrib['type'] = 'not_a_model'

                        if objects.attrib['type'] == 'model':
                            model_found = True
                            b_id = f"b{objects.attrib['id']}"
                            self.bodies.append(b_id)
                            self.verts[b_id] = []
                            self.faces[b_id] = []
                            self.normals[b_id] = []
                            self.textures[b_id] = []

                            for vert in objects.findall("mesh/vertices/vertex"):
                                self.verts[b_id].append(vertex_list_from_dict(vert.attrib))
                                self.textures[b_id].append([0, 0, 0])

                            for index in objects.findall("mesh/triangles/triangle"):
                                normal = calculate_normal(self.verts[b_id], index.attrib)
                                if normal not in self.normals[b_id]:
                                    self.normals[b_id].append(normal)
                                    normal = len(self.normals[b_id]) - 1
                                else:
                                    normal = self.normals[b_id].index(normal)

                                self.faces[b_id].append([
                                    [index.attrib["v1"], index.attrib["v1"], normal],
                                    [index.attrib["v2"], index.attrib["v2"], normal],
                                    [index.attrib["v3"], index.attrib["v3"], normal]])

        if not model_found:
            raise NotImplementedError("3MF didn't have any models")

    def save(self, filename):
        offset = -1 if self.obj_ready else 0

        model_tag = f'model unit="{self.units}" xml:lang="en-US" ' \
                    f'xmlns:m="http://schemas.microsoft.com/3dmanufacturing/material/2015/02" ' \
                    f'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"'
        model_xml_dict = {model_tag: {'resources': {}, 'build': []}}

        for body in self.bodies:
            if not self.faces[body]:
                continue

            object_tag = f'object id="{body}" type="model"'
            xml_verts = convert_verts_to_xml(self.verts[body])
            xml_faces = convert_faces_to_xml(self.faces[body], offset)
            model_xml_dict[model_tag]['resources'][object_tag] = {}
            model_xml_dict[model_tag]['resources'][object_tag]['mesh'] = {}
            model_xml_dict[model_tag]['resources'][object_tag]['mesh']['vertices'] = xml_verts
            model_xml_dict[model_tag]['resources'][object_tag]['mesh']['triangles'] = xml_faces

            model_xml_dict[model_tag]['build'].append(f'item objectid="{body}"')

        rels = '<?xml version="1.0" encoding="UTF-8"?><Relationships ' \
               'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' \
               '<Relationship Target="/3D/3dmodel.model" Id="rel0" ' \
               'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" /></Relationships>'
        content_types = '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' \
                        '<Default Extension="rels" ' \
                        'ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' \
                        '<Default Extension="model" ' \
                        'ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'

        t = 0
        temp_folder = f"./TEMP_{t}/"
        while path.exists(temp_folder):
            t += 1
            temp_folder = f"./TEMP_{t}/"
        mkdir(temp_folder)

        with cd(temp_folder):
            mkdir("3D")
            mkdir("_rels")

            with open("[Content_Types].xml", "w") as c_types:
                c_types.write(content_types)
                c_types.close()

            with open("_rels/.rels", "w") as rels_f:
                rels_f.write(rels)
                rels_f.close()

            with open("3D/3dmodel.model", "w") as model:
                model.write(dict_to_xml(model_xml_dict))
                model.close()

            with ZipFile(filename, "w", ZIP_DEFLATED) as zipfile:
                zipfile.write("[Content_Types].xml")
                zipfile.write("3D/3dmodel.model")
                zipfile.write("_rels/.rels")
                zipfile.close()

            remove("./[Content_Types].xml")
            remove("./_rels/.rels")
            remove("./3D/3dmodel.model")
            rmdir("./_rels")
            rmdir("./3D")

        rmdir(temp_folder)

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
