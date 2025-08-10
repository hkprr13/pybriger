from ..Base import Base    #マネージャーのベースクラス

class AlterTableAddConstraint(Base):
    def __init__(self, tableName: str):
        super().__init__(tableName)
        