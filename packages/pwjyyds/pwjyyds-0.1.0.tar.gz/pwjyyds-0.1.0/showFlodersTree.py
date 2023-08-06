import re
from pathlib import Path
from pathlib import WindowsPath
from typing import Optional, List
import toDocx

__version__ = '0.1.0'

"""
输入路径，展现路径下的文件树状结构图
"""


class DirectionTree:
    def __init__(self,
                 direction_name: str = 'WorkingDirection',
                 direction_path: str = '.',
                 ignore_list: Optional[List[str]] = None):
        self.owner: WindowsPath = Path(direction_path)
        self.tree: str = direction_name + '\n'
        self.ignore_list = ignore_list
        if ignore_list is None:
            self.ignore_list = []
        self.direction_ergodic(path_object=self.owner, n=0)

    def tree_add(self, path_object: WindowsPath, n=0, last=False):
        if n > 0:
            if last:
                self.tree += '│' + ('    │' * (n - 1)) + '    └─ ─ ─ ' + path_object.name
            else:
                self.tree += '│' + ('    │' * (n - 1)) + '    ├─ ─ ─ ' + path_object.name
        else:
            if last:
                self.tree += '└' + '─ ─ ─ ' + path_object.name
            else:
                self.tree += '├' + '─ ─ ─ ' + path_object.name
        if path_object.is_file():
            self.tree += '\n'
            return False
        elif path_object.is_dir():
            self.tree += '\n'
            return True

    def filter_file(self, file):
        for item in self.ignore_list:
            if re.fullmatch(item, file.name):
                return False
        return True

    def direction_ergodic(self, path_object: WindowsPath, n=0):
        dir_file: list = list(path_object.iterdir())
        dir_file.sort(key=lambda x: x.name.lower())
        dir_file = [f for f in filter(self.filter_file, dir_file)]
        for i, item in enumerate(dir_file):
            if i + 1 == len(dir_file):
                if self.tree_add(item, n, last=True):
                    self.direction_ergodic(item, n + 1)
            else:
                if self.tree_add(item, n, last=False):
                    self.direction_ergodic(item, n + 1)


def main():
    i_l = [
        '\.git', '__pycache__', 'test.+', 'venv', '.+\.whl', '\.idea', '.+\.jpg', '.+\.png',
        'image', 'css', 'admin', 'tool.py', 'db.sqlite3'
    ]
    path = r'E:\GIS实验项目\土地征用\征地管理信息系统'
    # 生成结构树
    tree = DirectionTree(ignore_list=i_l, direction_path=path)
    print(tree.tree)

    # 将结构树打包
    # mydoc = toDocx.doc
    # mydoc.toDoc(mydoc, tree.tree)


if __name__ == '__main__':
    main()
