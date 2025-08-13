#-------------------------------------------------------------------------------
from ..AsyncBase import AsyncBase # 基底クラス
from ...common   import public    # パブリックメソッド
#-------------------------------------------------------------------------------
class AsyncDeleteRecord(AsyncBase):
    """
    レコード削除クラス
    """
    #---------------------------------------------------------------------------
    def __init__(
            self,
            tableName : str,
            columns   : str,
            values    : tuple
        ):
        """
        レコード削除のクラスの初期化
        """
        super().__init__(tableName)
        # クエリ
        self.__query = f"DELETE FROM {self.tableName} WHERE {columns}"
        # プレイスホルダーをSQLによって置き換える
        self.__query = self.__query.replace(
            "?", self.sqlEngine.PLACEHOLDER
        )
        # 値
        self.__values = values 
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self):
        """クエリ"""
        return self.__query
    #---------------------------------------------------------------------------
    @public
    @property
    def values(self):
        """値"""
        return self.__values
    #---------------------------------------------------------------------------
    @public
    async def execute(self):
        return await super().execute(self.__query, self.__values)
#-------------------------------------------------------------------------------