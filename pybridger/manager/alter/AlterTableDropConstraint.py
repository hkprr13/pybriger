from ..Base import Base    #マネージャーのベースクラス

class AlterTableDropConstraint(Base):
    def __init__(self, tableName: str):
        super().__init__(tableName)