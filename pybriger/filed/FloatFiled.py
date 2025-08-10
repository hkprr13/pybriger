#-------------------------------------------------------------------------------
from .Filed      import Filed # 基底クラス
from ..datatypes import Float # 浮動小数点型
#-------------------------------------------------------------------------------
class FloatFiled(Filed):
    def __init__(
            self,
            isPrimaryKey    = False,
            isNotNull       = False,
            isUnique        = False,
            default         = None,
            foreignKey      = None
        ) -> None:
        super().__init__(
            dataType        = Float(),
            isPrimaryKey    = isPrimaryKey,
            isNotNull       = isNotNull,
            isUnique        = isUnique,
            isAutoincrement = False,
            default         = default,
            foreignKey      = foreignKey
        )
#-------------------------------------------------------------------------------