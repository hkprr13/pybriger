#-------------------------------------------------------------------------------
from ..common       import private # プライベートメソッド
from ..common       import public  # パブリックメソッド
from ..config       import Config  # コンフィグクラス
from ..query        import Query   # クエリクラス
#-------------------------------------------------------------------------------
class DDL:
    #---------------------------------------------------------------------------
    def __init__(self, query : str) -> None:
        self.__query= query
    #---------------------------------------------------------------------------
    @property
    @private
    def __sqlEngine(self):
        """
        sqlエンジンの設定
        """
        engine = Config.sqlEngine
        if engine is None:
            raise Exception("エンジンが未設定です")
        return engine
    #---------------------------------------------------------------------------
    @public
    def execute(self):
        self.__sqlEngine.execute(Query(self.__query))
    #---------------------------------------------------------------------------
    @public
    def commit(self):
        self.__sqlEngine.commit()
#-------------------------------------------------------------------------------