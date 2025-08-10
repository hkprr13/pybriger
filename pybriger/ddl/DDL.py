#-------------------------------------------------------------------------------
from ..common     import private   # プライベートメソッド
from ..common     import public    # パブリックメソッド
from ..config     import Config    # コンフィグクラス
#-------------------------------------------------------------------------------
class DDL:
    #---------------------------------------------------------------------------
    def __init__(self, sql : str) -> None:
        self.__sql = sql
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
        self.__sqlEngine.execute(self.__sql)
    #---------------------------------------------------------------------------
    @public
    def commit(self):
        self.__sqlEngine.commit()
#-------------------------------------------------------------------------------