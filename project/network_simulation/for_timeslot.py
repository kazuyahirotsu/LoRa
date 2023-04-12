# example

# 0
# hub -> repeat
# 1
# repeat -> all end
# 2
# end1 -> repeat
# 3
# (end1 -> repeat)
# 4
# (end1 -> repeat)
# 5
# end2 -> repeat
# 6
# end2 -> repeat
# 7
# (end2 -> repeat)
# 8

# repeat 0~8
# end1 1~3
# end2 1, 3~6

import random
ontimes_child = []
ontimes_repeat = []
success_rate_array = []
# endとrepeatの通信は最小でsend_delay、最大でtimeout
child_num = 10
simulation_num = 100
time_span = 600
# retry_p = 0.01
retry_sum = 0
send_delay = 1
send_timeout_delay = 3
# time_error_wait_time = 1
for retry_p in [num * 0.01 for num in range(0, 101)]: # 0,101
    time = 0
    success_rate = 0

    alive = [True]*child_num
    ontime = [0]*(child_num+1)
    wakeup_time = [0]*(child_num+1)
    for i in range(1,child_num+1):
        # wakeup_time[i] = send_delay*2*i-time_error_wait_time 
        # wakes up at this time on their clock, but in reality it's send_delay*2*i
        # because the time is delayed due to sending delay
        wakeup_time[i] = send_delay*2 + send_delay*3*(i-1)

    for _ in range(simulation_num):

        time = round(time+send_delay*2,2)

        for child_id in range(child_num):
            if alive[child_id]:
                # end->repeat
                retry_num = 0
                # get retry count
                for i in range(2):
                    if random.random()>retry_p:
                        break
                    else:
                        retry_num += 1
                
                # add time
                retry_sum += retry_num
                time = round(time+send_delay*(1+retry_num),2)
            
                if retry_num == 2 and random.random()<=retry_p:
                    # communication failed
                    pass
                else:
                    success_rate += 1

                # add ontime the time on
                ontime[child_id+1] += (time%time_span-wakeup_time[child_id+1]) + send_delay # add the time to receive now time
                # print(time,wakeup_time[child_id+1])
                if time%time_span-wakeup_time[child_id+1] <=0:
                    print("warning")
                
                time = round(time+send_delay*(2-retry_num),2)

            else:
                # timeout
                time = round(time+send_timeout_delay,2)

        ontime[0] += (time%time_span-wakeup_time[0])

        time = round(time+(time_span-time%time_span),2)


    for i in range(len(ontime)):
        ontime[i] /= simulation_num
    ontimes_child.append(sum(ontime[1:])/child_num)
    ontimes_repeat.append(ontime[0])
    success_rate_array.append(success_rate/(simulation_num*child_num))
print(ontimes_child)

import matplotlib.pyplot as plt
print("child_num: "+str(child_num))
print("simulation_num: "+str(simulation_num))
print("time_span: "+str(time_span))
print("send_delay: "+str(send_delay))
print("time_span: "+str(time_span))

print("repeat on time")
plt.plot(ontimes_repeat)
plt.show()
print("child average on time")
plt.plot(ontimes_child)
plt.show()
print("success rate for repeat <-> child")
plt.plot(success_rate_array)
plt.show()
