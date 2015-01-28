def co():
    yield 1
    yield 2
    n = 3
    while True:
        s = (yield n)
        if s is not None:
            n = s
        n += 1

it = co()
