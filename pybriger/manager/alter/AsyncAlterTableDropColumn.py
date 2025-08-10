#-------------------------------------------------------------------------------
from ..AsyncBase import AsyncBase # 基底クラス
from ...common   import public    # パブリックメソッド
#-------------------------------------------------------------------------------
class AsyncAlterTableDropColumn(AsyncBase):
    """テーブルからカラムを削除するクラス"""
    #---------------------------------------------------------------------------
    def __init__(
            self,
            tableName  : str,
            columnName : str
        ):
        """
        テーブルからカラムを削除するクラスの初期化
        Args:
            tableName (str)  : テーブル名
            columnNmae (str) : カラム名
        """
        super().__init__(tableName)
        self.__query = f"ALTER TABLE {tableName} DROP COLUMN {columnName};"
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self):
        """クエリ"""
        return self.__query
    #---------------------------------------------------------------------------
    @public
    async def execute(self):
        return await super().execute(self.__query)
#-------------------------------------------------------------------------------