import time


def execute_time(func):
    import time

    def wrapper(*args, **kw):
        start_time = time.time()
        func_return = func(*args, **kw)
        end_time = time.time()
        # 保留4位小数
        print('{}() execute time:{}s'.format(func.__name__, round((end_time - start_time), 4)))
        return func_return

    return wrapper


if __name__ == '__main__':
    @execute_time
    def test(second):
        time.sleep(second)


    test(3.813231)
