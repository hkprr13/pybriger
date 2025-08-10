#-------------------------------------------------------------------------------
import inspect              # 呼び出し履歴を調べるのに使用
from functools import wraps # デコレーターで
                            # 元の関数名やドキュメントを保持するために使用
#-------------------------------------------------------------------------------
def public(func):
    """
    publicであること明示的にするメソッド
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 関数を呼び出したモジュールの名前
        caller  = inspect.stack()[1].frame.f_globals.get("__name__")
        # 関数が定義されているモジュールの名前
        current = func.__globals__.get("__name__")
        if not caller == current:
            pass
            # print(f"外部モジュール内で{func.__name__}を呼び出し")
        else:
            pass
            # print(f"同一モジュール内で{func.__name__}を呼び出し")
        return func(*args, ** kwargs)
    # メタ情報としてpublicであること示す
    return wrapper
#-------------------------------------------------------------------------------