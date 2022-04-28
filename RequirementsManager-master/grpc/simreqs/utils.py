import os
import os.path as op
from typing import List


def get_all_files(root_path: str) -> List[str]:
    result = []
    for path, sub_dirs, files in os.walk(root_path):
        for name in files:
            file = op.join(path, name)
            result.append(file)
    return result
