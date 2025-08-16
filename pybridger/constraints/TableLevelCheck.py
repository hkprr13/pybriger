#-------------------------------------------------------------------------------
from .Constraints import Constraints # 基底クラス
from ..common     import private     # プライベートメソッド
from ..common     import public      #　パブリックメソッド
#-------------------------------------------------------------------------------
class TableLevelCheck(Constraints):
    def __init__(self, *conditons : tuple[str]) -> None:
        self.__conditions = conditons
    #---------------------------------------------------------------------------
    @public
    def toSql(self) -> str:
        sql = ""
        for cond in self.__conditions:
            sql += f"CHECK ({cond}),"
        sql = sql[:-1]
        return sql
#-------------------------------------------------------------------------------