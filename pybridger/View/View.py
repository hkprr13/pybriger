#-------------------------------------------------------------------------------
import csv                         # csvライブラリのインポート
from ..common     import private   # プライベートメソッド
from ..common     import public    # パブリックメソッド
from ..config     import Config    # コンフィグクラス
from ..column     import Column    # カラムクラス
from ..conditions import Condition # 条件クラス
from ..query      import Query     # クエリクラス
#-------------------------------------------------------------------------------
class View:
    """
    ビュー操作クラス
    Attributes:
        __viewName   (str)                         : ビュー名
        __conditions (Condition)                   : 条件式オブジェクト
        __columns    (Column)                      : カラムオブジェクト
        __sqlEngine  (Sqlite3Engine | MySqlEngine) : エンジンオブジェクト
    """
    #---------------------------------------------------------------------------
    def __init__(
            self,
            viewName   : str,
            conditions : Condition,
            *columns   : Column
        ) -> None:
        """
        ビューの操作をする
        Args:
            viewName   (str)       : ビュー名
            conditions (Condition) : 条件式 例: User.age >= 20
            *columns   (Column)    : カラム
        Examples:
            view = View("viewName", User.age >= 20, User.id, User.name)
        """
        self.__viewName   = viewName
        self.__conditions = conditions
        self.__columns    = columns
    #---------------------------------------------------------------------------
    @property
    @private
    def __sqlEngine(self):
        """
        sqlエンジンの設定
        """
        engine = Config.sqlEngine
        if engine is None:
            raise Exception("エンジンが未設定です")
        return engine
    #---------------------------------------------------------------------------
    @ private
    def __bulidSelectQuery(self) -> str:
        # クエリ
        query = "SELECT " # 末尾にスペース
        # テーブル名
        tableName = ""
        # カラム名を取得する
        for col in self.__columns:
            tableName = col.tableName
            query += f"{col.columnName}, " # 末尾にスペース
        else:
            # 末尾とカンマを消す
            query = query[:-2]
            # 成形する
            query += f" FROM {tableName} WHERE {self.__conditions}"
        # SELECT id, name FROM User WHERE age >= 10 の形式で返す
        return query
    #---------------------------------------------------------------------------
    @public
    def create(
            self,
            replace             : bool = False,
            checkOption         : bool = False,
            localCheckOption    : bool = False,
            cascadedCheckOption : bool = False,
            securityDefiner     : bool = False,
            readOnly            : bool = False
        ):
        """
            データベースにビューを作成する
            ※出力はしない
            Args:
                replace             (bool) : 既存のビューを置き換える
                checkOption         (bool) : ビューを通した更新を制限
                localCheckOption    (bool) : ネストビューで自分自身の条件のみを強制
                cascadedCheckOption (bool) : ネストビューすべての条件を強制
                securityDefiner     (bool) : ビューを作成したユーザ権限で実行
                readOnly            (bool) : ビューから書き込み操作を禁止
            Examples:
                view = View("viewName", User.age >= 10, User.id, User.name)
                view.create(replece = True, checkOption = True)
        """
        # クエリ
        query     = f"CREATE " # 末尾にスペース
        # セレクト句
        selectSql = self.__bulidSelectQuery()
        # リプレイスビューが有効なら
        if replace == True:
            query += "OR REPLACE " # 末尾にスペース
        # CREATE VIEW viewName AS SELECT id, name FROM User WHWRE age >= 10
        query += f"VIEW {self.__viewName} AS {selectSql} " # 末尾にスペース
        # オプション句の構築
        withClaises = []
        # チェックオプションが有効なら
        if checkOption:
            withClaises.append("CHECK OPTION")
        # ローカルチェックオプションが有効なら
        if localCheckOption:
            withClaises.append("LOCAL CHECK OPTION")
        # カスケードチェックオプションが有効なら
        if cascadedCheckOption:
            withClaises.append("CASCADED CHECK OPTION")
        # セキュリティーデフェンダーが有効なら
        if securityDefiner:
            withClaises.append("SECURITY DEFINER")
        # 読み取り専用が有効なら
        if readOnly:
            withClaises.append("READ ONLY")
        # オプション句リストが空ではなければ
        if withClaises:
            query += f"WITH {' '.join(withClaises)}"
            query += ";"
        else:
            query = query[:-1] + ";" # 末尾にスペースを削除する
        self.__sqlEngine.execute(query = Query(query))
        self.__sqlEngine.commit()
    #---------------------------------------------------------------------------
    @public
    def show(self) -> list:
        """
        ビューの表示
        Returns:
            ビューのイテレーターを返す
        """
        # クエリ
        query = f"SELECT * FROM {self.__viewName};"
        cur = self.__sqlEngine.cursor()
        cur.execute(query)
        # リストで返す
        return cur.fetchall()
    #---------------------------------------------------------------------------
    @public
    def drop(self):
        """
        ビューの削除
        """
        # クエリ
        query = f"DROP VIEW IF EXISTS {self.__viewName};"
        self.__sqlEngine.execute(query = Query(query))
        self.__sqlEngine.commit()
    #---------------------------------------------------------------------------
    @public
    def makeCSV(
            self,
            filePath      : str,
            includeHeader : bool = True,
            encoding      : str = "utf-8"
        ):
        """
        ビュー内容をCSVファイルとして出力する
        Args:
            filePath      (str)  : 出力先のCSVファイルパス(.csv不要)
            includeHeader (bool) : ヘッダー行(カラム名)を含んで出力するか
            ncoding       (str)  : 出力ファイルの文字コード
        Raises:
            Exception : エンジンが未設定またはクエリ失敗時
        """
        # カーソルの設定
        cur = self.__sqlEngine.cursor()
        cur.execute(f"SELECT * FROM {self.__viewName};") # ビュー名で指定
        # 出力に失敗時に戻り値を返す
        if cur.description is None:
            print("出力に失敗しました")
            return
        # カラム名の取得
        columnNames = [description[0] for description in cur.description]
        # データ行の取得
        rows = cur.fetchall()
        # ファイルに書き込み
        try:
            with open(
                file    = f"{filePath}.csv", mode     = "w",
                newline = "",                encoding = encoding
            ) as f:
                writer = csv.writer(f)
                # ヘッダー行フラグが真なら
                if includeHeader:
                    writer.writerow(columnNames) # ヘッダー行あり
                writer.writerows(rows)           # データ行
            print("出力に成功しました")
        except Exception as e:
            print(e)            
#-------------------------------------------------------------------------------