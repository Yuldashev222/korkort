lst = [2 ** i for i in range(1, 11)]

print(lst)


class CustomList(str):
    def __getitem__(self, item):
        print(item)
        return super().__getitem__(item)
slice()

lst1 = CustomList('hello')

lst1[2:3:10]
