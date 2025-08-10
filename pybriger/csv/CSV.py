#-------------------------------------------------------------------------------
import csv
from typing   import cast, Any      # 型チェック用
from ..common import public         # パブリックメソッド
from ..common import private        # プライベートメソッド
from ..config import Config         # コンフィグクラス
from ..model  import Model          # モデルクラス
from ..engine import MySqlEngine    # MySQLエンジンクラス
from ..engine import Sqlite3Engine  # Sqlite3エンジンクラス
#-------------------------------------------------------------------------------
class CSV:
    #---------------------------------------------------------------------------
    def __init__(self, model : type[Model]) -> None:
        self.__model     = model
        self.__tableName = self.__model.tableName
    #---------------------------------------------------------------------------
    @property
    @public
    def sqlEngine(self):
        """sqlエンジンの設定"""
        engine = Config.sqlEngine
        if engine is None:
            raise Exception("エンジンが未設定です")
        return engine
    #---------------------------------------------------------------------------
    @property
    @public
    def database(self):
        """データベースの設定"""
        database = Config.database
        if database is None:
            raise Exception("データベースが未設定です")
        return database
    #---------------------------------------------------------------------------
    @public
    def createTable(self):
        try:
            self.__model.createTableIfNotExists()
        except:
            raise Exception("テーブルの作成に失敗しました")
    #---------------------------------------------------------------------------
    @public
    def importToDatabase(self, filePath : str):
        """
        CSVファイルをデータベースにインポートする
        """
        # CSVファイルの読み込みと分離
        header, data = self.__parseCSV(filePath)
        # DB側のカラムと照合
        dbColumns = self.__getTableColumns()
        if not set(header) == set(dbColumns):
            raise Exception("CSVファイルのヘッダーとDBのカラムが一致していません")
        # プレイスホルダー
        placeHolders = "(" \
                     + ", ".join([self.sqlEngine.PLACEHOLDER * len(header)]) \
                     + ")"
        # カラムのSQL
        columnsSql = "(" \
                   + ", ".join([f"{col}" for col in header]) \
                   + ")"
        # クエリ
        query = f"INSERT INTO {self.__tableName} " \
              + f"{columnsSql} VALUES {placeHolders}"
        # クエリの実行
        try:
            self.sqlEngine.executeAny(query, data)
            self.sqlEngine.commit()
        except Exception as e:
            self.sqlEngine.rollback()
            raise Exception(f"データの挿入に失敗しました: {e}")
    #---------------------------------------------------------------------------
    @public
    def exportFromDatabase(self,  filePath : str):
        """
        データベースをCSVファイルにエクスポートする
        """
        # クエリ
        query = f"SELECT * FROM {self.__tableName};"
        cur = self.sqlEngine.cursor()
        cur.execute(query)
        data = cur.fetchall()
        # CSVに書き込む
        with open(filePath, mode = "w", newline = "", encoding = "utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.__getTableColumns())
            writer.writerows(data)
        print(f"{filePath}を作成しました")
    #---------------------------------------------------------------------------
    @private
    def __parseCSV(self, filePath : str) -> tuple[list[str], list[tuple]]:
        try:
            with open(filePath, newline = "", encoding= "utf-8") as csvFile:
                reader = csv.reader(csvFile)
                header = next(reader)
                if not header:
                    raise ValueError("CSVファイルにヘッダーが存在しません")
                data = []
                for row in reader:
                    if not len(row) == len(header):
                        raise ValueError("CSVの行とヘッダーの列数が一致しません")
                    data.append(tuple(row))
                return header, data
        except FileNotFoundError:
            raise FileNotFoundError("CSVファイルが存在しません")
        except StopIteration:
            raise ValueError("CSVファイルが空です")
        except Exception as e:
            raise Exception(f"CSVファイルの読み込みに失敗しました: {e}")
    #---------------------------------------------------------------------------
    @private
    def __getTableColumns(self):
        # MYSQLの場合
        if isinstance(self.sqlEngine, MySqlEngine):
            # クエリ
            query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
                  + f"WHERE TABLE_SCHEMA = {self.sqlEngine.PLACEHOLDER}" \
                  + f"AND TABLE_NAME = {self.sqlEngine.PLACEHOLDER};"
            cur = self.sqlEngine.cursor(dictionary = True)
            cur.execute(query, (self.database, self.__tableName))
            # 型チェック
            rows = cast(list[dict[str, Any]], cur.fetchall())
            return [row["COLUMN_NAME"] for row in rows]
        # Sqlite3の場合
        elif isinstance(self.sqlEngine, Sqlite3Engine):
            # クエリ
            query = f"PRAGMA table_info({self.__tableName});"
            cur = self.sqlEngine.cursor()
            cur.execute(query)
            return [row[1] for row in cur.fetchall()]
        else:
            raise Exception("エンジンが未設定です")
#-------------------------------------------------------------------------------