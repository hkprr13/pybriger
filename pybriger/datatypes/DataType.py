#-------------------------------------------------------------------------------
from ..common import public
#-------------------------------------------------------------------------------
class DataType:
    """
    データ型の基底クラス
    Attributes:
        query     (str) : 使用するSQLのデータ型のクエリ
        length    (int) : 使用するSQLのデータ型の最大文字数の長さ
        precision (int)  : 使用するSQLのデータの精度
    """
    sqlEngine : None
    #---------------------------------------------------------------------------
    def __init__(
            self,
            query     : str | None = None,
            length    : int | None = None,
            precision : int | None = None
        ):
        self.query     = query
        self.length    = length
        self.precision = precision
    #---------------------------------------------------------------------------
    @public
    def getQuery(self) -> str | None:
        """
        データ型のクエリ名の取得
        Returns:
            str | None: 設定されたクエリ文字列
        """
        return self.query
    #---------------------------------------------------------------------------
    @public
    def setQuery(
        self,
        query : str | None = None
    ) -> None:
        """
        Args:
            query (str): クエリ文字列
        Raises:
            TypeError : 引数が文字列でない場合
        """
        if query is None or isinstance(query, str):
            self.query = query
        else:
            raise TypeError("型が違います")
    #---------------------------------------------------------------------------
    @public
    def getLength(self) -> int | None:
        """
        データの長さ（文字数やバイト長）を取得する
        Returns:
            int | None: 設定された長さ
        """
        return self.length
    #---------------------------------------------------------------------------
    @public
    def setLength(
        self,
        length : int | None = None
    ) -> None:
        """
        データの長さを設定する
        Args:
            length (int): 最大長
        Raises:
            TypeError: 引数が整数でない場合
        """
        # 型チェック
        if length is None or isinstance(length, int):
            self.length = length
        else:
            raise TypeError("型が違います")
    #---------------------------------------------------------------------------
    @public
    def getPrecision(self) -> int | None:
        """
        精度を取得する（例：小数点以下の桁数)
        Returns:
            int | None: 設定された精度
        """
        return self.precision
    #---------------------------------------------------------------------------
    @public
    def setPrecision(
        self,
        precision : int | None = None
    ) -> None:
        """
        精度を設定する
        Args:
            precision (int) : 小数点以下の桁数など

        Raises:
            TypeError: 引数が整数でない場合
        """
        # 型チェック
        if precision is None or isinstance(precision, int):
            self.precision = precision
        else:
            raise TypeError("型が違います")
    #---------------------------------------------------------------------------
    @public
    def toSql(self) -> str:
        """
        設定をもとにSQLの型定義文字列を生成して返す
        Returns:
            str: SQLの型定義文字列
        """
        # 長さが未定義(None)ではなくかつ制度が未定義(None)ではないとき
        if  self.length    is not None \
        and self.precision is not None:
            return f"{self.query}({self.length},{self.precision})"
        # 長さが未定義(None)ではないとき
        elif self.length is not None:
            return f"{self.query}({self.length})"
        # 長さが未定義(None)であり、かつ制度が未定義(None)であるとき
        else:
            return self.query if self.query else ""

#-------------------------------------------------------------------------------