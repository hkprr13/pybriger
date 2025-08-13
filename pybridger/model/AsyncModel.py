#-------------------------------------------------------------------------------
from .ModelMeta    import ModelMeta
from ..column      import Column
from ..common      import private
from ..common      import public
from ..constraints import Constraints
from ..manager     import Base 
from ..manager     import AsyncAlterTableAddColumn
from ..manager     import AsyncAlterTableAddConstraint
from ..manager     import AsyncAlterTableDropColumn
from ..manager     import AsyncAlterTableDropConstraint
from ..manager     import AsyncAlterTableRenameColumn
from ..manager     import AsyncCreateIndex
from ..manager     import AsyncCreateTable
from ..manager     import AsyncCreateTableIfNotExists
from ..manager     import AsyncCreateTrigger
from ..manager     import AsyncCreateView
from ..manager     import AsyncInsertRecord
from ..manager     import AsyncInsertRecords
from ..manager     import AsyncUpdateRecord
from ..manager     import AsyncUpdateRecords
from ..manager     import AsyncDeleteRecord
from ..manager     import AsyncDropIndex
from ..manager     import AsyncDropIndexIfExists
from ..manager     import AsyncDropTable
from ..manager     import AsyncDropTableIfExists
from ..manager     import AsyncDropTrigger
from ..manager     import AsyncDropTriggerIfNotExists
from ..manager     import AsyncDropView
from ..manager     import AsyncDropViewIfExists
from ..manager     import Select
#-------------------------------------------------------------------------------
class Model(metaclass = ModelMeta):
    """
    モデルクラスの基底クラス。

    Attributes:
        tableName (str)                     : テーブル名（クラス名から自動取得）
        columns   (list[dict[str, Column]]) : カラム定義のリスト
    """

    tableName : str                     # テーブル名
    columns   : list[dict[str, Column]] # カラム
    #---------------------------------------------------------------------------
    # プライベートメソッド
    #---------------------------------------------------------------------------
    @classmethod
    @private
    def __parameterColumnsToStrings(cls, columns :tuple[Column, ...]) -> str:
        cols = ""
        for col in columns:
            cols += col.columnName + ", "
        return cols[:-2]
    #---------------------------------------------------------------------------
    @classmethod
    @private
    def __columnsToQuery(cls):
        """
        カラムをSQL文にする
        テーブル作成時に使用する
        """
        cls.__foreignKeyList = [] # 外部キー定義リスト
        columnDefineLists    = [] # 各カラム定義
        # 各カラム定義をリストに追加
        for cols in cls.columns:
            columnSql = cls.__columnsToSql(cols)
            columnDefineLists.append(columnSql)
        # 外部キーがある場合、末尾に追加
        for fk in cls.__foreignKeyList:
            columnDefineLists.append(fk)
        return ", ".join(columnDefineLists)
    #---------------------------------------------------------------------------
    @classmethod
    @private
    def __columnsToSql(
            cls,
            columns : dict[str, Column]
        ) -> str:
        """
        カラムをSQL文にする
        columnsToQueryでのみ使用するプライベートメソッド
        Args:
            columns (dict[str, Column]) : カラム 
        Returns:
            Create文で使用するSQL文を返す
        """
        columnName, columnObject = next(iter(columns.items()))
        parts = []
        parts.append(columnName)
        # データ型
        if columnObject.dataTypeSql:
            parts.append(columnObject.dataTypeSql)
        # 主キー
        if columnObject.primaryKeySql:
            parts.append(columnObject.primaryKeySql)
        # デフォルト値
        if columnObject.defaultSql:
            parts.append(columnObject.defaultSql)
        # ユニーク設定
        if columnObject.uniqueSql:
            parts.append(columnObject.uniqueSql)
        # NotNull制約
        if columnObject.notNullSql:
            parts.append(columnObject.notNullSql)
        # 外部キー制約
        # 定義ある場合は別途保管 
        fk = cls.__foreignKeyToSql(columnName, columnObject)
        if fk:
            cls.__foreignKeyList.append(fk)        
        return " ".join(parts)
    #---------------------------------------------------------------------------
    @classmethod
    @private
    def __foreignKeyToSql(
            cls,
            columnName : str,
            columnObject : Column
        ) -> str:
        """
        外部キー制約の設定をSQL文として出力するプライベートメソッド
        Args:
            columnName   (str) : カラム名
            cokumnObject (str) : カラムオブジェクト
        Returns:
            fk : SQL文
        """
        fk = columnObject.foreignKeySql
        # リプレイスする
        if fk: fk = fk.replace("~~~", columnName)
        else:  fk = ""
        return fk
    #---------------------------------------------------------------------------
    # パブリックメソッド
    #---------------------------------------------------------------------------
    # CREATE系
    @classmethod
    @public
    async def createTable(cls) -> AsyncCreateTable:
        """
        テーブルを作成する
        Returns:
            CreateTable : テーブル作成クラス
        """
        columns = cls.__columnsToQuery()
        return AsyncCreateTable(
            tableName = cls.__name__, # テーブル名
            columns   = columns       # テーブル作成用カラム
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def createTableIfNotExists(cls) -> AsyncCreateTableIfNotExists:
        """
        テーブルが存在しない場合に作成する
        Returns:
            CreateTableIfNotExists : テーブル作成クラス
        """
        columns = cls.__columnsToQuery()
        return AsyncCreateTableIfNotExists(
            tableName = cls.__name__, # テーブル名
            columns   = columns       # テーブル作成用カラム
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def createIndex(
            cls,
            indexName : str,
            *columns  : Column
        ) -> AsyncCreateIndex:
        """
        インデックスを作成する
        Args:
            indexName (str)    : 作成するインデックス名
            *columns  (Column) : 対象とするカラム
        Returns:
            CreateIndex: インデックス作成処理オブジェクト
        Examples:
            ↓ インスタンスの作成
            user = User.createIndex("indexName", User.id, User.name)
            ↓ 実行とコミット
            user.execute()
            user.commit()
        """
        # カラムを文字列に変更する
        cols = cls.__parameterColumnsToStrings(columns)
        return AsyncCreateIndex(
            indexName = indexName,
            tableName = cls.__name__,
            columns   = cols
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    def createView(cls): ...
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def createTrigger(
            cls,
            triggerName : str,
            timing      : str,
            event       : str,
            body        : Base
        ):
        """
        トリガーの作成
        Args:
            triggerName (str) : トリガー名 
            timing      (str) : タイミング BEFORE AFTER
            event       (str) : イベント  INSERT UPDATE DELETE
            body        (str) : 実行するSQL文
        Examples:
            trigger = User.createTrigger(
                "tableName",
                "triggerName",
                "before | after",
                "inser | update | delete",
                User.InsertRecord(~~~)      <-実行したいものを入れる
            )
            trigger.execute()
            trigger.commit()
        """
        return AsyncCreateTrigger(
            tableName   = cls.__name__, # テーブル名
            triggerName = triggerName,  # トリガー名
            timing      = timing,       # イベントタイミング
            event       = event,        # イベント
            body        = body.query    # 実行するSQL
        )
    #---------------------------------------------------------------------------
    # DROP系
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def dropTable(cls) -> AsyncDropTable:
        """
        テーブルを削除する
        Example:
            user = User.dropTable()
            user.execute()
            user.commit()
        Returns:
            DropTable : テーブル削除クラス
        """
        return AsyncDropTable(
            tableName = cls.__name__
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def dropTableIfExists(cls) -> AsyncDropTableIfExists:
        """
        テーブルが存在する場合のみ削除する
        Example:
            user = User.dropTableIfExists()
            user.execute()
            user.commit()
        Returns:
            DropTableIfExists : テーブル削除クラス
        """
        return AsyncDropTableIfExists(
            tableName = cls.__name__
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def dropView(cls, viewName : str) -> AsyncDropView:
        """
        ビューの削除
        Args:
            viewName (str) : 削除するビュー名
        Example:
            user = User.dropView("view")
            user.execute()
            user.commit()
        Returns:
            DropView : ビュー削除クラス
        """
        return AsyncDropView(
            tableName = cls.__name__,
            viewName  = viewName
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def dropViewIfExist(cls, viewName : str) -> AsyncDropViewIfExists:
        """
        ビューが存在する場合削除する
        Args:
            viewName (str) : 削除するビュー名
        Example:
            user = User.dropView("view")
            user.execute()
            user.commit()
        Returns:
            DropViewIfExists : ビュー削除クラス
        """
        return AsyncDropViewIfExists(
            tableName = cls.__name__,
            viewName  = viewName
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def dropIndex(cls, indexName : str) -> AsyncDropIndex:
        """
        インデックス削除
        Args:
            indexName (str) : インデックス名
        Example:
            user = User.dropIndex("index")
            user.execute()
            user.commit()
        Returns:
            DropIndex : インデックス削除クラス
        """
        return AsyncDropIndex(
            tableName = cls.__name__,
            indexName = indexName
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def dropIndexIfNotExists(
            cls,
            indexName : str
        ) -> AsyncDropIndexIfExists:
        """
        インデックス削除
        Args:
            indexName (str) : インデックス名
        Example:
            user = User.dropIndexIfExists("index")
            user.execute()
            user.commit()
        Returns:
            DropIndexIfExists : インデックス削除クラス
        """
        return AsyncDropIndexIfExists(
            tableName = cls.__name__,
            indexName = indexName
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def dropTrigger(cls, triggerName : str) -> AsyncDropTrigger:
        """
        トリガーの削除
        Args:
            triggerName (str) : トリガー名
        Examples:
            user = User.dropTrigger("trigger")
            user.execute()
            user.commit()
        Returns:
            DropTrigger : トリガー削除オブジェクト
        """
        return AsyncDropTrigger(
            tableName   = cls.__name__,
            triggerName = triggerName
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def dropTriggerIfNotExists(
            cls,
            triggerName : str
        ) -> AsyncDropTriggerIfNotExists:
        """
        トリガーの削除
        Args:
            triggerName (str) : トリガー名
        Examples:
            user = User.dropTriggerIfNotExists("trigger")
            user.execute()
            user.commit()
        Returns:
            DropTriggerIfNotExists : トリガー削除オブジェクト
        """
        return AsyncDropTriggerIfNotExists(
            tableName   = cls.__name__,
            triggerName = triggerName
        )
    #---------------------------------------------------------------------------
    # INSERT/UPDATE/DELETE
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def insertRecord(cls, **columns) -> AsyncInsertRecord:
        """
        レコードを挿入
        Args:
            **columns : 例: id = 1, name = "name", age = 19...
        Examples:
            user = User.insertRecord(id = 1, name = "name", age = 19)
            user.execute()
            user.commit()

            Userテーブルにidが1, nameが"name", ageが19が挿入される
        Returns:
            InsertRecord : レコード挿入クラスを返す
        """
        cols         = "" # カラム
        placeHolders = "" # プレイスホルダー
        values       = [] # 値
        # id = 1, name = "name", age = 19...の形に成形
        # 値をストックに格納
        # カラム数に応じて, プレイスホルダー数を決定
        for key, value in columns.items():
            cols         += f"{key}, "
            placeHolders += "?, "
            values.append(value)
        return AsyncInsertRecord(
            tableName    = cls.__name__,     # テーブル名
            columns      = cols[:-2],        # id,name, ...の形で渡す, 末尾を削除
            values       = tuple(values),    # 値はタプルで渡す
            placeHolders = placeHolders[:-2] # プレイスホルダー, 末尾を削除
        )
        
    #---------------------------------------------------------------------------
    @classmethod    
    @public
    async def insertRecords(cls, **columns) -> AsyncInsertRecords:
        """
        レコードを複数挿入
        Args:
            **columns : 例: id   = [1,   2,   3  ],
                            name = ["a", "b", "c"],
                            age  = [19,  22,  17 ]
        Examples:
            user = User.insertRecord(
                id = [1, 2, 3], name = ["a", "b", "c"], age = [19, 22, 17]
            )
            user.execute()
            user.commit()

            ↓Userテーブルに
            |id|name|user|
            |1 |a   |19  |
            |2 |b   |22  |
            |3 |c   |17  | と複数レコードが挿入される
        Returns:
            InsertRecord : レコード複数挿入クラスを返す
        """
        cols         = "" # カラム
        placeHolders = "" # プレイスホルダー
        for key, values in columns.items(): # valuesは使わない
            cols         += f"{key}, "
            placeHolders += "?, "
        return AsyncInsertRecords(
            tableName    = cls.__name__,     # テーブル名
            columns      = cols[:-2],        # id,name, ...の形で渡す, 末尾を削除
            data         = list(        
                zip(*columns.values())       # 値はリストで渡す
            ), 
            placeHolders = placeHolders[:-2] # プレイスホルダー, 末尾を削除          
        )
    #---------------------------------------------------------------------------
    @classmethod    
    @public
    async def updateRecord(cls, **updateColumns) -> AsyncUpdateRecord:
        """
        レコードを更新
        Args:
            **updateColumns : 更新したいカラムを指定する
        Examples:
            user = User.updateRecord(name = "a", age = 20)
            user.where(id = 1)
            user.execute()
            user.commit()
        Returns:
            UpdateRecord : レコード更新クラスを返す 
        """
        cols   = "" # カラム
        values = [] # 値(リスト型)
        # id = ?, name = ?, age = ? の形に成型
        for key, value in updateColumns.items():
            cols += f"{key} = ?, "
            values.append(value)
        return AsyncUpdateRecord(
            tableName    = cls.__name__,    # テーブル名
            columns      = cols[:-2] + " ", # ←WHEREの前に空白を入れる用
            values       = tuple(values),   # タプルで渡す
        )
    #---------------------------------------------------------------------------
    @classmethod    
    @public
    async def updateRecords(cls, **updateColumns) -> AsyncUpdateRecords:
        """
        レコードを更新
        Args:
            **updateColumns : 更新したいカラムを指定する
        Examples:
            user = User.updateRecords(
                name = ["a","b","c"], age = [20,22,24]
            ).where(id = [1,2,3]) ※whereも忘れずに
            user.execute()
            user.commit()
        Returns:
            UpdateRecords : 複数レコード更新クラスを返す 
        """
        cols = "" # カラム
        for key, value in updateColumns.items(): # valueは使わない
            cols += f"{key} = ?, "
        return AsyncUpdateRecords(
            tableName = cls.__name__,    # テーブル名
            columns   = cols[:-2] + " ", # ←WHEREの前に空白を入れる用
            data      = list(zip(*updateColumns.values()))
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    async def deleteRecord(cls, **deleteColumns) -> AsyncDeleteRecord:
        """
        レコードを削除
        Args:
            **deleteColumns : 削除したいカラムを指定する
        Examples:
            user = User.deleteRecord(id = 1) ※複数指定不可
            user.execute()
            user.commit()
        Returns:
            DeleteRecord : レコード削除クラスを返す
        """
        cols    = "" # カラム
        values = [] # 値(リスト型)
        # id = ? の形に成型
        for key, value in deleteColumns.items():
            cols += f"{key} = ?, "
            values.append(value)
        return AsyncDeleteRecord(
            tableName = cls.__name__,    # テーブル名
            columns   = cols[:-2] + " ", # <-WHEREの前に空白を入れる用
            values    = tuple(values)    # タプルで渡す
        )
    #---------------------------------------------------------------------------
    # ALTER系
    #---------------------------------------------------------------------------
    @classmethod
    @public
    def alterTableAddColumn(
            cls,
            **column : Column
        ) -> AsyncAlterTableAddColumn:
        """
        テーブルにカラムを追加する
        Args:
            column (Column) : カラム
        Examples:
            user = User.alterTableAddColumn(age = Column(Integer()))
            user.execute()
            user.commit()
        Returns:
            AlterTableAddColumn : カラム追加クラス
        """
        columnName   : str    # カラム名
        columnObject : Column # カラムオブジェクト
        # カラム
        for key, value in column.items():
            columnName   = key
            columnObject = value
        # 条件
        constraints = f"{columnObject.notNullSql} "\
                    + f"{columnObject.notNullSql} "\
                    + f"{columnObject.uniqueSql}"
        return AsyncAlterTableAddColumn(
            tableName   = cls.__name__,             # テーブル名
            column      = columnName,               # カラム名
            dataType    = columnObject.dataTypeSql, # データ型
            constraints = constraints               # 制約
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    def alterTableDropColumn(
            cls,
            column : Column
        ) -> AsyncAlterTableDropColumn:
        """
        テーブルからカラムを削除する
        Args:
            column (Column) : カラム
        Examples:
            user = User.alterTableDropColumn(User.age)
            user.execute()
            user.commit()
        Returns:
            AlterTableDropColumn : カラム削除クラス
        """
        return AsyncAlterTableDropColumn(
            tableName  = cls.__name__,     # テーブル名
            columnName = column.columnName # カラム名
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    def alterTableRenameColumn(
            cls,
            oldName : str,
            newName : str
        ) -> AsyncAlterTableRenameColumn:
        """
        テーブルのカラム名を変更
        Args:
            oldName (str) : 既存の名前 
            newName (str) : 新しい名前
        Examples:
            user = User.alterTableRenameColumn("email", "address")
            user.execute()
            user.commit()
        Returns:
            AlterTableRenameColumn : カラム名変更クラス
        """
        return AsyncAlterTableRenameColumn(
            tableName = cls.__name__,
            oldName   = oldName,
            newName   = newName
        )
    #---------------------------------------------------------------------------
    @classmethod
    @public
    def alterTableAddConstraint(cls,**constraints : Constraints): ...
    #---------------------------------------------------------------------------
    @classmethod
    @public
    def alterTableDropConstraint(cls): ...
    #---------------------------------------------------------------------------
    @classmethod
    @public
    def alterView(cls): ...
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    @classmethod
    @public
    def fromDict(cls, data : dict):
        instance = cls()
        for key, value in data.items():
            if hasattr(isinstance, key):
                setattr(instance, key, value)
        return instance
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    def __and__(self, other):
        return f"{self} {other}"
#-------------------------------------------------------------------------------