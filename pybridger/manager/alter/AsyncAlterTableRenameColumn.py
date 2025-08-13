#-------------------------------------------------------------------------------
from ..AsyncBase import AsyncBase # 基底クラス
from ...common   import public    # パブリックメソッド
#-------------------------------------------------------------------------------
class AsyncAlterTableRenameColumn(AsyncBase):
    """テーブルのカラム名変更クラス"""
    #---------------------------------------------------------------------------
    def __init__(
            self,
            tableName : str,
            oldName   : str,
            newName   : str,
        ):
        """
        テーブルのカラム名変更クラス
        Args:
            tableName (str) : テーブル名
            oldName   (str) : 既存の名前
            newName   (str) : 新しい名前
        """
        super().__init__(tableName)
        self.__query = f"ALTER TABLE {tableName} " \
                     + f"RENAME COLUMN {oldName} TO {newName};"
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