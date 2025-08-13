#-------------------------------------------------------------------------------
from .Constraints import Constraints # 基底クラス
from ..common     import private     # プライベートメソッド
from ..common     import public      #　パブリックメソッド
#-------------------------------------------------------------------------------
class NotNull(Constraints):
    def __init__(
            self,
            enabled: bool | None = None
        ):
        """
        NOT NULL 制約を管理するクラス
        Args:
            enabled (bool | None): TrueならNOT NULL有効
                                   Falseなら無効
                                   Noneなら未明示
        """
        self.setEnabled(enabled)
    #---------------------------------------------------------------------------
    @private
    def setEnabled(
            self,
            enabled: bool | None
        ) -> None:
        if enabled is not None \
        and not isinstance(enabled, bool):
            raise TypeError("enabledはboolまたはNoneである必要があります")
        self.enabled = enabled
    #---------------------------------------------------------------------------
    @public
    def isEnabled(self) -> bool | None:
        """
        NOT NULLが有効かどうかを取得する
        Returns:
            bool | None: 有効ならTrue
                         無効ならFalse
                         未明示ならNone
        """
        return self.enabled
    #---------------------------------------------------------------------------
    @public
    def toSql(self) -> str:
        """
        SQL形式のNOT NULL制約文字列を返す
        Returns:
            str: NOT NULLまたは 空文字（未明示の場合）
        """
        if self.enabled is None:
            return ""
        elif self.enabled:
            return "NOT NULL"
        else:
            return ""
#-------------------------------------------------------------------------------
