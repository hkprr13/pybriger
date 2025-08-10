#-------------------------------------------------------------------------------
from .Constraints import Constraints # 基底クラス
from ..common     import private     # プライベートメソッド
from ..common     import public      #　パブリックメソッド
#-------------------------------------------------------------------------------
class AutoIncrement(Constraints):
    def __init__(self) -> None:
        ...
    @public
    def toSql(self) -> str:
        return "AUTOINCREMENT"
#-------------------------------------------------------------------------------