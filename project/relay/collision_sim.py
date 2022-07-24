import random
trials = [10**i for i in range(7)]
p_list = []
slot_num = 5
slot_length = 0.5
time_length = 60-slot_length
for trial in trials:
    p = 0
    for _ in range(trial):
        nooverlap = True
        a = [random.uniform(0, time_length) for _ in range(slot_num)]
        a.sort()
        for i in range(1,slot_num):
            if a[i]-a[i-1]>slot_length:
                continue
            else:
                nooverlap = False
                break
        if nooverlap:
            p += 1
    p = p/trial
    p_list.append(p)
print(trials)
print(p_list)