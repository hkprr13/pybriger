from ..Base import Base    #マネージャーのベースクラス
class AlterTableRenameTable(Base):
    def __init__(
            self,
            tableName: str
        ):
        super().__init__(tableName)