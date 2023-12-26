st = "Hello world. my name is John. This is my world"


def foo(text: str):
    text = text.lower().replace(".", "").replace(",", "")
    words = text.split()
    return {word: words.count(word) for word in words}


print(foo(st))
