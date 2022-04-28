from simreqs.utils import get_all_files
from simreqs.logger import logger


class MySentences:
    def __init__(self, dirname: str, limit: int = None):
        self.files = get_all_files(dirname)
        self.counter = 0
        self.limit = limit

    def __iter__(self):
        for file_ in self.files:
            # 如果超出上限，直接返回
            if self.limit and self.counter > self.limit:
                return

            self.counter += 1
            logger.info(f'Processed {self.counter}...')
            with open(file_, encoding='utf-8') as f:
                for line in f:
                    yield line.split()
