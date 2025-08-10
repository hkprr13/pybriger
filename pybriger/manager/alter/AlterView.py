from ..Base import Base    #マネージャーのベースクラス

class AlterView(Base):
    def __init__(self, tableName: str):
        super().__init__(tableName)