

class Test:

    def __init__(self):
        self.data = None

    # 定义方法
    def func(self, param):
        self.data = param
        print("Do something: " + param)


class TestCall:

    def __init__(self):
        self.data = None

    # 定义__call__方法
    def __call__(self, param):
        self.data = param
        print("Do something: " + param)


if __name__ == '__main__':
    test = Test()
    test.func('test')
    test_call = TestCall()
    test_call('test call')
