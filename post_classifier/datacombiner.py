class DataCombiner():
    filelocations = []
    data = []
    target = []
    classification_names = dict()

    def __init__(self, filenames=[], classifications=[]):
        if filenames is None:
            raise TypeError
        if classifications is None:
            raise TypeError
        self.filelocations = filenames
        self.parseFiles()

    def parseFiles(self):
        try:
            for index, filename in enumerate(self.filelocations):
                if not isinstance(filename, str):
                    raise TypeError
                ax = open(filename, 'r').read().split('\n')
                self.data += ax
                self.target += [index for _ in range(len(ax))]
                self.classification_names[index] = filename
        except Exception as e:
            print('Error parsing files')


class Object(object):
    pass
