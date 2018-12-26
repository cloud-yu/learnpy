# -*- coding: utf-8 -*-
import os


class SearchFile():
    def __init__(self, path='.'):
        self._path = path
        self._abspath = os.path.abspath(self._path)

    def findfile(self, filename, root=''):
        if not os.path.isabs(root):
            root = os.path.join(self._abspath, root)

        try:
            dirlist = os.listdir(root)
            for dir in dirlist:
                dir = os.path.join(root, dir)
                if (os.path.isfile(dir)):
                    if os.path.basename(dir).find(filename) != -1:
                        yield os.path.relpath(dir, self._abspath)

                if (os.path.isdir(dir)):
                    # for value in self.findfile(filename, dir):
                    #     yield value
                    yield from self.findfile(filename, dir)
        except FileNotFoundError as e:
            print('File not found!')


if __name__ == '__main__':
    f = SearchFile()
    #    f.findfile('py')
    for file in (list(f.findfile('py'))):
        print(file)
