#-------------------------------------------------------------------------------
from .Filed      import Filed   # 基底クラス
from ..datatypes import Boolean # 論理値型
#-------------------------------------------------------------------------------
class BoolFiled(Filed):
    def __init__(
            self,
            isPrimaryKey    = False,
            isNotNull       = False,
            isUnique        = False,
            default         = None,
            foreignKey      = None
        ) -> None:
        super().__init__(
            dataType        = Boolean(),
            isPrimaryKey    = isPrimaryKey,
            isNotNull       = isNotNull,
            isUnique        = isUnique,
            isAutoincrement = False,
            default         = default,
            foreignKey      = foreignKey
        )
#-------------------------------------------------------------------------------