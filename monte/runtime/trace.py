from monte.runtime.m import theM

def trace(x):
    print theM.toQuote(x).s.encode('utf-8'),

def traceln(x):
    print theM.toQuote(x).s.encode('utf-8')
