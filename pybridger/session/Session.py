#-------------------------------------------------------------------------------
from ..config   import Config
from ..common   import private
#-------------------------------------------------------------------------------
class Session:
    def __init__(self) -> None:
        self.__conn = None
    #---------------------------------------------------------------------------
    @property
    @private
    def __sqlEngine(self):
        engine = Config.sqlEngine
        if engine is None:
            raise Exception("エンジンが未設定です")
        return engine
    #---------------------------------------------------------------------------
    def __enter__(self):
        self.__conn = self.__sqlEngine.connect()
        return self.__conn
    #---------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                if self.__conn:
                    self.__conn.commit()
            else:
                if self.__conn:
                    self.__conn.rollback()
        finally:
            if self.__conn:
                self.__conn.close()
            self.__conn = None
    #---------------------------------------------------------------------------
#-------------------------------------------------------------------------------