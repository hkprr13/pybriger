#-------------------------------------------------------------------------------
import inspect              # 呼び出し履歴を調べるのに使用
from functools import wraps # デコレーターで
                            # 元の関数名やドキュメントを保持するために使用
#-------------------------------------------------------------------------------
def private(func):
    """
    privateであること明示的にするメソッド
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 呼び出し元のスタック情報を取得
        callerFrame    = inspect.stack()[1]
        # 呼び出し元のモジュールを取得
        # 呼び出したコードが属しているモジュール
        callModule     = inspect.getmodule(callerFrame[0])
        # この@privateメソッドが定義されているモジュール
        dediningModule = inspect.getmodule(func)
        # モジュールが違う場合はエラー
        if not callModule == dediningModule:
            raise PermissionError(
                f"'{func.__name__}'はプライベートです"
            )
        else:
            return func(*args, **kwargs)
    return wrapper
#-------------------------------------------------------------------------------