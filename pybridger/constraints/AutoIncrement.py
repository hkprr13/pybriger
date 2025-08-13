#-------------------------------------------------------------------------------
from .Constraints   import Constraints  # 基底クラス
from ..common       import private      # プライベートメソッド
from ..common       import public       # パブリックメソッド
from ..config       import Config       # コンフィグクラス
#-------------------------------------------------------------------------------
class AutoIncrement(Constraints):
    def __init__(self) -> None:
        ...
    @public
    def toSql(self) -> str:
        engine = Config.sqlEngine
        if engine is None:
            raise Exception("エンジンが未指定です")
        
        return engine.AUTOINCREMENT
#-------------------------------------------------------------------------------