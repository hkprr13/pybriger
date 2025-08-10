#-------------------------------------------------------------------------------
from .Filed      import Filed   # 基底クラス
from ..datatypes import Integer # 整数型
#-------------------------------------------------------------------------------
class IntFiled(Filed):
    def __init__(
            self,
            isPrimaryKey    = False,
            isNotNull       = False,
            isUnique        = False,
            isAutoincrement = False,
            default         = None,
            foreignKey      = None
        ) -> None:
        super().__init__(
            dataType        = Integer(),
            isPrimaryKey    = isPrimaryKey,
            isNotNull       = isNotNull,
            isUnique        = isUnique,
            isAutoincrement = isAutoincrement,
            default         = default,
            foreignKey      = foreignKey
        )
#-------------------------------------------------------------------------------