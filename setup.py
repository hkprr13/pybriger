from setuptools import setup, find_packages

setup(
    name                          = "pybriger",                                 # パッケージ名（PyPI上の名前）
    version                       = "0.1.0",                                    # バージョン
    author                        = "KazuhiroKondo",                            # 名前
    author_email                  = "hkprr13@gmail.com",                        # メールアドレス
    description                   = "自作のORMです",                             # 説明
    long_description              = open(
        "README.md",                                                            #
        encoding = "utf-8"                                                      #
    ).read(),                                                                   # 詳細説明
    long_description_content_type = "text/markdown",                            # READMEのフォーマット指定
    url                           = "https://github.com/hkprr13/pybriger.git",  # プロジェクトURL
    packages                      = find_packages(),                            # パッケージを自動検出
    python_requires               = '>=3.13.3',                                 # 対応Pythonバージョン指定
    install_requires              = [                                           # 依存パッケージ
        "mysql-connector-python>=1.1.1",                                        # mysqlドライバ
        "aiomysql>=0.2.0",                                                      # 非同期mysqlドライバ
        "aiosqlite>=0.21.0",                                                    # 非同期sqlite3ドライバ
        "psycopg>=3.2.9",                                                       # PostgreSQLドライバ
        "psycopg-binary>=3.2.9"                                                 # 非同期PostgreSQLドライバ
    ],
    classifiers = [                                                             # PyPI用の分類タグ
        "Programming Language :: Python :: 3",                                  #
        "License :: OSI Approved :: MIT License",                               #
        "Operating System :: OS Independent",                                   #
    ],
    include_package_data = True,                                                # MANIFEST.inの指定を有効にする場合
    entry_points = {                                                            # コンソールスクリプトを追加する場合
        'console_scripts': [
            'my-command=my_module.cli:main',                                    # 
        ],
    },
)