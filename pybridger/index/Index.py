#-------------------------------------------------------------------------------
from ..common       import private # プライベートメソッド
from ..common       import public  # パブリックメソッド
from ..config       import Config  # コンフィグクラス
from ..column       import Column  # カラムクラス
from ..query        import Query   # クエリクラス
#-------------------------------------------------------------------------------
class Index:
    def __init__(
            self,
            indexName : str,
            *columns  : Column
        ) -> None:
        """
        インデックスの操作クラス
        Args:
            indexName (str)    : インデックス名
            *columns  (Column) : カラムオブジェクト
        Examples:
            ↓ インデックスインスタンスの作成
            index = Index("indexName", User.id, User.name)
            ↓ インデックスを作成
            index.create()
            ↓ インデックスを削除
            index.drop()
            ※ 各操作は自動でコミットされる
        """
        self.__indexName = indexName        # インデックス名
        self.__columns   = columns          # カラムオブジェクト群
        self.__sqlEngine = Config.sqlEngine # エンジンオブジェクト
    #---------------------------------------------------------------------------
    @ private
    def __columnsToSql(self) -> str:
        query = ""
        for col in self.__columns:
            if query == "":
                query += f"{col.tableName}("
            else:
                query += f"{col.columnName}, "
        else:
            query = query[:-2]
            query += ")"
        # User (id, name, ...)の形に成形して返す
        return query
    #---------------------------------------------------------------------------
    @ public
    def create(self) -> None:
        """
        インデックスの作成
        """
        # User (id, name, ...)の形を取得する
        colToSql = self.__columnsToSql()
        # クエリ
        query = f"CREATE INDEX {self.__indexName} ON {colToSql};"
        # エンジンが設定されていたら
        if not self.__sqlEngine is None:
            self.__sqlEngine.execute(Query(query))
            self.__sqlEngine.commit()
        else:
            raise Exception("エンジンが未設定です")
    #---------------------------------------------------------------------------
    @ public
    def drop(self) -> None:
        """
        インデックスの削除
        """
        # クエリ
        query = f"DROP INDEX IF NOT EXISTS {self.__indexName};"
        # エンジンが設定されていたら
        if not self.__sqlEngine is None:
            self.__sqlEngine.execute(Query(query))
            self.__sqlEngine.commit()
        else:
            raise Exception("エンジンが未設定です")  
#-------------------------------------------------------------------------------