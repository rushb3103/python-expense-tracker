from libraries.db import db


class transactions(db):
    def __init__(self):
        super().__init__()
        self.table = "transactions"