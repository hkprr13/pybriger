#-------------------------------------------------------------------------------
from .Filed      import Filed # 基底クラス
from ..datatypes import Time  # 時刻型
#-------------------------------------------------------------------------------
class TimeFiled(Filed):
    def __init__(
            self,
            isPrimaryKey    = False,
            isNotNull       = False,
            default         = None,
            foreignKey      = None
        ) -> None:
        super().__init__(
            dataType        = Time(),
            isPrimaryKey    = isPrimaryKey,
            isNotNull       = isNotNull,
            isUnique        = False,
            isAutoincrement = False,
            default         = default,
            foreignKey      = foreignKey
        )
#-------------------------------------------------------------------------------