#-------------------------------------------------------------------------------
from .SqlDateTypes import SqlDateTypes
#-------------------------------------------------------------------------------
class Sqlite3DateTypes(SqlDateTypes):
    """MySQLのデータ型クラス"""
    #---------------------------------------------------------------------------
    # データ型定義（SQLite3 の型に対応）
    INTEGER     = "INTEGER"             # 整数型（64bit、オートインクリメントにも使用）
    SMALLINT    = "INTEGER"             # SQLiteにSMALLINTなし → INTEGERで代用
    LONG        = "INTEGER"             # SQLiteは全て64bit整数
    TINYINT     = "INTEGER"             # SQLiteにTINYINTなし → INTEGERで代用
    FLOAT       = "REAL"                # 単精度浮動小数点（SQLiteはREALで一括）
    DOUBLE      = "REAL"                # 倍精度浮動小数点（SQLiteはREALで一括）
    DECIMAL     = "NUMERIC"             # 高精度数値（丸めあり）
    NUMERIC     = "NUMERIC"             # NUMERIC型（任意精度数値）
    CHAR        = "TEXT"                # 固定長文字列 → SQLiteではTEXTで統一
    VARCHAR     = "TEXT"                # 可変長文字列 → TEXTにマッピングされる
    TEXT        = "TEXT"                # テキスト全般
    BLOB        = "BLOB"                # バイナリデータ
    BYTEA       = "BLOB"                # PostgreSQL互換のためのエイリアス
    DATE        = "TEXT"                # 日付（SQLiteは日付専用型なし）
    TIME        = "TEXT"                # 時刻（同上）
    DATETIME    = "TEXT"                # 日時（同上）
    TIMESTAMP   = "TEXT"                # タイムスタンプ（同上）
    BOOLEAN     = "INTEGER"             # 真偽値（0または1として保存）
    NULL        = "NULL"                # NULL明示
    UUID        = "TEXT"                # UUID文字列（標準UUID関数なし）
    JSON        = "TEXT"                # JSON（SQLite3.9以降はJSON関数あり）
    JSONB       = "TEXT"                # PostgreSQLとの互換のためのエイリアス
    ARRAY       = "TEXT"                # 配列型なし → JSON文字列などで代用
    ENUM        = "TEXT"                # 列挙型なし → TEXT＋制約で代用可能
    SET         = "TEXT"                # 複数選択型なし → TEXTで代用
    XML         = "TEXT"                # XML型なし → TEXTで代用
    HSTORE      = "TEXT"                # キー・バリュー型なし → JSON等で代用
    INET        = "TEXT"                # IPアドレス型なし → TEXTで代用
    CIDR        = "TEXT"                # サブネット表現型なし → TEXTで代用
    GEOMETRY    = "TEXT"                # 空間型なし（SpatiaLite使用時は拡張可能）
    PLACEHOLDER = "?"                   # sqlite3 モジュールのプレースホルダー
    AUTO        = "INTEGER PRIMARY KEY AUTOINCREMENT"  # 自動採番
    SERIAL      = "INTEGER PRIMARY KEY AUTOINCREMENT"  # PostgreSQLとの互換のため

    AUTOINCREMENT = "AUTOINCREMENT" # 自動採番
#-------------------------------------------------------------------------------