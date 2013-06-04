import cProfile
import lsprofcalltree
import sys, time, pprint, json, os
from collections import Counter
from ometa import runtime
runtime.TIMING = True
from monte import eparser, unparser
rulesInvoked = Counter()
memoHits = Counter()
trace = []
def tf(src, span, inp):
    trace.append((src, span, inp))
    if src[0].isalnum():
        rulesInvoked[src] += 1
        memoHits[src, inp] += 1


tim = time.time()
data = open(sys.argv[1]).read()
#pr = cProfile.Profile()
#ep = pr.runcall(eparser.parse, data)
#kc = lsprofcalltree.KCacheGrind(pr)
#kc.output(open('monte.cachegrind', 'w'))

ep = eparser.parse(data)
open("output.e", 'w').write('\n'.join(str(x) for x in unparser.Unparser.transform(ep)[0]))
print "E code parsed in %s secs" % ((time.time() - tim))
# print "Top rules:"
# pprint.pprint(rulesInvoked.most_common(8))
# print "Top memo hits:"
# pprint.pprint(memoHits.most_common(8))
