#-------------------------------------------------------------------------------
from ..common import public  # パブリックメソッド
from ..config import Config  # コンフィグクラス
#-------------------------------------------------------------------------------
class AsyncBase:
    """
    データベース操作マネージャークラスにおける基底クラス
    """
    def __init__(self, tableName : str):
        """初期化"""
        self.tableName = tableName
    #---------------------------------------------------------------------------
    @property
    @public
    def sqlEngine(self):
        """sqlエンジンの設定"""
        engine = Config.asyncSqlEngine
        if engine is None:
            raise Exception("エンジンが未設定です")
        return engine
    #---------------------------------------------------------------------------
    @public
    async def connect(self):
        """コネクト"""
        await self.sqlEngine.connect()
    #---------------------------------------------------------------------------        
    @public
    async def cursor(self):
        """カーソル"""
        return await self.sqlEngine.cursor()

    # #---------------------------------------------------------------------------
    @public
    async def execute(self, query : str, value : tuple = ()):
        """クエリの実行"""
        await self.sqlEngine.execute(query, value)
    #---------------------------------------------------------------------------
    @public
    async def executeAny(self, query : str, data : list[tuple[str]]):
        """複数クエリの実行"""
        await self.sqlEngine.executeAny(query, data)
    #---------------------------------------------------------------------------
    @public
    async def commit(self):
        """データベースにコミットする"""
        await self.sqlEngine.commit()
    #---------------------------------------------------------------------------
    @public
    async def transaction(self):
        """トランザクション"""
        await self.sqlEngine.transaction()
    #---------------------------------------------------------------------------
    @public
    async def rollback(self):
        """ロールバック"""
        await self.sqlEngine.rollback()
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self) -> str:...
#-------------------------------------------------------------------------------