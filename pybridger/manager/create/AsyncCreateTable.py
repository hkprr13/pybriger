#-------------------------------------------------------------------------------
from ..AsyncBase import AsyncBase # 基底クラス
from ...common   import public    # パブリックメソッド
#-------------------------------------------------------------------------------
class AsyncCreateTable(AsyncBase):
    """
    非同期テーブル作成クラス
    ※存在する場合も
    """
    def __init__(
            self,
            tableName : str,
            columns   : str
        ):
        """
        非同期テーブル作成クラスの初期化
        Args:
            tableName (str) : テーブル名
            columns   (str) : CREATE TABLE (...);の...部分
        """
        super().__init__(tableName)
        # クエリ
        self.__query = f"CREATE TABLE {tableName} ({columns});"
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