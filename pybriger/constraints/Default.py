#-------------------------------------------------------------------------------
from .Constraints import Constraints # 基底クラス
from ..common     import private     # プライベートメソッド
from ..common     import public      #　パブリックメソッド
#-------------------------------------------------------------------------------
class Default(Constraints):
    def __init__(self, value: str | int | float | bool | None):
        """
        デフォルト値の定義クラス
        Args:
            value (str | int | float | bool | None): デフォルト値
        """
        self.setValue(value)
    #---------------------------------------------------------------------------
    @private
    def setValue(self, value: str | int | float | bool | None):
        """
        デフォルト値を設定（内部用）
        Raises:
            TypeError: 非対応のデータ型の場合
        """
        if isinstance(value, (str, int, float, bool)) or value is None:
            self.value = value
        else:
            raise TypeError(
                f"デフォルト値として使用できない型: {type(value).__name__}"
            )
    #---------------------------------------------------------------------------
    @public
    def getValue(self) -> str | int | float | bool | None:
        """
        デフォルト値を取得
        Returns:
            str | int | float | bool | None: デフォルト値
        """
        return self.value
    #---------------------------------------------------------------------------
    @public
    def toSql(self) -> str:
        """
        SQL文の DEFAULT 句に変換
        Returns:
            str: SQL形式のDEFAULT句（例: DEFAULT 1）
        """
        if self.value is None:
            return ""
        elif isinstance(self.value, str):
            return f"DEFAULT '{self.value}'"
        elif isinstance(self.value, bool):
            return "DEFAULT TRUE" if self.value else "DEFAULT FALSE"
        else:
            return f"DEFAULT {self.value}"
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------