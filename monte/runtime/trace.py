import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def trace(x):
    print x,

def traceln(x):
    print x

def traceback():
    import traceback
    traceback.print_exc()
