# wakeup together
import matplotlib.pyplot as plt
waketime_1 = []
waketime_2 = []
child_nums = []

a=1*(9/10)+2*(1/10)*(9/10)+3*(1/10)*(1/10)
p_1=(a+1)*(9/10)+(a+2)*(1/10)*(9/10)+(a+3)*(1/10)*(1/10)*(9/10)+3*(1/10)*(1/10)*(1/10)
p_2=1*(9/10)+2*(1/10)*(9/10)+3*(1/10)*(1/10)
transmit_time = 0.5
setup_time = 0.1

for child_num in range(1,100):
    child_nums.append(child_num)
    waketime_1.append((transmit_time+setup_time + transmit_time*p_1*(child_num+1)/2)*child_num+(transmit_time+setup_time + transmit_time*p_1*child_num))
    waketime_2.append((transmit_time+setup_time + transmit_time*1.11)*child_num
+(transmit_time+setup_time + transmit_time*3)*(child_num-1)*child_num/2 
+(transmit_time+setup_time + transmit_time*3)*(child_num-1)
+transmit_time+setup_time + transmit_time*1.11
+(transmit_time+setup_time + transmit_time)/6)

fig = plt.figure(facecolor="white")
plt.plot(child_nums,waketime_1, label='method1')
plt.plot(child_nums,waketime_2, label='method2')
plt.xlabel('child_num')
plt.ylabel('waketime')
plt.legend() 
plt.show()


# with late wakeup
import matplotlib.pyplot as plt
waketime_1 = []
waketime_2 = []
child_nums = []

a=1*(9/10)+2*(1/10)*(9/10)+3*(1/10)*(1/10)
p_1=(a+1)*(9/10)+(a+2)*(1/10)*(9/10)+(a+3)*(1/10)*(1/10)*(9/10)+3*(1/10)*(1/10)*(1/10)
p_2=1*(9/10)+2*(1/10)*(9/10)+3*(1/10)*(1/10)
transmit_time = 0.5
setup_time = 0.1

for child_num in range(1,100):
    child_nums.append(child_num)
    waketime_1.append((transmit_time+setup_time + transmit_time*p_1*(child_num+1)/2)*child_num+(transmit_time+setup_time + transmit_time*p_1*child_num)- (transmit_time*2*child_num/2)*child_num)
    waketime_2.append((transmit_time+setup_time + transmit_time*p_2)*child_num
+(transmit_time+setup_time + transmit_time*3)*(child_num-1)*child_num/2 
+(transmit_time+setup_time + transmit_time*3)*(child_num-1)
+transmit_time+setup_time + transmit_time*p_2
+(transmit_time+setup_time + transmit_time)/6
- (transmit_time+setup_time + transmit_time*3)*(child_num-1)*child_num/2)

fig = plt.figure(facecolor="white")
plt.plot(child_nums,waketime_1, label='method1')
plt.plot(child_nums,waketime_2, label='method2')
plt.xlabel('child_num')
plt.ylabel('waketime')
plt.legend() 
plt.show()


# low retry prob with late wakeup
import matplotlib.pyplot as plt
waketime_1 = []
waketime_2 = []
child_nums = []

a=1*(99/100)+2*(1/100)*(99/100)+3*(1/100)*(1/100)
p_1=(a+1)*(99/100)+(a+2)*(1/100)*(99/100)+(a+3)*(1/100)*(1/100)*(99/100)+3*(1/100)*(1/100)*(1/100)
p_2=1*(99/100)+2*(1/100)*(99/100)+3*(1/100)*(1/100)
transmit_time = 0.5
setup_time = 0.1

