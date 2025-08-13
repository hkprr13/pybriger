#-------------------------------------------------------------------------------
from .SqlDateTypes import SqlDateTypes
#-------------------------------------------------------------------------------
class MySqlDateTypes(SqlDateTypes):
    """MySQLのデータ型クラス"""
    #---------------------------------------------------------------------------
    # データ型定義（MySQLの型に対応）
    INTEGER     = "INT"                  # 整数型（32bit）
    LONG        = "BIGINT"               # 長整数（64bit）
    SMALLINT    = "SMALLINT"             # 小さい整数（16bit）
    TINYINT     = "TINYINT"              # 非常に小さい整数（8bit）
    MEDIUMINT   = "MEDIUMINT"            # 中間の整数（24bit）
    FLOAT       = "FLOAT"                # 単精度浮動小数点
    DOUBLE      = "DOUBLE"               # 倍精度浮動小数点
    DECIMAL     = "DECIMAL"              # 高精度数値（任意精度）
    NUMERIC     = "NUMERIC"              # DECIMALの別名
    CHAR        = "CHAR"                 # 固定長文字列
    VARCHAR     = "VARCHAR"              # 可変長文字列
    TEXT        = "TEXT"                 # 長文（最大64KB）
    TINYTEXT    = "TINYTEXT"             # 小さなテキスト
    MEDIUMTEXT  = "MEDIUMTEXT"           # 中程度のテキスト
    LONGTEXT    = "LONGTEXT"             # 非常に大きなテキスト
    BLOB        = "BLOB"                 # バイナリデータ（最大64KB）
    TINYBLOB    = "TINYBLOB"             # 小さなBLOB
    MEDIUMBLOB  = "MEDIUMBLOB"           # 中程度のBLOB
    LONGBLOB    = "LONGBLOB"             # 非常に大きなBLOB
    DATE        = "DATE"                 # 日付（YYYY-MM-DD）
    TIME        = "TIME"                 # 時刻（HH:MM:SS）
    DATETIME    = "DATETIME"             # 日時（MySQL独自形式）
    TIMESTAMP   = "TIMESTAMP"            # タイムスタンプ
    YEAR        = "YEAR"                 # 年（4桁）
    BOOLEAN     = "BOOLEAN"              # 真偽値（TINYINT(1)の別名）
    NULL        = "NULL"                 # NULL明示
    AUTO        = "AUTO_INCREMENT"       # 自動採番
    UUID        = "CHAR(36)"             # UUID（関数UUID()で生成、文字列として保存）
    JSON        = "JSON"                 # JSON型（MySQL 5.7+）
    ENUM        = "ENUM"                 # 列挙型（値の列挙）
    SET         = "SET"                  # 複数選択型
    GEOMETRY    = "GEOMETRY"             # 空間情報型（GIS）
    POINT       = "POINT"                # 座標点
    LINESTRING  = "LINESTRING"           # 線
    POLYGON     = "POLYGON"              # ポリゴン
    XML         = "TEXT"                 # MySQLにXML専用型はない（TEXTで代替）
    HSTORE      = "TEXT"                 # MySQLはHSTOREなし
    INET        = "VARCHAR(45)"          # IPv4/IPv6用（最大45文字）
    CIDR        = "VARCHAR(43)"          # サブネット（"192.168.0.0/24"など）
    ARRAY       = "JSON"                 # MySQLは配列型なし → JSONで代替
    FILE        = "LONGBLOB"             # ファイル保存用（最大4GB）
    PLACEHOLDER = "%s"                   # プレースホルダー
    SERIAL             = "BIGINT UNSIGNED AUTO_INCREMENT"  # SERIAL
    MULTILINESTRING    = "MULTILINESTRING"
    MULTIPOLYGON       = "MULTIPOLYGON"
    GEOMETRYCOLLECTION = "GEOMETRYCOLLECTION"
    
    AUTOINCREMENT = "AUTO_INCREMENT" # 自動採番
#-------------------------------------------------------------------------------