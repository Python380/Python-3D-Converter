from modelFormats import *


class Converter:
    def __init__(self, filea, fileb):
        self.file_a = filea
        self.file_b = fileb

        # file name is [0], file type is [1]

    def convert(self):
        if self.file_a[1] in TYPES_TO_CLASS_ALIAS.keys() and self.file_b[1] in TYPES_TO_CLASS_ALIAS.keys():
            try:
                file = TYPES_TO_CLASS_ALIAS[self.file_a[1].lower()]()
                file2 = TYPES_TO_CLASS_ALIAS[self.file_b[1].lower()]()

                file.load(self.file_a[0])
                file2.load_from_data(*file.return_data())
                file2.save(self.file_b[0])
            except Exception as e:
                print(e)
                exit(2)
        else:
            print("Unknown Type!")
            exit(1)
