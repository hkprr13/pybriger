#-------------------------------------------------------------------------------
class SqlDateTypes:
    #---------------------------------------------------------------------------  
    INTEGER            = ""  # 一般的な整数型（INT、32bit）
    LONG               = ""  # 大きな整数型（BIGINT、64bit）
    SMALLINT           = ""  # 小さめの整数型（16bit）
    TINYINT            = ""  # 非常に小さい整数型（8bit）、BOOLEANの代替として使われる
    MEDIUMINT          = ""  # 中間のサイズの整数型（24bit）

    FLOAT              = ""  # 単精度浮動小数点数（約7桁の精度）
    DOUBLE             = ""  # 倍精度浮動小数点数（約15桁の精度）
    DECIMAL            = ""  # 任意精度の固定小数点数（金融・会計に最適）
    NUMERIC            = ""  # DECIMALと同義（SQL標準）

    CHAR               = ""  # 固定長文字列（CHAR(n)）、短い定長データ向け
    VARCHAR            = ""  # 可変長文字列（VARCHAR(n)）、一般的な文字列データ
    TEXT               = ""  # 長文テキスト（最大 65,535 バイト）
    TINYTEXT           = ""  # 非常に小さなテキスト（最大 255 バイト）
    MEDIUMTEXT         = ""  # 中程度のテキスト（最大 16,777,215 バイト）
    LONGTEXT           = ""  # 非常に大きなテキスト（最大 4GB）

    BLOB               = ""  # バイナリデータ（最大 65,535 バイト）
    TINYBLOB           = ""  # 非常に小さなBLOB（最大 255 バイト）
    MEDIUMBLOB         = ""  # 中程度のBLOB（最大 16MB）
    LONGBLOB           = ""  # 非常に大きなBLOB（最大 4GB）

    DATE               = ""  # 日付（YYYY-MM-DD）
    TIME               = ""  # 時刻（HH:MM:SS）
    DATETIME           = ""  # 日付＋時刻（YYYY-MM-DD HH:MM:SS）、タイムゾーンなし
    TIMESTAMP          = ""  # タイムスタンプ（UTCに変換される）
    YEAR               = ""  # 年（4桁または2桁）

    BOOLEAN            = ""  # 真偽値（TINYINT(1) として扱われる）
    NULL               = ""  # NULL 値明示用（型ではなく修飾的な意味）

    AUTO               = ""  # 自動採番（AUTO_INCREMENT 修飾子）
    UUID               = ""  # UUIDを保存するための文字列（通常は CHAR(36)）
    JSON               = ""  # JSON型（MySQL 5.7以降対応、構造化データ格納可能）
    ENUM               = ""  # 列挙型（事前定義された値の中から1つを選択）
    SET                = ""  # 複数選択可能な列挙型（0〜64個まで）

    GEOMETRY           = ""  # 空間情報の基本型（GIS拡張で使用）
    POINT              = ""  # 座標点（X,Y）
    LINESTRING         = ""  # 線（複数点の連続）
    POLYGON            = ""  # ポリゴン（閉じた線の集合）

    XML                = ""  # MySQLに専用XML型はないためTEXTで代用される
    HSTORE             = ""  # PostgreSQLのKey-Value型、MySQLでは非対応（TEXTで代用）
    INET               = ""  # IPv4/IPv6アドレス（VARCHAR(45)が一般的）
    CIDR               = ""  # サブネット表記（例: 192.168.0.0/24、VARCHARで代用）
    ARRAY              = ""  # MySQLには配列型がないためJSONで代替することが多い
    FILE               = ""  # ファイルデータ格納用（LONGBLOBなど）

    PLACEHOLDER        = ""  # SQLにおけるパラメータプレースホルダー（例: %s, ?）
    SERIAL             = ""  # BIGINT UNSIGNED AUTO_INCREMENTのエイリアス（MySQL構文糖衣）

    MULTILINESTRING    = ""  # 複数線（GIS）
    MULTIPOLYGON       = ""  # 複数ポリゴン（GIS）
    GEOMETRYCOLLECTION = ""  # 複数の空間要素の集合（GIS）
#-------------------------------------------------------------------------------
