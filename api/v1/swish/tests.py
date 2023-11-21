# # # # # # # # # # # # assert 1 < 5
# # # # # # # # # # # # a: int = 11
# # # # # # # # # # # #
# # # # # # # # # # # #
# # # # # # # # # # # # class A:
# # # # # # # # # # # #     def __init__(self, text):
# # # # # # # # # # # #         self.text = text
# # # # # # # # # # # #
# # # # # # # # # # # #
# # # # # # # # # # # # class B(A):
# # # # # # # # # # # #     def __init__(self, author, text):
# # # # # # # # # # # #         super().__init__(text)
# # # # # # # # # # # #         self.author = author
# # # # # # # # # # # #
# # # # # # # # # # # #
# # # # # # # # # # # # b = B('hello', 'adasd')
# # # # # # # # # # # #
# # # # # # # # # # # # print(b.__dict__)
# # # # # # # # # # #
# # # # # # # # # # # def custom_abs(func):
# # # # # # # # # # #     def wrapper(seq):
# # # # # # # # # # #         return func(abs(seq))
# # # # # # # # # # #
# # # # # # # # # # #     return wrapper
# # # # # # # # # # #
# # # # # # # # # # #
# # # # # # # # # # # def foo(seq: int) -> list:
# # # # # # # # # # #     return [i for i in range(0, seq, 2)]
# # # # # # # # # # #
# # # # # # # # # # #
# # # # # # # # # # # def test() -> None:
# # # # # # # # # # #     assert foo(10) == [0, 2, 4, 6, 8]
# # # # # # # # # # #     assert foo(-10) == [0, 2, 4, 6, 8]
# # # # # # # # # # #     assert foo(2) == [0]
# # # # # # # # # # #     assert foo(-2) == [0]
# # # # # # # # # # #     assert foo(0) == []
# # # # # # # # # # #     assert foo(-1) == [0]
# # # # # # # # # # #     print('Successfully completed')
# # # # # # # # # # #
# # # # # # # # # # #
# # # # # # # # # # # test()
# # # # # # # # # #
# # # # # # # # # #
# # # # # # # # # # def foo(*args, **kwargs):
# # # # # # # # # #     return args, kwargs
# # # # # # # # # #
# # # # # # # # # #
# # # # # # # # # # lst1 = foo(1, 2, 3, 4, a=1, {1: 2, 3: 4}, asd=1)
# # # # # # # # # #
# # # # # # # # # # print(lst1)
# # # # # # # # # import random
# # # # # # # # #
# # # # # # # # #
# # # # # # # # # class A:
# # # # # # # # #     b = list(range(20))
# # # # # # # # #     random.shuffle(b)
# # # # # # # # #
# # # # # # # # #     @classmethod
# # # # # # # # #     def get_b(cls):
# # # # # # # # #         return cls.b
# # # # # # # # #
# # # # # # # # #
# # # # # # # # # print(A.get_b())
# # # # # # # from functools import wraps
# # # # # # #
# # # # # # #
# # # # # # # def sup_decor(a):
# # # # # # #     print(a)
# # # # # # #
# # # # # # #
# # # # # # # def text_decor(text):
# # # # # # #     def decor(func):
# # # # # # #         @wraps(func)
# # # # # # #         def wrapper(*args, **kwargs):
# # # # # # #             print(text)
# # # # # # #             print('Decorator start')
# # # # # # #             func(*args, **kwargs)
# # # # # # #             print('Decorator end')
# # # # # # #
# # # # # # #         return wrapper
# # # # # # #
# # # # # # #     return decor
# # # # # # #
# # # # # # #
# # # # # # # def foo():
# # # # # # #     """
# # # # # # #     hello world qilib beradi
# # # # # # #     """
# # # # # # #     print('function')
# # # # # # #
# # # # # # #
# # # # # # # f1 = text_decor(text='asd')(foo)
# # # # # # #
# # # # # # # f1()
# # # # # #
# # # # # #
# # # # # # class Cat:
# # # # # #
# # # # # #     def __len__(self):
# # # # # #         return 20
# # # # # #
# # # # # #
# # # # # # c = Cat()
# # # # # #
# # # # # # print(len(c))
# # # # #
# # # # # def foo(lst1, lst2):
# # # # #     result = list(set(lst1 + lst2))
# # # # #     result.sort(key=lambda item: int(item[0]))
# # # # #     return result
# # # # #
# # # # #
# # # # # def test():
# # # # #     assert foo(['213123123, <obj> asd1221', '64684, <obj> 6455456asd'], ['213123123, <obj> asd1221', '64684, <obj> 6455456asd']) == ['213123123, <obj> asd1221', '64684, <obj> 6455456asd']
# # # # #
# # # # #
# # # # # test()
# # # #
# # # #
# # # # def foo(lst):
# # # #     lst.sort(key=lambda item: item == 0)
# # # #     return lst
# # # #
# # # #
# # # # def test():
# # # #     assert foo([1, 11, 2, 3, 0, 4, 5, 0]) == [1, 11, 2, 3, 4, 5, 0, 0]
# # # #
# # # #
# # # # test()
# # # import time
# # # from datetime import datetime
# # #
# # #
# # # def summing_time(func):
# # #     def wrapper(a, b):
# # #         time_now = datetime.now()
# # #         func(a, b)
# # #         print(datetime.now() - time_now)
# # #
# # #     return wrapper
# # #
# # #
# # # @summing_time
# # # def sum_numbers(a, b):
# # #     return a + b
# # #
# # #
# # # sum_numbers(10, 10)
# #
# # class A:
# #     ...
# #
# #
# # print(hash(A()))
#
#
# def foo(dct: dict, val):
#     return list(filter(lambda item: item[1] == val, dct.items()))
#     # return sorted(dct.items(), key=lambda item: item[1])[-2:]
#
#
# def test():
#     assert foo({'a': 34, 'd': 66, 'c': 12, 'b': 9000}, 9000) == [('b', 9000)]
#
#
# print(foo({'a': 34, 'd': 66, 'c': 12, 'b': 9000}, 9000))
