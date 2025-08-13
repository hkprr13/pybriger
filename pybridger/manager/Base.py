#-------------------------------------------------------------------------------
from ..common import public  # パブリックメソッド
from ..config import Config  # コンフィグクラス
#-------------------------------------------------------------------------------
class Base:
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
        engine = Config.sqlEngine
        if engine is None:
            raise Exception("エンジンが未設定です")
        return engine
    #---------------------------------------------------------------------------
    @public
    def connect(self):
        """コネクト"""
        self.sqlEngine.connect()
    #---------------------------------------------------------------------------        
    @public
    def cursor(self):
        """カーソル"""
        return self.sqlEngine.cursor()

    # #---------------------------------------------------------------------------
    @public
    def execute(self, query : str, value : tuple = ()):
        """クエリの実行"""
        self.sqlEngine.execute(query, value)
    #---------------------------------------------------------------------------
    @public
    def executeAny(self, query : str, data : list[tuple[str]]):
        """複数クエリの実行"""
        self.sqlEngine.executeAny(query, data)
    #---------------------------------------------------------------------------
    @public
    def commit(self):
        """データベースにコミットする"""
        self.sqlEngine.commit()
    #---------------------------------------------------------------------------
    @public
    def transaction(self):
        """トランザクション"""
        self.sqlEngine.transaction()
    #---------------------------------------------------------------------------
    @public
    def rollback(self):
        """ロールバック"""
        self.sqlEngine.rollback()
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self) -> str:...
#-------------------------------------------------------------------------------