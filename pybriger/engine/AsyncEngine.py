#-------------------------------------------------------------------------------
from .base     import AsyncMySqlEngine
from .base     import AsyncSqlite3Engine
from ..common  import public          #パブリックメソッド
from ..column  import Column
from ..model   import Model           # モデルクラス
from ..manager import Select          # SELECT句クラス
from ..config  import Config
#-------------------------------------------------------------------------------
class AsyncEngine:
    """
    SQLエンジンを初期化・管理するためのクラス
    データベースの接続設定、エンジンの初期化、SQL発行に必要な
    各種情報の取得・設定を提供する
    """
    #---------------------------------------------------------------------------
    def __init__(
            self,
            sqlEngineName : str,
            hostName      : str | None = None,
            userName      : str | None = None,
            password      : str | None = None,
            database      : str | None = None
        ):
        """
        エンジンを初期化し、接続情報を登録する。
        Parameters:
            sqlEngineName (str) : 使用するエンジン名
            hostName      (str) : ホスト名
            userName      (str) : ユーザー名
            password      (str) : パスワード
            databaseName  (str) : データベース名またはDBファイルパス
        """
        self.sqlEngineName = sqlEngineName 
        self.hostName      = hostName
        self.userName      = userName
        self.password      = password
        self.database      = database
    #---------------------------------------------------------------------------
    @public
    async def launch(self) -> None:
        """
        SQLエンジンをエンジン名に応じて初期化する
        Raises:
            ModuleNotFoundError : 未対応のエンジン名が指定された場合
        """
        if self.sqlEngineName == "sqlite3":
            if self.database:
                self.sqlEngine = AsyncSqlite3Engine(
                    databasePath = self.database
                )
            raise Exception("データベースを指定してください")
        elif self.sqlEngineName == "mysql":
            if  self.hostName and self.userName \
            and self.password and self.database:
                self.sqlEngine = AsyncMySqlEngine(
                    hostName     = self.hostName,
                    userName     = self.userName,
                    password     = self.password,
                    databaseName = self.database
                )
            else:
                raise Exception("引数を指定ください")
        else:
            raise ModuleNotFoundError("未対応のモジュールエンジンです")
        Config.asyncSqlEngine = self.sqlEngine
        Config.database       = self.database
    #---------------------------------------------------------------------------
    @public
    async def commit(self) -> None:
        """
        トランザクションをコミットする
        """
        await self.sqlEngine.commit()
    #---------------------------------------------------------------------------
    @public
    async def connectOpen(self) -> None:
        """
        データベース接続を開始する
        """
        await self.sqlEngine.connectOpen()
    #---------------------------------------------------------------------------
    @public
    async def connectClose(self) -> None:
        """
        データベース接続を閉じる
        """
        await self.sqlEngine.connectClose()
    #---------------------------------------------------------------------------