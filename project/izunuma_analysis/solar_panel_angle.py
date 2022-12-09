# 東から反時計回りの角度aと縦の角度b                                                                                                                                                                                                                                                                                    
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

min_diff = 10**6
min_c = 0
min_d = 0
a = np.radians(30)
b = np.radians(75)

for c_change in range(1,89):
    for d_change in range(1,89):

        c = np.radians(c_change)
        d = np.radians(d_change)


        optimal_v = [0,0,0,0,-np.sin(np.radians(33)),np.cos(np.radians(33))]
        optimal_v = [0,0,0,0,-np.sin(np.radians(33))/np.linalg.norm(np.array(optimal_v[3:])),np.cos(np.radians(33))/np.linalg.norm(np.array(optimal_v[3:]))]
        v1 = [0, 0, 0, np.cos(b)*np.cos(a), np.cos(b)*np.sin(a), np.sin(b)]
        v2 = [v1[3], v1[4], v1[5], 1,np.tan(a-c),- (np.cos(a)+np.sin(a)*np.tan(a-c))/np.tan(b)]
        v2 = [v1[3], v1[4], v1[5], 1/np.linalg.norm(np.array(v2[3:])),np.tan(a-c)/np.linalg.norm(np.array(v2[3:])),- (np.cos(a)+np.sin(a)*np.tan(a-c))/(np.tan(b)*np.linalg.norm(np.array(v2[3:])))]
        v3 = [v2[0]+v2[3], v2[1]+v2[4], v2[2]+v2[5], 1, np.tan(a-c-d), np.tan(b)*np.cos(a-c)*(np.tan(a-c)*np.tan(a-c-d)+1)/np.cos(c)]
        v3 = [v2[0]+v2[3], v2[1]+v2[4], v2[2]+v2[5], 1/np.linalg.norm(np.array(v3[3:])), np.tan(a-c-d)/np.linalg.norm(np.array(v3[3:])), np.tan(b)*np.cos(a-c)*(np.tan(a-c)*np.tan(a-c-d)+1)/(np.cos(c)*np.linalg.norm(np.array(v3[3:])))]
        soa = np.array([optimal_v,v1,v2,v3])


        v3_2 = v3[3:]/np.linalg.norm(np.array(v3[3:]))
        optimal_v_2 = optimal_v[3:]/np.linalg.norm(np.array(optimal_v[3:]))
        # print(v3_2)
        # print(optimal_v_2)
        # print("diff="+str(np.linalg.norm(v3_2-optimal_v_2)))
        if np.linalg.norm(v3_2-optimal_v_2) < min_diff:
            min_diff = np.linalg.norm(v3_2-optimal_v_2)
            min_c = c_change
            min_d = d_change

c = np.radians(min_c)
d = np.radians(min_d)

optimal_v = [0,0,0,0,-np.sin(np.radians(33)),np.cos(np.radians(33))]
optimal_v = [0,0,0,0,-np.sin(np.radians(33))/np.linalg.norm(np.array(optimal_v[3:])),np.cos(np.radians(33))/np.linalg.norm(np.array(optimal_v[3:]))]
v1 = [0, 0, 0, np.cos(b)*np.cos(a), np.cos(b)*np.sin(a), np.sin(b)]
v2 = [v1[3], v1[4], v1[5], 1,np.tan(a-c),- (np.cos(a)+np.sin(a)*np.tan(a-c))/np.tan(b)]
v2 = [v1[3], v1[4], v1[5], 1/np.linalg.norm(np.array(v2[3:])),np.tan(a-c)/np.linalg.norm(np.array(v2[3:])),- (np.cos(a)+np.sin(a)*np.tan(a-c))/(np.tan(b)*np.linalg.norm(np.array(v2[3:])))]
v3 = [v2[0]+v2[3], v2[1]+v2[4], v2[2]+v2[5], 1, np.tan(a-c-d), np.tan(b)*np.cos(a-c)*(np.tan(a-c)*np.tan(a-c-d)+1)/np.cos(c)]
v3 = [v2[0]+v2[3], v2[1]+v2[4], v2[2]+v2[5], 1/np.linalg.norm(np.array(v3[3:])), np.tan(a-c-d)/np.linalg.norm(np.array(v3[3:])), np.tan(b)*np.cos(a-c)*(np.tan(a-c)*np.tan(a-c-d)+1)/(np.cos(c)*np.linalg.norm(np.array(v3[3:])))]

v1_ref = [v1[3], v1[4], v1[5], -v1[3], -v1[4], (v1[3]**2 + v1[4]**2) / v1[5]]

soa = np.array([optimal_v,v1,v2,v3,v1_ref])

v3_2 = v3[3:]/np.linalg.norm(np.array(v3[3:]))
optimal_v_2 = optimal_v[3:]/np.linalg.norm(np.array(optimal_v[3:]))

print(min_c, min_d)
theta1 = np.arccos((v1_ref[3]*v2[3]+v1_ref[4]*v2[4]+v1_ref[5]*v2[5]) / (np.sqrt(v1_ref[3]**2+v1_ref[4]**2+v1_ref[5]**2)*np.sqrt(v2[3]**2+v2[4]**2+v2[5]**2)))
theta2 = np.arccos((v1_ref[3]*v3[3]+v1_ref[4]*v3[4]+v1_ref[5]*v3[5]) / (np.sqrt(v1_ref[3]**2+v1_ref[4]**2+v1_ref[5]**2)*np.sqrt(v3[3]**2+v3[4]**2+v3[5]**2)))
print(np.rad2deg(theta1), np.rad2deg(theta2))
print("diff="+str(np.linalg.norm(v3_2-optimal_v_2)))



print(soa)
X, Y, Z, U, V, W = zip(*soa)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, U, V, W)
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([0, 2])
plt.show()