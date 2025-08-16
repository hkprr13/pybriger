#-------------------------------------------------------------------------------
from .Condition import Condition
#-------------------------------------------------------------------------------
class ConditionGroup(Condition):
    """
    条件式クラス(複数グループ)
    """
    def __init__(
            self,
            tableName, 
            left,
            operator = None,
            right    = None
        ):
        """
        条件式クラス
        Args:
            tableName (str | None) : テーブル名
            left      (Any)        : 左の条件
            operator  (Any | None) : 比較文
            right     (Any | None) : 右の条件
        """
        super().__init__(tableName, left, operator, right)
    #---------------------------------------------------------------------------
    def __str__(self):
        return super().__str__()
#-------------------------------------------------------------------------------