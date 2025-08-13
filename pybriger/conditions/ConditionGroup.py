#-------------------------------------------------------------------------------
from .Condition import Condition
#-------------------------------------------------------------------------------
class ConditionGroup(Condition):
    def __init__(
            self,
            tableName, 
            left,
            operator = None,
            right    = None
        ):
        super().__init__(tableName, left, operator, right)
    #---------------------------------------------------------------------------
    def __str__(self):
        return super().__str__()
#-------------------------------------------------------------------------------