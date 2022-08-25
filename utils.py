from xml.etree.ElementTree import Element
import os


USAGE_STR = """
python convert.py [FLAGS]

REQUIRED FLAGS:
    -i\tInput file
    -o\tOutput file
"""


def set_by_list(tree, file_path, contents):
    last_key = file_path[-1]
    for k in file_path[:-1]:
        tree = tree[k]

    tree[last_key] = contents


def populate_file_tree(tree, files):
    for file, contents in files.items():
        file_path = file.replace("\\", "/").split("/")
        set_by_list(tree, file_path, contents)

    return tree


def determine_filetype(filename):
    return filename.split(".")[-1]


def de_namespace(element_tree: Element):
    it = element_tree
    for child in it:
        child.tag = child.tag.split('}', 1)[1]
        de_namespace(child)
    return it


def vertex_list_from_dict(data):
    return data["x"], data["y"], data["z"]


def cross_product(a, b):
    return [((a[1] * b[2]) - (a[2] * b[1])),
            ((a[2] * b[0]) - (a[0] * b[2])),
            ((a[0] * b[1]) - (a[1] * b[0]))]


def calculate_normal(vertices, indices):
    indices = [int(indices["v1"]), int(indices["v2"]), int(indices["v3"])]
    v0, v1, v2 = (vertices[indices[0]]), vertices[indices[1]], vertices[indices[2]]
    v0, v1, v2 = [float(v0[0]), float(v0[1]), float(v0[2])],\
                 [float(v1[0]), float(v1[1]), float(v1[2])],\
                 [float(v2[0]), float(v2[1]), float(v2[2])]
    return cross_product([v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2]], [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]])


def convert_verts_to_xml(vertices):
    output = []
    for vert in vertices:
        output.append(f'vertex x="{vert[0]}" y="{vert[1]}" z="{vert[2]}"')

    return output


def convert_faces_to_xml(data, offset):
    output = []
    for vert in data:
        output.append(f'triangle v1="{int(vert[0][0]) + offset}" v2="{int(vert[1][0]) + offset}" v3="{int(vert[2][0]) + offset}"')

    return output


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)