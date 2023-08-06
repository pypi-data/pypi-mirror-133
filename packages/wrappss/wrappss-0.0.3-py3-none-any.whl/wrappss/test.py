from wrapper import execute_time, execute_count, email_exception
import time

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


class Exception1(Exception):
    pass


class Exception2(Exception):
    pass


class Exception3(Exception):
    pass


# 监控指定的异常，不同异常发给不同的人
@email_exception(['zzlzzl996@126.com'], traced_exceptions=Exception1)
@email_exception(['2656155887@qq.com'], traced_exceptions=(Exception2, Exception3))
def test(args):
    if args == 1:
        raise Exception1
    elif args == 2:
        raise Exception2
    else:
        raise Exception3


if __name__ == '__main__':
    test(1)