for child_num in range(1,500):
    child_nums.append(child_num)
    waketime_1.append((transmit_time+setup_time + transmit_time*p_1*(child_num+1)/2)*child_num+(transmit_time+setup_time + transmit_time*p_1*child_num)- (transmit_time*2*child_num/2)*child_num)
    waketime_2.append((transmit_time+setup_time + transmit_time*p_2)*child_num
+(transmit_time+setup_time + transmit_time*3)*(child_num-1)*child_num/2 
+(transmit_time+setup_time + transmit_time*3)*(child_num-1)
+transmit_time+setup_time + transmit_time*p_2
+(transmit_time+setup_time + transmit_time)/6
- (transmit_time+setup_time + transmit_time*3)*(child_num-1)*child_num/2)

fig = plt.figure(facecolor="white")
plt.plot(child_nums,waketime_1, label='method1')
plt.plot(child_nums,waketime_2, label='method2')
plt.xlabel('child_num')
plt.ylabel('waketime')
plt.legend() 
plt.show()


# retry prob change with late wakeup
import matplotlib.pyplot as plt
waketime_1 = []
waketime_2 = []
retry_ps = []

transmit_time = 0.5
setup_time = 0.1
child_num = 10

for retry_p in range(0,100):
    retry_p /= 100
    try_ave =2*(1-retry_p)+3*(retry_p)*(1-retry_p)+4*(retry_p)*(retry_p)*(1-retry_p)+3*(retry_p)*(retry_p)*(retry_p)

    a=1*(1-retry_p)+2*(retry_p)*(1-retry_p)+3*(retry_p)*(retry_p)
    p_1=(a+1)*(1-retry_p)+(a+2)*(retry_p)*(1-retry_p)+(a+3)*(retry_p)*(retry_p)*(1-retry_p)+3*(retry_p)*(retry_p)*(retry_p)
    p_2=1*(1-retry_p)+2*(retry_p)*(1-retry_p)+3*(retry_p)*(retry_p)

    retry_ps.append(retry_p)
    waketime_1.append((transmit_time+setup_time + transmit_time*p_1*(child_num+1)/2)*child_num+(transmit_time+setup_time + transmit_time*p_1*child_num)- (transmit_time*2*child_num/2)*child_num)
    waketime_2.append((transmit_time+setup_time + transmit_time*p_2)*child_num
    +(transmit_time+setup_time + transmit_time*3)*(child_num-1)*child_num/2 
    +(transmit_time+setup_time + transmit_time*3)*(child_num-1)
    +transmit_time+setup_time + transmit_time*p_2
    +(transmit_time+setup_time + transmit_time)/6
    - (transmit_time+setup_time + transmit_time*3)*(child_num-1)*child_num/2)
    
fig = plt.figure(facecolor="white")
plt.plot(retry_ps,waketime_1, label='method1')
plt.plot(retry_ps,waketime_2, label='method2')
plt.xlabel('retry_p')
plt.ylabel('waketime')
plt.legend() 
plt.show()


# total time to complete procedure
import matplotlib.pyplot as plt
time_overall_1 = []
time_overall_2 = []
child_nums = []
a=1*(9/10)+2*(1/10)*(9/10)+3*(1/10)*(1/10)
p_1=(a+1)*(9/10)+(a+2)*(1/10)*(9/10)+(a+3)*(1/10)*(1/10)*(9/10)+3*(1/10)*(1/10)*(1/10)
p_2=1*(9/10)+2*(1/10)*(9/10)+3*(1/10)*(1/10)
transmit_time = 0.5
setup_time = 0.1

for child_num in range(1,500):
    child_nums.append(child_num)
    time_overall_1.append(transmit_time+setup_time + transmit_time*p_1*child_num)
    time_overall_2.append((transmit_time+setup_time + transmit_time*3)*(child_num-1)+transmit_time+setup_time + transmit_time*p_2)

fig = plt.figure(facecolor="white")
plt.plot(child_nums,time_overall_1, label='method1')
plt.plot(child_nums,time_overall_2, label='method2')
plt.xlabel('child_num')
plt.ylabel('time_overall')
plt.legend() 
plt.show()