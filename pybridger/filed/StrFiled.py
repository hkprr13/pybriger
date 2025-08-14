#-------------------------------------------------------------------------------
from .Filed      import Filed # 基底クラス
from ..datatypes import Char  # 固定長文字列型
#-------------------------------------------------------------------------------
class StrFiled(Filed):
    """
    文字列型カラム定義
    """
    def __init__(
            self,
            isPrimaryKey    : bool        = False,
            isNotNull       : bool        = False,
            isUnique        : bool        = False,
            isAutoincrement : bool        = False,
            default         : str  | None = None,
            foreignKey      : str  | None = None
        ) -> None:
        """
        文字列型カラム定義の初期化
        Args:
            isPrimaryKey    (bool)       : 主キーの設定
            isNotNull       (bool)       : NotNull制約の設定
            isUnique        (bool)       : ユニーク制約の設定
            isAutoincrement (bool)       : 自動採番の設定
            default         (str | None) : デフォルト値の設定
            foreignKey      (str | None) : 外部キー制約の設定
        """
        super().__init__(
            dataType        = Char(),       # データ型の指定
            isPrimaryKey    = isPrimaryKey, # 初期化時に依存
            isNotNull       = isNotNull,    # 初期化時に依存
            isUnique        = isUnique,     # 初期化時に依存
            isAutoincrement = False,        # 設定しない
            default         = default,      # 初期化時に依存
            foreignKey      = foreignKey    # 初期化時に依存
        )
#-------------------------------------------------------------------------------