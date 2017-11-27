import itertools
import re
from collections import Counter
from operator import attrgetter, sub

import numpy as np
import sys

from evaluation_tools.Evaluator import evaluate_file, count_fails, init

noc_rg = init()

filename = sys.argv[1]#"/home/thi/all.results.gz"
print("evaluating %s" % filename)

errornous, results = evaluate_file(noc_rg, filename)
faillist = count_fails(results)

all_result = (
    attrgetter('name', 'errornous', 'unexpected_len_sent', 'unexpected_len_recv', 'len_sent', 'len_recv',
               'sents_invalid',
               'recv_invalid', 'params', 'connection_counter_invalid')(obj) for obj in results)
names, errors, uls, ulr, ls, lr, si, ri, params, ff = itertools.zip_longest(*all_result)
print("errors: %s"%[e.name for e in errornous])
print("------------Statistics---------------")
print('Total Number of runs: %d' % len(results))
print("Runs with unexpected behavior: %d Ratio: %f" % (len(faillist), len(faillist) / float(len(results))))
print('IDs: %s' % ' '.join(sorted([obj.name for obj in results if not obj.is_valid()])))
print('Total number of simulation errors: %d' % len(errornous))
print('Total number of runs with an unexpected amount of sent flits: %d' % sum(uls))
print('Total number of runs with an unexpected amount of recv flits: %d' % sum(ulr))
print('Runs where the number of sent flits and the number of received flits differs between 2 nodes: %d' % sum(ff))
print('Maximum number of sent flits: %d' % max(ls))
print('Average number of sent flits: %f' % (sum(ls) / float(len(ls))))
print('Minimum number of sent flits: %d' % min(ls))
print('Maximum number of recv flits: %d' % max(lr))
print('Average number of recv flits: %f' % (sum(lr) / float(len(lr))))
print('Minimum number of recv flits: %d' % min(lr))
print('Average difference between number of sent and received flits: %f' % (sum(map(sub, ls, lr)) / float(len(ls))))
avg_dif_wdif_list = list(filter(lambda x: x != 0, map(sub, ls, lr)))
if len(avg_dif_wdif_list) != 0:
    avg_dif_wdif = sum(map(abs, avg_dif_wdif_list)) / float(len(avg_dif_wdif_list))
    print('Average difference between number of sent and received flits (only when different): %f' % avg_dif_wdif)
    print('Average absolute difference between number of sent and received flits (only when different): %f' % (
        sum(map(abs, avg_dif_wdif_list)) / float(len(avg_dif_wdif_list))))
    print('Variance of the difference between number of sent and received flits (only when different): %f' % np.var(
        avg_dif_wdif_list))
else:
    print("No differences in amount of sent and received packets!")

print('Average number of wrong injected flits: %d' % (sum(si) / float(len(si))))
print('Average number of wrong routed flits (XY Routing): %d' % (sum(ri) / float(len(ri))))
print('Maximum number of wrong routed flits (XY Routing): %d' % max(ri))

paramlist = [obj.params.split(' ')[:6] + [' '.join(obj.params.split(' ')[6:])] for obj in results if not obj.is_valid()]
if len(paramlist) == 0:
    print("No faults detected!")
else:
    breaktimes, breaktimesa, faultvalues, faultlengths, breakname1, breakname2, additionals = itertools.zip_longest(
        *paramlist)
    breaktimes = list(map(int, breaktimes))
    faultvalues = list(map(int, faultvalues))
    print('Average breaktime which lead to a fault: %f' % (sum(breaktimes) / float(len(breaktimes))))
    print('Maximum breaktime which lead to a fault: %f' % (max(breaktimes)))
    print('Average faultvalue: %f' % (sum(faultvalues) / float(len(faultvalues))))
    print('Which pins broke something statistic: ')
    print(Counter(breakname2))
    # Look at difflib, maybe matching blocks, maybe consider buckets
    total = 0
    for pattern in [r'^U', r'^valid_', r'^[\\]*CONTROL_PART/allocator_unit', r'^[\\]*CONTROL_PART/LBDR',
                    r'^[\\]*FIFO_[NESLW]/FIFO_comb', r'^[\\]*FIFO_[NESLW]/FIFO_seq', r'^[\\]*XBAR']:
        tmp = len(list(filter(lambda s: re.match(pattern, s.guessComponent()) is not None, faillist)))
        total += tmp
        print('"%s" broke something: %d' % (pattern, tmp))
    if total < len(breakname2):
        print('Missed %d patterns!' % (len(breakname2) - total))

    # convert to cell name and connected pin list.
    for obj in faillist:
        print(obj.guessComponent(), obj.params)
print("------------Statistics---------------")
