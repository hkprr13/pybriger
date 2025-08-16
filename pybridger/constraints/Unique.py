#-------------------------------------------------------------------------------
from .Constraints import Constraints # 基底クラス
from ..common     import private     # プライベートメソッド
from ..common     import public      #　パブリックメソッド
#-------------------------------------------------------------------------------
class Unique(Constraints):
    """
    ユニーク制約クラス
    """
    def __init__(self, isUnique : bool):
        """
        """
        self.__isUnique = isUnique
    #---------------------------------------------------------------------------
    def toSql(self) -> str:
        """
        ユニーク制約のSQLを生成
        Returns:
            str: UNIQUE制約のSQL
        """
        if self.__isUnique:
            return "UNIQUE"
        else:
            return ""
#-------------------------------------------------------------------------------
