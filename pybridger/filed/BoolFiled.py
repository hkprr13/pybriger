#-------------------------------------------------------------------------------
from .Filed         import Filed        # 基底クラス
from ..datatypes    import Boolean      # 論理値型
from ..constraints  import ForeignKey   #
from ..common       import private
#-------------------------------------------------------------------------------
class BoolFiled(Filed):
    """
    真偽値のカラム定義クラス
    """
    #---------------------------------------------------------------------------
    def __init__(
            self,
            isNotNull  : bool        = False,
            default    : bool | None = None,
            foreignKey : str  | None = None
        ) -> None:
        """
        真偽値のカラム定義クラスの初期化
        Args:
            isNotNull  (bool)        : NotNull制約を有効化するかどうか
            defalut    (bool | None) : デフォルト値を設定するかどうか 
                                     : Noneなら未指定,
                                     : Trueならデフォルト値がTrue,
                                     : Flaseならデフォルト値がFalse
            foreignKey (str | None)  : 外部キー制約の指定
        """
        super().__init__(
            dataType        = Boolean(),                  # データ型の指定
            isPrimaryKey    = False,                      # 設定しない
            isNotNull       = isNotNull,                  # 初期化時に依存
            isUnique        = False,                      # 設定しない
            isAutoincrement = False,                      # 設定しない
            default         = self.__setDefalut(default), # 文字列に変換
            foreignKey      = foreignKey                  # 初期化時に依存
        )
    #---------------------------------------------------------------------------
    @private
    def __setDefalut(self, defalut):
        if defalut is None:
            return None
        else:
            return str(defalut)
#-------------------------------------------------------------------------------