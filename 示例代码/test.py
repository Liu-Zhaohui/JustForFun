# from varname import Wrapper
import re


def func(n):
    var = 'test'
    var_name = 'vara'
    s = locals()[var_name]
    print(s)


def func2(a, b):
    globals()['a'] = 250
    locals()[a] = b
    print(globals()['a'])
    print(locals()[a])


def get_var(text):
    if re.match('{{.*}}', text):
        print(text.strip('{}'))
        print('truetrue')

# @result_re
# def test():
#     print('yes')


class Decorator:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        '''
        instance:代表实例，sum中的self
        owner：代表类本身，Test类

        '''
        try:
            self.function(self, *args, **kwargs)
            self.result = 'success'
            self.exception = None
        except Exception as ex:
            self.result = 'failed'
            self.exception = ex


class TestD:
    def __init__(self):
        self.result = None
        self.exception = None
        self.reset = True  # 定义一个类属性，稍后在装饰器里更改
        # self.func1 = True

    def result_re(func):
        def wrapper(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
                self.result = 'success'
                self.exception = None
            except Exception as ex:
                self.result = 'failed'
                self.exception = ex

            # return func()

        return wrapper

    @result_re
    def test(self):
        print('ok')

    @Decorator
    def test_decorator(self, a):
        print('测试类装饰器', a)

    # 在类里定义一个装饰器
    def clothes(func):  # func接收body
        def ware(self, *args, **kwargs):  # self,接收body里的self,也就是类实例
            print('This is a decrator!')
            if self.reset == True:  # 判断类属性
                print('Reset is Ture, change Func..')
                # self.func1 = False  # 修改类属性
            else:
                print('reset is False.')

            return func(self, *args, **kwargs)

        return ware

    @clothes
    def body(self):
        print('The body feels could!')


if __name__ == '__main__':
    # func2(a='test', b=100)
    # get_var('{{134}}')
    # test
    t = TestD()
    # t.test
    t.test_decorator('NB')
    # t.test2()
    # t.body()
    print(t.result)
    print(t.exception)

