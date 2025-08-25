import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import time
from HydrostaticsFunc import hydrostatics as hyd
from weightdistribution import weight as weigh
import functions as fn

lcg = 47.514
wt = 3066.67
density_seawater = 1.025
eps1 = 0.0005 #Relative error for distance
eps2 = 0.005  #Relative error for weight
file_path = "SecLine.dat"
df = pd.read_excel('hydrostatic.xlsx')

draft1 = df["Draft"].to_numpy()
draft = np.asfarray(draft1)
mass1 = df["Mass"].to_numpy()
mass = np.asfarray(mass1/density_seawater)
vol1 = df["Vol"].to_numpy()
vol = np.asfarray(vol1/density_seawater)
lcb1 = df["LCB"].to_numpy()
lcb = np.asfarray(lcb1)
awp1 = df["Awp"].to_numpy()
awp = np.asfarray(awp1)
lcf1 = df["Lcf"].to_numpy()
lcf = np.asfarray(lcf1)


i2, i1 = fn.find_closest(mass, wt)
draftNew = fn.interpolate(draft[i1], mass[i1], draft[i2], mass[i2], wt)
volNew = fn.interpolate(vol[i1], mass[i1], vol[i2], mass[i2], wt)
lcbNew = fn.interpolate(lcb[i1], mass[i1], lcb[i2], mass[i2], wt)
awpNew = fn.interpolate(awp[i1], mass[i1], awp[i2], mass[i2], wt)
lcfNew = fn.interpolate(lcf[i1], mass[i1], lcf[i2], mass[i2], wt)

AP, FP = draftNew, draftNew

iteration = 0
start_time = time.time()

new = hyd(AP, FP)
stations = new["stations"]
length = len(stations)
load = np.zeros(len(stations))
weight_bile = np.zeros(len(stations)) 
weight_constant = np.zeros(len(stations))
shear = np.zeros(len(stations))
bm = np.zeros(len(stations))

#Weight distribution function
weight_func, x_new = weigh()
weight_final = np.zeros(length)
cnt = 0
for i in range(len(stations)):

    if(stations[i] > 0):
        idx2, idx1 = fn.find_closest(x_new, stations[i])
        val = fn.interpolate( weight_func[idx1],  x_new[idx1],  weight_func[idx2],  x_new[idx2], stations[i])
        weight_final[i] = val
    else:
        continue

wt = scipy.integrate.trapz(weight_final, stations)

while True:
    
    iteration += 1

    if(fn.getSignature(lcg, lcbNew) == 1): #Aft trim
        AP += 0.001
        FP -= 0.001
        new = hyd(AP,FP)
        lcbNew = new["LCB"]
    
    if(fn.getSignature(lcg,lcbNew) == -1): #Forward Trim
        AP -= 0.001
        FP += 0.001
        new = hyd(AP,FP)
        lcbNew = new["LCB"]

    if(fn.getSignature(lcg, lcbNew) == 0): #Trim is done, now parallel sinkage
        new = hyd(AP, FP)
        if(abs((wt - new["weight"]))/wt <= eps2):
            print("Nice! Your solution converged!")
            break
        elif((abs(wt - new["weight"]))/wt > eps2):
            
            if(wt > new["weight"]): #Parallel sinkage
                AP += 0.001
                FP += 0.001
                new = hyd(AP,FP)
                lcbNew = new["LCB"]

            if(wt < new["weight"]): #Negative parallel sinkage
                AP -= 0.001
                FP -= 0.001
                new = hyd(AP,FP)
                lcbNew = new["LCB"]

    if(iteration == 10000):
        print("Your solution could not converge, try again next time")
        break
    
    print("{:<20f} {:<20f} {:<20f} {:<20f} {:<20f}".format(iteration,lcbNew,AP,FP,new["weight"]))
end_time = time.time()
elapsed_time = end_time - start_time
print("Time taken: " + str(round(elapsed_time, 4)) + " s")

sectionWeight = -new["sectionMass"]
                     
load = weight_final + sectionWeight

# Shear force and Bending moment calculations
for i in range(length):
    shear[i] = scipy.integrate.trapz(load[:i], stations[:i])
    bm[i] = scipy.integrate.trapz(shear[:i], stations[:i])

print("LCB, LCG, Weight and Bouyancy: " + str(new["LCB"]) +" m, " +str(lcg) + " m, " + str(wt) + " tonnes, " + str(new["weight"]) + " tonnes" )

x_line = np.linspace(0, stations[-1], 11)

plt.subplot(2,2,1)
plt.plot(stations, sectionWeight, label='Bouyancy', color = 'skyblue')
plt.plot(stations,weight_final, label='Weight Distribution', color = 'black')
plt.plot(stations,load, label='Loadline', linestyle='--', color = 'gray')
plt.legend()
plt.grid(alpha=0.3)
plt.xticks(x_line)
plt.title('Weight/Bouyancy/Loadline')
plt.ylabel('Weight (tonnes)')
plt.xlabel('Stations (x)')

plt.subplot(2,2,2)
plt.plot(stations,shear, label='Shear Force')
plt.legend()
plt.grid(alpha=0.3)
plt.xticks(x_line)
plt.title('Shear Force')
plt.ylabel('Shear Force (kN)')
plt.xlabel('Stations (x)')

plt.subplot(2,2,4)
plt.plot(stations,bm, label='Bending Moment')
plt.legend()
plt.grid(alpha=0.3)
plt.xticks(x_line)
plt.title('Bending Moment')
plt.ylabel('Bending Moment (kN-m)')
plt.xlabel('Stations (x)')

plt.show()