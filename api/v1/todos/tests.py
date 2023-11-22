from collections import Counter


def get_count(nums: list[int], el):
    cnt = 0
    for i in nums:
        if i == el:
            cnt += 1
    return cnt


def foo(nums: list[int]):
    set_nums = []
    result = []
    for i in nums:
        if i not in set_nums:
            set_nums.append(i)

    for i in set_nums:
        result.append((i, get_count(nums, i)))
    return result


def test():
    assert foo([1, 1, 1, 4, 2, 6, 1, 6, 9]) == [(1, 4), (4, 1), (2, 1), (6, 2), (9, 1)]
    assert foo([201, 200, 3, 49, 50, 6, 201, 8, 49]) == [(201, 2), (200, 1), (3, 1), (49, 2), (50, 1), (6, 1), (8, 1)]
    assert foo([59, 200, 53, 44, 59, 90, 91, 1001, 29]) == [(59, 2), (200, 1), (53, 1), (44, 1), (90, 1), (91, 1),
                                                            (1001, 1), (29, 1)]


test()
print(Counter('abac'))
