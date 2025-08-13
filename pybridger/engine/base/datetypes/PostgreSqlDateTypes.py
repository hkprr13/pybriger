#-------------------------------------------------------------------------------
from .SqlDateTypes import SqlDateTypes
#-------------------------------------------------------------------------------
class PostgreSqlDateTypes(SqlDateTypes):
    """PostgreSQLのデータ型クラス"""
    #---------------------------------------------------------------------------
    # データ型定義（PostgreSQL の型に対応）
    INTEGER    = "INTEGER"             # 整数型（32bit）
    LONG       = "BIGINT"              # 長整数（64bit）
    SMALLINT   = "SMALLINT"            # 小さい整数
    FLOAT      = "REAL"                # 単精度浮動小数点
    DOUBLE     = "DOUBLE PRECISION"    # 倍精度浮動小数点
    DECIMAL    = "DECIMAL"             # 高精度数値（任意精度）
    NUMERIC    = "NUMERIC"             # 高精度数値（同上）
    CHAR       = "CHAR"                # 固定長文字列
    VARCHAR    = "VARCHAR"             # 可変長文字列
    TEXT       = "TEXT"                # 長文
    BLOB       = "BLOB"                # バイナリデータ
    BYTEA      = "BYTEA"               # PostgreSQL用バイナリ
    DATE       = "DATE"                # 日付（YYYY-MM-DD）
    TIME       = "TIME"                # 時刻（HH:MM:SS）
    DATETIME   = "TIMESTAMP"           # 日時
    TIMESTAMP  = "TIMESTAMP"           # タイムスタンプ
    BOOLEAN    = "BOOLEAN"             # 真偽値
    NULL       = "NULL"                # NULL明示
    AUTO       = "AUTO_INCREMENT"      # MySQLでの自動採番
    SERIAL     = "SERIAL"              # PostgreSQLでの自動採番
    UUID       = "UUID"                # UUID
    JSON       = "JSON"                # JSON
    JSONB      = "JSONB"               # バイナリ形式のJSON
    ARRAY      = "ARRAY"               # 配列型
    ENUM       = "ENUM"                # 列挙型
    SET        = "SET"                 # 複数選択型
    XML        = "XML"                 # XML型
    HSTORE     = "HSTORE"              # キー・バリュー型
    INET       = "INET"                # IPアドレス型
    CIDR       = "CIDR"                # サブネット型
    GEOMETRY   = "GEOMETRY"            # 空間情報型
    PLACEHOLDER = "%s"                 # psycopg のプレースホルダー
    AUTOINCREMENT = "AUTOINCREMENT" # 自動採番
#-------------------------------------------------------------------------------