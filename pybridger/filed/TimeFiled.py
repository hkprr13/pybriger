#-------------------------------------------------------------------------------
from .Filed      import Filed # 基底クラス
from ..datatypes import Time  # 時刻型
#-------------------------------------------------------------------------------
class TimeFiled(Filed):
    def __init__(
            self,
            isNotNull       = False,
            default         = None,
            foreignKey      = None
        ) -> None:
        """
        時間型のカラム定義クラスの初期化
        Args:
            isNotNull  (bool)       : NotNull制約を有効化するかどうか
            defalut    (str | None) : デフォルト値を設定するかどうか   
            foreignKey (str | None) : 外部キー制約の指定  
        """
        super().__init__(
            dataType        = Time(),    # データ型の指定
            isPrimaryKey    = False,     # 設定しない
            isNotNull       = isNotNull, # 初期化時に依存
            isUnique        = False,     # 設定しない
            isAutoincrement = False,     # 設定しない
            default         = default,   # 初期化時に依存
            foreignKey      = foreignKey # 初期化時に依存
        )
#-------------------------------------------------------------------------------