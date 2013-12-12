
def makeSafeScope():
    import _monte
    from monte.objects.equalizer import equalizer
    from monte.objects.e import E
    return {
        '__equalizer': Equalizer(),
        'E': E,
        #'gc': wrap(gc),
        #'__loop': loop,
        'throw': _monte.throw,
        #'makeProxy': ref.makeProxy,
        }
