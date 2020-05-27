def triangle(a, b, c):
    if (a < b + c) & (b < a + c) & (c < a + b):
        return True
    else:
        return False

def test():
    assert triangle(4, 2, 1)

if __name__ == '__main__':
    test()