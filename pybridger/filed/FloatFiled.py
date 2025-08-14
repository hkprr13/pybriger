#-------------------------------------------------------------------------------
from .Filed      import Filed # 基底クラス
from ..datatypes import Float # 浮動小数点型
#-------------------------------------------------------------------------------
class FloatFiled(Filed):
    """
    浮動小数点型カラム定義クラス
    """
    def __init__(
            self,
            isNotNull               = False,
            default    : str | None = None,
            foreignKey : str | None = None
        ) -> None:
        """
        浮動小数点型カラム定義の初期化
        Args:
            isNotNull  (bool)       : NotNull制約を有効化するかどうか
            defalut    (str | None) : デフォルト値を設定するかどうか   
            foreignKey (str | None) : 外部キー制約の指定  
        """
        super().__init__(
            dataType        = Float(),   # データ型の指定
            isPrimaryKey    = False,     # 設定しない
            isNotNull       = isNotNull, # 初期化時に依存
            isUnique        = False,     # 設定しない
            isAutoincrement = False,     # 設定しない
            default         = default,   # 初期化時に依存
            foreignKey      = foreignKey # 初期化時に依存
        )
#-------------------------------------------------------------------------------