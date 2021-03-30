

# 将类写成装饰器，未调试成功
class Decorator(object):
    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner):
        """
        instance:代表实例，sum中的self
        owner：代表类本身，Test类
        """
        try:
            self.function(instance)
            self.result = 'success'
            self.exception = None
        except Exception as ex:
            self.result = 'failed'
            self.exception = ex


# 使用函数做装饰器，存报告结果
def func_decorator(func):
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
            print('go go go')
            self.result = 'success'
            self.exception = None
        except Exception as ex:
            self.result = 'failed'
            self.exception = ex
    return wrapper


class DecoratorTest(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        '''
        instance:代表实例，sum中的self
        owner：代表类本身，Test类

        '''
        print('调用的是get函数')
        return self.func(instance)  # instance就是Test类的self


class TestD:
    def __init__(self):
        self.result = None
        self.exception = None
        self.reset = True  # 定义一个类属性，稍后在装饰器里更改
        # self.func1 = True

    # def result_re(func):
    #     def wrapper(self, *args, **kwargs):
    #         try:
    #             func(self, *args, **kwargs)
    #             self.result = 'success'
    #             self.exception = None
    #         except Exception as ex:
    #             self.result = 'failed'
    #             self.exception = ex
    #
    #         # return func()
    #
    #     return wrapper

    @func_decorator
    def test_decorator(self):
        # self.reset = False
        print('测试类装饰器')


if __name__ == '__main__':
    d = TestD()
    d.test_decorator()
    print(d.result)
    print(d.exception)
