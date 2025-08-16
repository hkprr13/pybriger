#-------------------------------------------------------------------------------
from __future__ import annotations # 循環インポートを回避する用
from typing import TYPE_CHECKING   
#-------------------------------------------------------------------------------
if TYPE_CHECKING:
    from ..engine import Sqlite3Engine      # 
    from ..engine import AsyncSqlite3Engine #
    from ..engine import MySqlEngine        #
    from ..engine import AsyncMySqlEngine   #
#-------------------------------------------------------------------------------
class Config:
    sqlEngine      : Sqlite3Engine       | MySqlEngine      | None = None
    asyncSqlEngine : AsyncSqlite3Engine  | AsyncMySqlEngine | None = None
    database : str | None = None
    sqlite3Engine      : Sqlite3Engine
    MySqlEngine        : MySqlEngine
    asyncSqlite3Engine : AsyncSqlite3Engine
    asyncMySqlEngine   : AsyncMySqlEngine
#-------------------------------------------------------------------------------