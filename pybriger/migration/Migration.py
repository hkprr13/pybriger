#-------------------------------------------------------------------------------
import os 
import sys
import importlib.util
from datetime import datetime
from ..engine import MySqlEngine
from ..engine import Sqlite3Engine
from ..model import Model
from ..common import public
from ..common import private
from ..column import Column
from ..constraints import Unique
from ..datatypes import Integer
from ..datatypes import Text
from ..config import Config
#-------------------------------------------------------------------------------
class Migration:
    def __init__(
            self,
            migrationsDir : str
        ) -> None:
        """
        マイグレーションクラスの初期化
        Args:
            migrationsDir (str) : マイグレーションディレクトリのパス
        """
        super().__init__()
        self.__migrationsDir = migrationsDir
        os.makedirs(migrationsDir, exist_ok = True)
        self.__sqlEngine.execute(self.__buildCreateTableSql())
        self.__sqlEngine.commit()
        print("初期化完了")
    #---------------------------------------------------------------------------
    @private
    def __buildCreateTableSql(self):
        query = "CREATE TABLE IF NOT EXISTS migration (" \
            + "id INTEGER PRIMARY KEY auto_increment, " \
            + "name text, applied_at TEXT)"
        # MySQLの場合
        if isinstance(self.__sqlEngine,MySqlEngine):
            query = query.replace(
                "auto_increment", "AUTO_INCREMENT"
            )
            query = query.replace(
                "text", "VARCHAR(255) UNIQUE"
            )
        # SQLite3の場合
        elif isinstance(self.__sqlEngine,Sqlite3Engine):
            query = query.replace(
                "auto_increment", "AUTOINCREMENT"
            )
            query = query.replace(
                "text", "TEXT"
            )
        else:
            raise Exception("エンジンが未設定です")
        return query
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
    def make(self, name : str) -> None:
        """
        新しいマイグレーションファイルを作成する
        Args:
            name (str) : マイグレーション名
        """
        timeStamp = datetime.now().strftime("%Y%m%d%H%M%S")
        fileName  = f"{timeStamp}_{name.replace('', '_')}.py"
        filePath  = os.path.join(self.__migrationsDir, fileName)
        templete = f"""\
def upgrade(engine):
    # ここにスキーマ変更SQLを記述
    pass
def downgrade(engine):
    # 元に戻すSQLを記述
    pass
"""
        with open(filePath, "w", encoding = "utf-8") as f:
            f.write(templete)
        print(f"{filePath}を作成しました")
    #---------------------------------------------------------------------------
    def history(self) -> list:
        """
        適用済みのマイグレーション一覧を返す
        Returns:
            list[str] : ファイル名のリスト
        """
        cur = self.__sqlEngine.cursor()
        cur.execute("SELECT name FROM migration ORDER BY id")
        rows = cur.fetchall()
        return []
#-------------------------------------------------------------------------------