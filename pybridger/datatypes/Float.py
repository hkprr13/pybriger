#-------------------------------------------------------------------------------
from .DataType import DataType # データ型クラス
from ..config  import Config   # コンフィグクラス
#-------------------------------------------------------------------------------
class Float(DataType):
    """浮動小数点型"""
    def __init__(
            self,
            length    : int | None = None,
            precision : int | None = None
        ):
        """
        浮動小数点型 \n
        Args: \n
            length    (int) : 長さ \n
            precision (str) : 精度 \n
        """
        # エンジンと非同期エンジンが未設定なら
        if Config.sqlEngine is None and Config.asyncSqlEngine is None:
            raise Exception("エンジンが未設定です")
        # エンジンが設定されていて、非同期エンジンが未設定
        elif Config.asyncSqlEngine is None and Config.sqlEngine is not None:
            super().__init__(
                query     = Config.sqlEngine.FLOAT,
                length    = length,
                precision = precision
            )
        # エンジンが未設定されていて、非同期エンジンが設定されている
        elif Config.sqlEngine is None and Config.asyncSqlEngine is not None:
            super().__init__(
                query     = Config.asyncSqlEngine.FLOAT,
                length    = length,
                precision = precision
            )
        else:
            raise Exception("エンジン設定エラー")
#-------------------------------------------------------------------------------