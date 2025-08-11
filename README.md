# pybriger
<<<<<<< HEAD
pythonを用いた自作ORM
=======
    pythonを用いたORM(オブジェクトリレーショナルマッピング)です。
    SQLを直接書くことなく、オブジェクトを操作するようにデータベースを操作できます。
## 実行方法
    a

## ファイル構成  
    [pybriger]                                          # Briger2 ORMのルートディレクトリ  
        ├── [Log]                                       # ロギング関連モジュール  
        │   ├── Log.py                                  # ログ出力・管理クラス  
        │   └── __init__.py                             # Logパッケージ初期化ファイル  
        ├── [Trigger]                                   # DBトリガー関連処理  
        │   ├── Trigger.py                              # トリガークラス定義  
        │   └── __init__.py                             # Triggerパッケージ初期化ファイル  
        ├── [View]                                      # DBビュー関連処理  
        │   ├── View.py                                 # ビュー定義クラス  
        │   └── __init__.py                             # Viewパッケージ初期化ファイル  
        ├── [aggregate]                                 # 集約関数（SUM, COUNTなど）  
        │   ├── Aggregate.py                            # 集約基底クラス  
        │   ├── Avg.py                                  # AVG関数実装  
        │   ├── Count.py                                # COUNT関数実装  
        │   ├── Max.py                                  # MAX関数実装  
        │   ├── Min.py                                  # MIN関数実装  
        │   ├── Sum.py                                  # SUM関数実装  
        │   └── __init__.py                             # aggregateパッケージ初期化ファイル  
        ├── [column]                                    # カラム関連定義  
        │   ├── Column.py                               # カラムクラス定義  
        │   └── __init__.py                             # columnパッケージ初期化ファイル  
        ├── [common]                                    # 共通ユーティリティや基底クラス  
        │   ├── Override.py                             # メソッドオーバーライド支援クラス  
        │   ├── Private.py                              # 非公開メンバ管理  
        │   ├── Public.py                               # 公開メンバ管理  
        │   └── __init__.py                             # commonパッケージ初期化ファイル  
        ├── [conditions]                                # SQLの条件式関連クラス  
        │   ├── Condition.py                            # 条件式基底クラス  
        │   ├── ConditionGroup.py                       # 複数条件のグループ化クラス  
        │   ├── Regexp.py                               # 正規表現条件クラス  
        │   └── __init__.py                             # conditionsパッケージ初期化ファイル  
        ├── [config]                                    # 設定管理モジュール  
        │   ├── Config.py                               # 設定情報管理クラス  
        │   └── __init__.py                             # configパッケージ初期化ファイル  
        ├── [constraints]                               # テーブル制約関連クラス  
        │   ├── AutoIncrement.py                        # 自動増分制約クラス  
        │   ├── Check.py                                # チェック制約クラス  
        │   ├── Constraints.py                          # 制約基底クラス  
        │   ├── Default.py                              # デフォルト値制約クラス  
        │   ├── ForeignKey.py                           # 外部キー制約クラス  
        │   ├── NotNull.py                              # NOT NULL制約クラス  
        │   ├── PrimaryKey.py                           # 主キー制約クラス  
        │   ├── Unique.py                               # ユニーク制約クラス  
        │   └── __init__.py                             # constraintsパッケージ初期化ファイル  
        ├── [csv]                                       # CSV入出力関連モジュール  
        │   ├── CSV.py                                  # CSV読み書きクラス  
        │   └── __init__.py                             # csvパッケージ初期化ファイル  
        ├── [datatypes]                                 # データ型関連クラス群  
        │   ├── Array.py                                # 配列型クラス  
        │   ├── Auto.py                                 # 自動型判別クラス  
        │   ├── Blob.py                                 # BLOB型クラス  
        │   ├── Boolean.py                              # 真偽値型クラス  
        │   ├── Char.py                                 # CHAR型クラス  
        │   ├── Cidr.py                                 # CIDR型クラス（ネットワークアドレス）  
        │   ├── DataType.py                             # データ型基底クラス  
        │   ├── Date.py                                 # DATE型クラス  
        │   ├── DateTime.py                             # DATETIME型クラス  
        │   ├── Decimal.py                              # DECIMAL型クラス  
        │   ├── Double.py                               # DOUBLE型クラス  
        │   ├── Enum.py                                 # ENUM型クラス  
        │   ├── File.py                                 # ファイル型クラス  
        │   ├── Float.py                                # FLOAT型クラス  
        │   ├── Geometry.py                             # Geometry型クラス  
        │   ├── GeometryCollection.py                   # GeometryCollection型クラス  
        │   ├── Hstore.py                               # HSTORE型クラス（PostgreSQL特有）  
        │   ├── Inet.py                                 # INET型クラス（IPアドレス）  
        │   ├── Integer.py                              # INTEGER型クラス  
        │   ├── Json.py                                 # JSON型クラス  
        │   ├── LineString.py                           # LineString型クラス  
        │   ├── Long.py                                 # LONG型クラス  
        │   ├── LongBlob.py                             # LongBlob型クラス  
        │   ├── LongText.py                             # LongText型クラス  
        │   ├── MediumBlob.py                           # MediumBlob型クラス  
        │   ├── MediumInt.py                            # MediumInt型クラス  
        │   ├── MediumText.py                           # MediumText型クラス  
        │   ├── MultiLineString.py                      # MultiLineString型クラス  
        │   ├── MultiPolygon.py                         # MultiPolygon型クラス  
        │   ├── Null.py                                 # NULL型クラス  
        │   ├── Numeric.py                              # Numeric型クラス  
        │   ├── Point.py                                # Point型クラス  
        │   ├── Polygon.py                              # Polygon型クラス  
        │   ├── Serial.py                               # SERIAL型クラス（自動連番）  
        │   ├── Set.py                                  # Set型クラス  
        │   ├── SmallInt.py                             # SmallInt型クラス  
        │   ├── Text.py                                 # Text型クラス  
        │   ├── Time.py                                 # TIME型クラス  
        │   ├── TimeStamp.py                            # TIMESTAMP型クラス  
        │   ├── TinyBlob.py                             # TinyBlob型クラス  
        │   ├── TinyInt.py                              # TinyInt型クラス  
        │   ├── TinyText.py                             # TinyText型クラス  
        │   ├── Uuid.py                                 # UUID型クラス  
        │   ├── VarChar.py                              # VARCHAR型クラス  
        │   ├── Xml.py                                  # XML型クラス  
        │   ├── Year.py                                 # YEAR型クラス  
        │   └── __init__.py                             # datatypesパッケージ初期化ファイル  
        ├── [ddl]                                       # DDL（スキーマ操作）関連  
        │   ├── DDL.py                                  # DDL基底クラス  
        │   └── __init__.py                             # ddlパッケージ初期化ファイル  
        ├── [engine]                                    # DB接続とSQL実行エンジン層  
        │   ├── [base]                                  # ベースエンジン（各DB共通基盤）  
        │   │   ├── [datetypes]                         # 日付型サポート用  
        │   │   │   ├── MySqlDateTypes.py               # MySQL用日付型定義  
        │   │   │   ├── PostgreSqlDateTypes.py          # PostgreSQL用日付型定義  
        │   │   │   ├── SqlDateTypes.py                 # SQL標準日付型定義  
        │   │   │   ├── Sqlite3DateTypes.py             # SQLite3用日付型定義  
        │   │   │   └── __init__.py                     # datetypesパッケージ初期化ファイル  
        │   │   ├── AsyncMySqlEngine.py                 # MySQL非同期エンジン  
        │   │   ├── AsyncPostgreSqlEngine.py            # PostgreSQL非同期エンジン  
        │   │   ├── AsyncSqlite3Engine.py               # SQLite3非同期エンジン  
        │   │   ├── MySqlEngine.py                      # MySQL同期エンジン  
        │   │   ├── PostgreSqlEngine.py                 # PostgreSQL同期エンジン  
        │   │   ├── SqlEngine.py                        # 共通SQLエンジン基底クラス  
        │   │   ├── Sqlite3Engine.py                    # SQLite3同期エンジン  
        │   │   └── __init__.py                         # baseパッケージ初期化ファイル  
        │   ├── AsyncEngine.py                          # 非同期エンジン基底クラス  
        │   ├── Engine.py                               # 同期エンジン基底クラス  
        │   └── __init__.py                             # engineパッケージ初期化ファイル  
        ├── [filed]                                     # フィールド（カラム）定義クラス群  
        │   ├── BoolFiled.py                            # Boolean型フィールド定義  
        │   ├── DateTimeFiled.py                        # DateTime型フィールド定義  
        │   ├── Filed.py                                # フィールド基底クラス  
        │   ├── FloatFiled.py                           # Float型フィールド定義  
        │   ├── IntFiled.py                             # Integer型フィールド定義  
        │   ├── StrFiled.py                             # 文字列型フィールド定義   
        │   ├── TimeFiled.py                            # Time型フィールド定義  
        │   └── __init__.py                             # filedパッケージ初期化ファイル  
        ├── [index]                                     # インデックス関連クラス  
        │   ├── Index.py                                # インデックスクラス定義  
        │   └── __init__.py                             # indexパッケージ初期化ファイル  
        ├── [maneger]                                   # DDL/DML操作マネージャ群  
        │   ├── [alter]                                 # ALTER系DDL操作  
        │   │   ├── AlterTableAddColumn.py              # カラム追加  
        │   │   ├── AlterTableAddConstraint.py          # 制約追加  
        │   │   ├── AlterTableDropColumn.py             # カラム削除  
        │   │   ├── AlterTableDropConstraint.py         # 制約削除  
        │   │   ├── AlterTableRenameColumn.py           # カラム名変更  
        │   │   ├── AlterTableRenameTable.py            # テーブル名変更  
        │   │   ├── AlterView.py                        # ビューの変更  
        │   │   ├── AsyncAlterTableAddColumn.py         # 非同期カラム追加  
        │   │   ├── AsyncAlterTableAddConstraint.py     # 非同期制約追加  
        │   │   ├── AsyncAlterTableDropColumn.py        # 非同期カラム削除  
        │   │   ├── AsyncAlterTableDropConstraint.py    # 非同期制約削除  
        │   │   ├── AsyncAlterTableRenameColumn.py      # 非同期カラム名変更  
        │   │   ├── AsyncAlterTableRenameTable.py       # 非同期テーブル名変更  
        │   │   ├── AsyncAlterView.py                   # 非同期ビュー変更  
        │   │   └── __init__.py                         # alterパッケージ初期化ファイル  
        │   ├── [create]                                # CREATE系DDL操作  
        │   │   ├── AsyncCreateIndex.py                 # 非同期インデックス作成  
        │   │   ├── AsyncCreateTable.py                 # 非同期テーブル作成  
        │   │   ├── AsyncCreateTableIfNotExists.py      # 非同期存在確認付きテーブル作成  
        │   │   ├── AsyncCreateTrigger.py               # 非同期トリガー作成  
        │   │   ├── AsyncCreateView.py                  # 非同期ビュー作成  
        │   │   ├── CreateIndex.py                      # インデックス作成  
        │   │   ├── CreateTable.py                      # テーブル作成  
        │   │   ├── CreateTableIfNotExists.py           # 存在確認付きテーブル作成  
        │   │   ├── CreateTrigger.py                    # トリガー作成  
        │   │   ├── CreateView.py                       # ビュー作成  
        │   │   └── __init__.py                         # createパッケージ初期化ファイル  
        │   ├── [drop]                                  # DROP系DDL操作  
        │   │   ├── AsyncDropIndex.py                   # 非同期インデックス削除  
        │   │   ├── AsyncDropIndexIfExists.py           # 非同期存在確認付きインデックス削除  
        │   │   ├── AsyncDropTable.py                   # 非同期テーブル削除  
        │   │   ├── AsyncDropTableIfExists.py           # 非同期存在確認付きテーブル削除  
        │   │   ├── AsyncDropTrigger.py                 # 非同期トリガー削除  
        │   │   ├── AsyncDropTriggerIfNotExists.py      # 非同期存在確認付きトリガー削除  
        │   │   ├── AsyncDropView.py                    # 非同期ビュー削除  
        │   │   ├── AsyncDropViewIfExists.py            # 非同期存在確認付きビュー削除  
        │   │   ├── DropIndex.py                        # インデックス削除  
        │   │   ├── DropIndexIfExists.py                # 存在確認付きインデックス削除  
        │   │   ├── DropTable.py                        # テーブル削除  
        │   │   ├── DropTableIfExists.py                # 存在確認付きテーブル削除  
        │   │   ├── DropTrigger.py                      # トリガー削除  
        │   │   ├── DropTriggerIfNotExists.py           # 存在確認付きトリガー削除  
        │   │   ├── DropView.py                         # ビュー削除  
        │   │   ├── DropViewIfExists.py                 # 存在確認付きビュー削除  
        │   │   └── __init__.py                         # dropパッケージ初期化ファイル  
        │   ├── [record]                                # レコード操作群（CRUD）  
        │   │   ├── AsyncDeleteRecord.py                # 非同期単一レコード削除  
        │   │   ├── AsyncInsertRecord.py                # 非同期単一レコード挿入  
        │   │   ├── AsyncInsertRecords.py               # 非同期複数レコード挿入  
        │   │   ├── AsyncUpdateRecord.py                # 非同期単一レコード更新  
        │   │   ├── AsyncUpdateRecords.py               # 非同期複数レコード更新  
        │   │   ├── DeleteRecord.py                     # 同期単一レコード削除  
        │   │   ├── InsertRecord.py                     # 同期単一レコード挿入  
        │   │   ├── InsertRecords.py                    # 同期複数レコード挿入  
        │   │   ├── UpdateRecord.py                     # 同期単一レコード更新  
        │   │   ├── UpdateRecords.py                    # 同期複数レコード更新  
        │   │   └── __init__.py                         # recordパッケージ初期化ファイル  
        │   ├── [select]                                # SELECT系クエリ組み立て  
        │   │   ├── GroupBy.py                          # GROUP BY句組み立て  
        │   │   ├── Select.py                           # SELECT文組み立て  
        │   │   ├── Where.py                            # WHERE句組み立て  
        │   │   └── __init__.py                         # selectパッケージ初期化ファイル   
        │   ├── AsyncBase.py                            # 非同期基底マネージャクラス  
        │   ├── Base.py                                 # 同期基底マネージャクラス  
        │   └── __init__.py                             # manegerパッケージ初期化ファイル  
        ├── [migration]                                 # DBマイグレーション関連  
        │   ├── Migration.py                            # マイグレーションクラス  
        │   └── __init__.py                             # migrationパッケージ初期化ファイル  
        ├── [model]                                     # モデル定義関連   
        │   ├── AsyncModel.py                           # 非同期モデル基底クラス  
        │   ├── Model.py                                # 同期モデル基底クラス  
        │   ├── ModelMeta.py                            # モデルメタクラス定義  
        │   └── __init__.py                             # modelパッケージ初期化ファイル  
        ├── README.md                                   # プロジェクト概要ドキュメント  
        └── __init__.py                                 # Briger2パッケージ初期化ファイル  
>>>>>>> 482d8ff (pybriger)
