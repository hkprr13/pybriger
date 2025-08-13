#-------------------------------------------------------------------------------
from .Filed      import Filed    # 基底クラス
from ..datatypes import DateTime # 日付型
#-------------------------------------------------------------------------------
class DateTimeFiled(Filed):
    def __init__(
            self,
            isPrimaryKey    = False,
            isNotNull       = False,
            isUnique        = False,
            default         = None,
            foreignKey      = None
        ) -> None:
        super().__init__(
            dataType        = DateTime(),
            isPrimaryKey    = isPrimaryKey,
            isNotNull       = isNotNull,
            isUnique        = isUnique,
            isAutoincrement = False,
            default         = default,
            foreignKey      = foreignKey
        )
#-------------------------------------------------------------------------------