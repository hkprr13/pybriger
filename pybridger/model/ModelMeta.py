#-------------------------------------------------------------------------------
from ..column import Column # カラムクラス
from ..filed  import Filed  # カラムクラス(フィールド)
#-------------------------------------------------------------------------------
class ModelMeta(type):
    """
    モデルクラスのメタクラス。
    Columnインスタンスを自動的に検出し、各カラムに `columnName`（変数名）と
    `tableName`（クラス名）を設定する。  
    また、テーブル名とカラム一覧をクラス属性として持たせる。
    このメタクラスは、ORMのModel定義時に使用され、クラス定義時に
    自動的にカラム定義を収集・構造化する役割を持つ。
    主な機能:
    - `Model` クラス自体は対象外（カラムを要求しない）
    - クラス定義時に Column 型の属性を検出し、名前とテーブル名を自動的に設定
    - クラス属性 `tableName`, `columns` を付与
    Attributes (動的に付加):
        tableName : str
            テーブル名（＝クラス名）
        columns : list[dict[str, Column]]
            カラム名とColumnオブジェクトの辞書リスト形式
    Exception:
        Columnが1つも定義されていない場合に例外を発生させる。
    Examples:
        class User(Model, metaclass=ModelMeta):
            id   = Column(Integer(), isPrimaryKey=True)
            name = Column(Text())
        
        → 自動的に:
            User.tableName = "User"
            User.columns = [{"id": Column(...)}, {"name": Column(...)}]
    """
    def __new__(mcs, name, bases, namespace):
        # Model自体にはカラムを要求しない
        if name == "Model":
            return super().__new__(mcs, name, bases, namespace)
        # カラムを自動登録
        columns = []
        for key, value in namespace.items():
            #カラムクラスかフィールドクラス
            if isinstance(value, Column) or isinstance(value, Filed):
                value.columnName = key       # カラム名に属性名を設定
                value.tableName  = name      # テーブル名にクラス名を設定
                columns.append({key: value}) # 辞書形式で保存
        # カラムが1つもない場合は例外
        if not columns:
            raise Exception(f"[{name}] クラスにカラムが定義されていません。")
        # テーブル名とカラムリストをクラス属性として付加
        namespace['tableName'] = name
        namespace['columns']   = columns
        return super().__new__(mcs, name, bases, namespace)
#-------------------------------------------------------------------------------
