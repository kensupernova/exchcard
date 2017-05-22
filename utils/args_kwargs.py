def foo(x, *args, **kwargs):
    print "------------------"
    print "x=", x
    print "args=", args
    print "kwargs=", kwargs

    for arg in args:
        print arg

    for k, v in kwargs.items():
        print k, v



if __name__ == "__main__":
    foo(x=1)
    foo(1, 'm', 'n', None)
    foo(1, 'm', 'n', a=1, b=3, c = 9)
