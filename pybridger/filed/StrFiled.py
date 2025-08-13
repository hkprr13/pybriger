#-------------------------------------------------------------------------------
from .Filed      import Filed # 基底クラス
from ..datatypes import Char  # 固定長文字列型
#-------------------------------------------------------------------------------
class StrFiled(Filed):
    def __init__(
            self,
            isPrimaryKey    = False,
            isNotNull       = False,
            isUnique        = False,
            default         = None,
            foreignKey      = None
        ) -> None:
        super().__init__(
            dataType        = Char(),
            isPrimaryKey    = isPrimaryKey,
            isNotNull       = isNotNull,
            isUnique        = isUnique,
            isAutoincrement = False,
            default         = default,
            foreignKey      = foreignKey
        )
#-------------------------------------------------------------------------------