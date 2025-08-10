#-------------------------------------------------------------------------------
from ..AsyncBase import AsyncBase   # 基底クラス
from ...common   import public      # パブリックメソッド
#-------------------------------------------------------------------------------
class AsyncDropTrigger(AsyncBase):
    """トリガー削除クラス"""
    def __init__(
            self,
            tableName   : str,
            triggerName : str
        ):
        """
        トリガー削除クラスの初期化
        Args:
            tableName   (str) : テーブル名
            triggerName (str) : トリガー名
        """
        super().__init__(tableName)
        self.__query = f"DROP TRIGGER {triggerName};"
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self):
        """クエリ"""
        return self.__query
    #---------------------------------------------------------------------------
    async def execute(self):
        await self.sqlEngine.execute(self.__query)
#-------------------------------------------------------------------------------