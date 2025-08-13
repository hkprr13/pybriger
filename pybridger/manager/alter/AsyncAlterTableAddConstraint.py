#-------------------------------------------------------------------------------
from ..AsyncBase import AsyncBase # 基底クラス
from ...common   import public    # パブリックメソッド
#-------------------------------------------------------------------------------
class AsyncAlterTableAddConstraint(AsyncBase):
    def __init__(self, tableName: str):
        super().__init__(tableName)
#-------------------------------------------------------------------------------