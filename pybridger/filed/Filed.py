#-------------------------------------------------------------------------------
from ..datatypes.DataType import DataType    # データ型　<-インポートエラー回避
from ..column             import Column      # カラムクラス
from ..constraints        import Default     # デフォルト値クラス
from ..constraints        import NotNull     # NotNullクラス
from ..constraints        import Unique      # ユニーク設定クラス
from ..constraints        import ForeignKey  # 外部キー制約クラス
from ..common             import private     # プライベートメソッド
from ..common             import override    # オーバライドメソッド 
#-------------------------------------------------------------------------------
class Filed(Column):
    """
    フィールドクラスの基底クラス
    カラムクラスを継承する。カラムクラスより設定に制限あり
    """
    def __init__(
            self,
            dataType        : DataType,
            isPrimaryKey    : bool       = False,
            isNotNull       : bool       = False,
            isUnique        : bool       = False,
            isAutoincrement : bool       = False,
            default         : str | None = None,
            foreignKey      : str | None = None
        ) -> None:
        # 制約
        self.dataType        = dataType
        self.isPrimaryKey    = isPrimaryKey
        self.isNotNull       = isNotNull
        self.isUnique        = isUnique
        self.isAutoincrement = isAutoincrement
        self.default         = default
        self.foreignKey      = foreignKey
        #
        self.columnName  : str
        self.tableName   : str
        self.dataTypeSql : str    
    #---------------------------------------------------------------------------
    @override
    @private
    def setDataTypeSql(self) -> None: ...
    #---------------------------------------------------------------------------
    @override
    @private
    def setPrimaryKeySql(self) -> None:
        return super().setPrimaryKeySql(self.isPrimaryKey)
    #---------------------------------------------------------------------------
    @override
    @private
    def setDefaultSql(self) -> None:
        return super().setDefaultSql(
            Default(self.default)
        )
    #---------------------------------------------------------------------------
    @override
    @private
    def setNotNullSql(self) -> None:
        return super().setNotNullSql(
            NotNull(self.isNotNull)
        )
    #---------------------------------------------------------------------------
    @override
    @private
    def setUniqueSql(self) -> None:
        return super().setUniqueSql(
            Unique(self.isUnique)
        )
    #---------------------------------------------------------------------------
    @override
    @private
    def setForeignKeySql(self) -> None:
        if self.foreignKey is None:
            foreignKey = None
        else:    
            foreignKey = ForeignKey(
                referenceName = self.foreignKey,
                onUpdate      = None,
                onDelete      = None
            )
        return super().setForeignKeySql(
            foreignKey = foreignKey
        ) 
#-------------------------------------------------------------------------------
