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
    """
    CSVファイルをデータベースにインポート/エクスポートするクラス
    """
    #---------------------------------------------------------------------------
    def __init__(self) -> None:
        ...
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
    def createTable(
            self,
            inputFilePath  : str,
            outputFilePath : str
        ) -> None:
        tableName, columnDefines = self.__makeColumnDefines(inputFilePath)
        with open(
            outputFilePath, mode = "w", newline = "", encoding = "utf-8"
        ) as f:
            w = f.write
            w(f"from pybridger import *\n")
            w(f"\n")
            w(f"engine = Engine() # 引数を設定してください\n")
            w(f"engine.launch()\n")
            w(f"\n")
            w("# テーブル定義\n")
            w(f"class {tableName}(Model):\n    ")
            line = self.__makeColumnLinesOfTable(columnDefines)
            w(line[:-4])
            w("# テーブル作成\n")
            w(f"{tableName.lower()} = {tableName}.createTable()\n")
            w(f"{tableName.lower()}.execute()\n")
            w(f"{tableName.lower()}.commit()\n")
    #---------------------------------------------------------------------------
    @private
    def __makeColumnLinesOfTable(self, columnDefines : list[str]):
        line = ""
        for col in columnDefines:
            l = f"{col[0]} = Column(dataType = "
            # データ型
            dataType = col[1]
            if dataType == "int":
                l += "Integer(), "
            elif dataType == "str":
                l += "Text(), "
            elif dataType == "bool":
                l += "Boolean(), "
            elif dataType == "float":
                l += "Float(), "
            elif dataType == "datetime":
                l += "DateTime(), "
            elif dataType == "time":
                l += "Time(), "
            # 主キー
            primaryKey = col[2]
            if primaryKey.lower() == "true":
                l += "isPrimaryKey = True, "
            elif primaryKey.lower() == "false":
                l += "isPrimaryKey = False, "
            # 自動採番
            autoIncrement = col[3]
            if autoIncrement.lower() == "true":
                l += "isAutoIncrement = True, "
            elif autoIncrement.lower() == "false":
                l += "isAutoIncrement = False, "
            # デフォルト値
            default = col[4]
            if default:
                l += f"Defalut('{default}'), "
            # NotNull
            notNull = col[5]
            if notNull.lower() == "true":
                l += "notNull = NotNull(True), "
            elif notNull.lower() == "false":
                l += "notNull = NotNull(False), "
            # ユニーク
            unique = col[6]
            if unique.lower() == "true":
                l += "unique = Unique(True), "
            elif unique.lower() == "false":
                l += "unique = Unique(False), "
            # チェック
            check = col[7]
            if check:
                l += f"check = Check('{check}'), "                      
            # テーブルレベルのチェック
            tableLevelCheck = col[8]
            if tableLevelCheck:
                l += f"tableLevelCheck = TableLevelCheck('{tableLevelCheck}'), "       
            # 外部キー
            foreignKey = col[9]
            if foreignKey:
                l += f"foreignKey = ForeignKey('{foreignKey}'), "
            l = l[:-2] + ") \n    "
            line += l
        return line
    #---------------------------------------------------------------------------
    @private
    def __makeColumnDefines(
            self, filePath : str
        ) -> tuple[str, list[str]]:
        with open(filePath, mode = "r", newline = "", encoding = "utf-8") as f:
            # 先頭行の取得
            headerLine : str = f.readline().strip()
            # 先頭行(設定されたカラム)をリスト化
            columns : list = headerLine.split(",")
            # テーブル名の取得(csvの0,0の場所)し、columnsをカラムのみにする
            tableName : str  = columns.pop(0)
            # カラムの定義
            columnDefines = [columns]
            for line in f.readlines():
                lines :str = line.strip()
                lineParts : list = lines.split(",")
                columnDefines.append(lineParts[1:])
            cols = []
            # 縦横を入れ替える
            for i in (map(list, zip(*columnDefines))):
                cols.append(i)
            return tableName, cols
    #---------------------------------------------------------------------------
    @public
    def importToDatabase(self, filePath : str, model : type[Model]):
        """
        CSVファイルをデータベースにインポートする
        """
        # CSVファイルの読み込みと分離
        self.__tableName = model.tableName
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
    def exportFromDatabase(self,  filePath : str, model : type[Model]):
        """
        データベースをCSVファイルにエクスポートする
        """
        self.__tableName = model.tableName
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
