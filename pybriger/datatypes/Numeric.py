#-------------------------------------------------------------------------------
from .DataType import DataType # データ型クラス
from ..config  import Config   # コンフィグクラス
#-------------------------------------------------------------------------------
class Numeric(DataType):
    """DECIMALの別名型"""
    def __init__(self):
        # エンジンと非同期エンジンが未設定なら
        if Config.sqlEngine is None and Config.asyncSqlEngine is None:
            raise Exception("エンジンが未設定です")
        # エンジンが設定されていて、非同期エンジンが未設定
        elif Config.asyncSqlEngine is None and Config.sqlEngine is not None:
            super().__init__(query = Config.sqlEngine.NUMERIC)
        # エンジンが未設定されていて、非同期エンジンが設定されている
        elif Config.sqlEngine is None and Config.asyncSqlEngine is not None:
            super().__init__(query = Config.asyncSqlEngine.NUMERIC)
        else:
            raise Exception("エンジン設定エラー")
#-------------------------------------------------------------------------------