#-------------------------------------------------------------------------------
from ..datatypes.DataType import DataType       # データ型　<-インポートエラー回避
from ..constraints        import AutoIncrement  # 自動採番 
from ..constraints        import PrimaryKey     # 主キークラス
from ..constraints        import Default        # デフォルト値クラス
from ..constraints        import NotNull        # NotNullクラス
from ..constraints        import Unique         # ユニーク設定クラス
from ..constraints        import ForeignKey     # 外部キー制約クラス
from ..common             import public         # パブリックメソッド
from ..common             import private        # プライベートメソッド
from ..conditions         import Condition      # 条件クラス
from ..conditions         import ConditionGroup # 条件クラス
#-------------------------------------------------------------------------------
class Column:
    """
    SQLのカラムを表現するためのクラス
    データ型、制約（主キー、NOT NULL、デフォルト値、ユニーク、外部キー）を定義し
    テーブル作成用のSQL構築やクエリビルダーでの利用を目的とする
    Attributes:
        columnName   (str)         : カラム名（Modelクラス側で自動設定）
        tableName    (str)         : テーブル名（Modelクラス側で自動設定）
        dataType     (DataType)    : カラムのデータ型
        dataTypeSql  (str)         : SQL用のデータ型文字列
        primaryKeySql(str)         : PRIMARY KEY 制約のSQL文字列
        defaultSql   (str)         : DEFAULT 制約のSQL文字列
        notNullSql   (str)         : NOT NULL 制約のSQL文字列
        uniqueSql    (str)         : UNIQUE 制約のSQL文字列
        foreignKeySql(str)         : FOREIGN KEY 制約のSQL文字列
    """
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    def __init__(
        self,
        dataType        : DataType,
        isPrimaryKey    : bool              = False,
        isAutoIncrement : bool              = False,
        default         : Default    | None = None,
        notNull         : NotNull    | None = None,
        unique          : Unique     | None = None,
        foreignKey      : ForeignKey | None = None
    ):
        """
        カラム情報を初期化する
        Args:
            dataType        (DataType)           : カラムのデータ型
            isPrimaryKey    (bool)               : 主キー
            isAutoIncrement (bool)               : 自動採番
            default         (Default | None)     : デフォルト値
            notNull         (NotNull | None)     : NOT NULL制約
            unique          (Unique | None)      : UNIQUE制約
            foreignKey      (ForeignKey | None)  : 外部キー制約
        Raises:
            ValueError : dataTypeがNoneの場合
        """
        # インスタンス属性の付与
        self.dataType   = dataType
        self.default    = default
        self.notNull    = notNull
        self.unique     = unique
        self.foreignKey = foreignKey
        # SQLの設定
        self.__setDataTypeSql(dataType)
        self.__setPrimaryKeySql(isPrimaryKey)
        self.__setAutoIncrement(isAutoIncrement)
        self.__setDefaultSql(default)
        self.__setNotNullSql(notNull)
        self.__setUniqueSql(unique)
        self.__setForeignKeySql(foreignKey)
        # カラム名とテーブル名
        self.columnName : str
        self.tableName  : str 
    #---------------------------------------------------------------------------
    @private
    def __setDataTypeSql(self, dataType: DataType | None) -> None:
        """
        データ型に応じたSQL文字列を設定する
        Args:
            dataType (DataType | None): データ型オブジェクト
        Raises:
            ValueError : Noneが渡された場合
        """
        if dataType is not None:
            self.dataTypeSql = dataType.toSql()
        else:
            raise ValueError("データ型が指定されていません")
    #---------------------------------------------------------------------------
    @private
    def __setPrimaryKeySql(self, isPrimaryKey : bool) -> None:
        """
        PRIMARY KEY 制約をSQL文字列として設定する
        Args:
            isPrimaryKey (bool): 主キーにするかどうか
        """
        if isPrimaryKey:
            self.primaryKeySql = PrimaryKey().toSql()
        else:
            self.primaryKeySql = ""
    #---------------------------------------------------------------------------
    @private
    def __setAutoIncrement(self, isAutoIncrement : bool ) -> None:
        """
        AUTO INCREMENT 制約をSQL文字列として設定する
        Args:
            isAutoIncrement (bool) : 自動採番するかどうか
        """
        if isAutoIncrement:
            self.autoIncrementSql = AutoIncrement().toSql()
        else:
            self.autoIncrementSql = ""
    #---------------------------------------------------------------------------
    @private
    def __setDefaultSql(self, default : Default | None) -> None:
        """
        DEFAULT 制約をSQL文字列として設定する
        Args:
            default (Default | None): デフォルト値
        """
        self.defaultSql = default.toSql() if default else ""
    #---------------------------------------------------------------------------
    @private
    def __setNotNullSql(self, notNull : NotNull | None) -> None:
        """
        NOT NULL 制約をSQL文字列として設定する
        Args:
            notNull (NotNull | None): NOT NULL 制約
        """
        self.notNullSql = notNull.toSql() if notNull else ""
    #---------------------------------------------------------------------------
    @private
    def __setUniqueSql(self, unique : Unique | None) -> None:
        """
        UNIQUE 制約をSQL文字列として設定する
        Args:
            unique (Unique | None): UNIQUE 制約
        """
        self.uniqueSql = unique.toSql() if unique else ""
    #---------------------------------------------------------------------------
    @private
    def __setForeignKeySql(self, foreignKey : ForeignKey | None) -> None:
        """
        FOREIGN KEY 制約をSQL文字列として設定する
        Args:
            foreignKey (ForeignKey | None): 外部キー制約
        """
        self.foreignKeySql = foreignKey.toSql() if foreignKey else ""
    #---------------------------------------------------------------------------
    @public
    def toSql(self):
        if hasattr(self, "tableName") and hasattr(self, "columnName"):
            sql = f"{self.tableName}.{self.columnName}"
        else:
            sql = f"{self.columnName}"
        return sql, []
    @public
    def like(self, value):
        """LIKE演算子"""
        return Condition(self.columnName, "LIKE", value)
    #---------------------------------------------------------------------------
    @public
    def In (self, *values):
        """IN演算子"""
        return Condition(self.columnName, "IN", values)
    #---------------------------------------------------------------------------
    @public
    def notIn (self, *values):
        """NOT IN演算子"""
        return Condition(self.columnName, "NOTIN", (values))
    #---------------------------------------------------------------------------
    @public
    def between(self, before, after):
        """BETWEEN演算子"""
        return Condition(self.columnName, "BETWEEN", (before, after))
    #---------------------------------------------------------------------------
    def __str__(self) -> str:
        return self.columnName
    #---------------------------------------------------------------------------
    def __eq__(self, value):
        """
        等価比較演算子 ==
        Returns:
            Condition : (columnName, '=', value)
        """
        return Condition(self.columnName, "=", value)
    #---------------------------------------------------------------------------
    def __ne__(self, value):
        """
        不等比較演算子 !=
        """
        return Condition(self.columnName, "!=", value)
    #---------------------------------------------------------------------------
    def __lt__(self, value):
        """
        小なり演算子 <
        """
        return Condition(self.columnName, "<", value)
    #---------------------------------------------------------------------------
    def __le__(self, value):
        """
        以下演算子 <=
        """
        return Condition(self.columnName, "<=", value)
    #---------------------------------------------------------------------------
    def __gt__(self, value):
        """
        大なり演算子 >
        """
        return Condition(self.columnName, ">", value)
    #---------------------------------------------------------------------------
    def __ge__(self, value):
        """
        以上演算子 >=
        """
        return Condition(self.columnName, ">=", value)
    #---------------------------------------------------------------------------
    def __and__(self, value):
        """
        AND演算子 AND
        """
        return ConditionGroup(self.columnName, "AND", value)
    #---------------------------------------------------------------------------
    def __or__(self, value):
        """
        OR演算子 OR
        """
        return ConditionGroup(self.columnName, "OR", value)
        
#-------------------------------------------------------------------------------
