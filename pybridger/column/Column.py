#-------------------------------------------------------------------------------
from ..datatypes.DataType import DataType           # データ型
from ..constraints        import AutoIncrement      # 自動採番 
from ..constraints        import PrimaryKey         # 主キークラス
from ..constraints        import Default            # デフォルト値クラス
from ..constraints        import NotNull            # NotNullクラス
from ..constraints        import Unique             # ユニーク設定クラス
from ..constraints        import Check              # CHECK制約クラス
from ..constraints        import TableLevelCheck    # CHCEK制約(テーブルレベル)
from ..constraints        import ForeignKey         # 外部キー制約クラス
from ..common             import public             # パブリックメソッド
from ..common             import private            # プライベートメソッド
from ..conditions         import Condition          # 条件クラス
from ..conditions         import ConditionGroup     # 条件クラス
#-------------------------------------------------------------------------------
class Column:
    """
    SQLのカラムを定義するためのクラス
    Attributes:
        columnName      (str)         : カラム名（Modelクラス側で自動設定）
        tableName       (str)         : テーブル名（Modelクラス側で自動設定）
        dataType        (DataType)    : カラムのデータ型
        dataTypeSql     (str)         : SQL用のデータ型文字列
        primaryKeySql   (str)         : PRIMARY KEY制約のSQL文字列
        defaultSql      (str)         : DEFAULT制約のSQL文字列
        notNullSql      (str)         : NOT NULL制約のSQL文字列
        uniqueSql       (str)         : UNIQUE制約のSQL文字列
        checkSql        (str)         : CHECK制約
        tableLevelCheck (str)         : テーブルレベルのCHECK制約
        foreignKeySql   (str)         : FOREIGN KEY制約のSQL文字列
    """
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    def __init__(
        self,
        dataType        : DataType,
        isPrimaryKey    : bool                   = False,
        isAutoIncrement : bool                   = False,
        default         : Default         | None = None,
        notNull         : NotNull         | None = None,
        unique          : Unique          | None = None,
        check           : Check           | None = None,
        tableLevelCheck : TableLevelCheck | None = None,
        foreignKey      : ForeignKey      | None = None
    ):
        """
        カラム情報を初期化する
        Args:
            dataType        (DataType)           : カラムのデータ型
            isPrimaryKey    (bool)               : 主キー
            isAutoIncrement (bool)               : 自動採番
            default         (Default    | None)  : デフォルト値
            notNull         (NotNull    | None)  : NOT NULL制約
            unique          (Unique     | None)  : UNIQUE制約
            check           (Check      | None)  : CHECK制約
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
        self.setDataTypeSql(dataType)
        self.setPrimaryKeySql(isPrimaryKey)
        self.setAutoIncrement(isAutoIncrement)
        self.setDefaultSql(default)
        self.setNotNullSql(notNull)
        self.setUniqueSql(unique)
        self.setCheckSql(check)
        self.setTableLevelCheckSql(tableLevelCheck)
        self.setForeignKeySql(foreignKey)
        # カラム名とテーブル名
        self.columnName : str
        self.tableName  : str 
    #---------------------------------------------------------------------------
    @public
    def setDataTypeSql(self, dataType: DataType | None) -> None:
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
    @public
    def setPrimaryKeySql(self, isPrimaryKey : bool) -> None:
        """
        PRIMARY KEY制約をSQL文字列として設定する
        Args:
            isPrimaryKey (bool): 主キーにするかどうか
        """
        if isPrimaryKey:
            self.primaryKeySql = PrimaryKey().toSql()
        else:
            self.primaryKeySql = ""
    #---------------------------------------------------------------------------
    @public
    def setAutoIncrement(self, isAutoIncrement : bool ) -> None:
        """
        AUTO INCREMENT制約をSQL文字列として設定する
        Args:
            isAutoIncrement (bool) : 自動採番するかどうか
        """
        if isAutoIncrement:
            self.autoIncrementSql = AutoIncrement().toSql()
        else:
            self.autoIncrementSql = ""
    #---------------------------------------------------------------------------
    @public
    def setDefaultSql(self, default : Default | None) -> None:
        """
        DEFAULT制約をSQL文字列として設定する
        Args:
            default (Default | None): デフォルト値
        """
        self.defaultSql = default.toSql() if default else ""
    #---------------------------------------------------------------------------
    @public
    def setNotNullSql(self, notNull : NotNull | None) -> None:
        """
        NOT NULL制約をSQL文字列として設定する
        Args:
            notNull (NotNull | None): NOT NULL制約
        """
        self.notNullSql = notNull.toSql() if notNull else ""
    #---------------------------------------------------------------------------
    @public
    def setUniqueSql(self, unique : Unique | None) -> None:
        """
        UNIQUE制約をSQL文字列として設定する
        Args:
            unique (Unique | None): UNIQUE制約
        """
        self.uniqueSql = unique.toSql() if unique else ""
    #---------------------------------------------------------------------------
    @public
    def setCheckSql(self, check : Check | None) -> None:
        """
        CHECK制約をSQL文字列として設定する
        Args:
            check (CHECK | None) : CHECK制約
        """
        self.checkSql = check.toSql() if check else ""
    #---------------------------------------------------------------------------
    @public
    def setTableLevelCheckSql(
            self,
            tableLevelCheck : TableLevelCheck | None
        ) -> None:
        """
        CHECK制約をSQL文字列として設定する
        Args:
            check (CHECK | None) : CHECK制約
        """
        if tableLevelCheck:
            self.tableLevelCheckSql = tableLevelCheck.toSql()
        else:
            self.tableLevelCheckSql = ""
    #---------------------------------------------------------------------------
    @public
    def setForeignKeySql(self, foreignKey : ForeignKey | None) -> None:
        """
        FOREIGN KEY制約をSQL文字列として設定する
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
    #---------------------------------------------------------------------------
    @public
    def like(self, value):
        """LIKE演算子"""
        return Condition(self.tableName, self.columnName, "LIKE", value)
    #---------------------------------------------------------------------------
    @public
    def In (self, *values):
        """IN演算子"""
        return Condition(self.tableName, self.columnName, "IN", values)
    #---------------------------------------------------------------------------
    @public
    def notIn (self, *values):
        """NOT IN演算子"""
        return Condition(self.tableName, self.columnName, "NOTIN", (values))
    #---------------------------------------------------------------------------
    @public
    def between(self, before, after):
        """BETWEEN演算子"""
        return Condition(
            self.tableName, self.columnName, "BETWEEN", (before, after)
        )
    #---------------------------------------------------------------------------
    def __str__(self) -> str:
        return self.columnName
    #---------------------------------------------------------------------------
    def __eq__(self, value):
        """
        等価比較演算子 ==
        """
        return Condition(self.tableName, self.columnName, "=", value)
    #---------------------------------------------------------------------------
    def __ne__(self, value):
        """
        不等比較演算子 !=
        """
        return Condition(self.tableName, self.columnName, "!=", value)
    #---------------------------------------------------------------------------
    def __lt__(self, value):
        """
        小なり演算子 <
        """
        return Condition(self.tableName, self.columnName, "<", value)
    #---------------------------------------------------------------------------
    def __le__(self, value):
        """
        以下演算子 <=
        """
        return Condition(self.tableName, self.columnName, "<=", value)
    #---------------------------------------------------------------------------
    def __gt__(self, value):
        """
        大なり演算子 >
        """
        return Condition(self.tableName, self.columnName, ">", value)
    #---------------------------------------------------------------------------
    def __ge__(self, value):
        """
        以上演算子 >=
        """
        return Condition(self.tableName, self.columnName, ">=", value)
    #---------------------------------------------------------------------------
    def __and__(self, value):
        """
        AND演算子 AND
        """
        return ConditionGroup(self.tableName, self.columnName, "AND", value)
    #---------------------------------------------------------------------------
    def __or__(self, value):
        """
        OR演算子 OR
        """
        return ConditionGroup(self.tableName, self.columnName, "OR", value)
#-------------------------------------------------------------------------------
