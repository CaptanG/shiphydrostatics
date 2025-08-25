def hydrostatics(AP, FP):
    from mpl_toolkits import mplot3d
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import matplotlib.pyplot as plt
    import numpy as np
    import scipy
    import pandas as pd
    import math as m

    density_seawater = 1.025

    lcg = 47.514
    wt = 3066.67

    file_path = "SecLine.dat"

    # Gets the count of sections
    def sectionNumber(path):
        try:
            with open(path, 'r') as file:

                lines = file.readlines()

                empty_lines = sum(1 for line in lines if line.strip() == '')

                return empty_lines

        except FileNotFoundError:
            print(f"File '{path}' not found.")
            return 0

    # Finds the closest point to the waterline
    def find_closest(arr,value):
        
        for i in range(len(arr)):
            if value<arr[i]:
                break
        idx1=i-1
        idx2=i
        return idx2,idx1

    # Interpolates the point on the waterline from the above and below points
    def interpolate(x1,y1,x2,y2,y=None,x=None):
        if (x2-x1)==0:
            return x1
        m=(y2-y1)/(x2-x1)
        if y is not None:
            x=((y-y1)/(m))+x1
            return x
        if x is not None:
            y=((x-x1)*m)+y1
            return y

    def transform(x,y,theta):
        trans=np.array([[m.cos(theta),-m.sin(theta)],[m.sin(theta),m.cos(theta)]])
        X=np.array([x,y])
        X1=np.matmul(trans,X)
        return X1[0],X1[1]

    def sinWave(case):
        theta=m.atan2(FP-AP,110)
        i=0
        k = (2*m.pi)/110
        Y2 = []
        while i<110:
            yy = AP
            if case==1:
                y1=2*(m.sin(k*i))
            elif case == 2:
                y1=2*(m.sin((k*i)-m.pi))
            new_x,new_y=transform(i,y1,theta)
            Y2.append([new_x,new_y+yy])
            i+=1
        Y2=np.array(Y2)
        return Y2

    # Limit for water depth
    def upto(x, typeFunc):

        if(typeFunc == 'calm'):  
            if(AP == FP):
                z1 = AP
                return z1
            elif(AP != FP):
                z2 = (((FP-AP)/(110-0))*(x-0)) + AP
                return z2

        elif(typeFunc == 'sine'):
            return sine_WL(x)

    def sine_WL(x):
        
        sinCurve = sinWave(case = 2)
        idx2,idx1 = find_closest(sinCurve[:,0],x)
        y=interpolate(sinCurve[idx2,0],sinCurve[idx2,1],sinCurve[idx1,0],sinCurve[idx1,1],x=x)

        return y    

    # Gets the section area till the waterline
    def area_upto(Y,Z,z_lim):
        
        global interpol
        
        idx2,idx1=find_closest(Z,z_lim)

        y_temp=interpolate(Y[idx1],Z[idx1],Y[idx2],Z[idx2],z_lim)
        
        Y=Y[Z<z_lim]
        Z=Z[Z<z_lim]
        
        Y=np.append(Y,[y_temp])
        Z=np.append(Z,[z_lim])

        area=scipy.integrate.trapz(Y,Z)
        
        return area

    # Calculates LCB from the underwater volume
    def getLCB(t,x):
        
        num = 0
        den = 0

        for i in range(len(t)-1):
            a = ((x[i]*t[i]) + (x[i+1]*t[i+1]))*(x[i+1] - x[i])
            b = (t[i+1] + t[i])*(x[i+1] - x[i])        
            num += a
            den += b
        
        return num/den

    # Gets the y coordinate of the section area lying on the waterplane
    def Y_waterplane(Y,Z,z_lim):
        
        global interpol
        
        val,idx=find_closest(Z,z_lim)
        
        if val<z_lim:
            idx1=idx
            idx2=idx+1
        elif val>z_lim:
            idx1=idx-1
            idx2=idx
        elif val==z_lim:
            idx1 = idx
            idx2 = idx
        
        y_temp=interpolate(Y[idx1],Z[idx1],Y[idx2],Z[idx2],z_lim)
        
        return y_temp

    # Calculates the waterplane area
    def waterplaneArea(x,y):
        
        area = scipy.integrate.trapz(y,x)*2

        return area

    # Calculates LCF for the given draft
    def getLCF(x,y):
        numerator=0
        denominator=0
        for i in range(len(x)-1):
            u=((y[i]*x[i])+(y[i+1]*x[i+1]))*(x[i+1]-x[i])
            v=(y[i]+y[i+1])*(x[i+1]-x[i])
            numerator+=u
            denominator+=v
        return numerator/denominator

    # Calulculate the underwater volume
    def underwaterVolume(y,x):

        volume = scipy.integrate.trapz(y,x)*2

        return volume

    # Check how the ship trims
    def getSignature(LCG, LCB):
        if(LCG-LCB < 0):
            return 1
        elif(LCG - LCB > 0):
            return -1
        elif(LCG == LCB):
            return 0

    secNo = sectionNumber(file_path)

    sectionArea = []
    sectionArea_x = []

    fp = open(file_path,'r+')

    a1 = fp.readline()
    a = a1.rstrip('\n').split(',')

    x = float(a[0])
    n = int(a[1])

    Y_wp = np.zeros(secNo)

    c = 0

    while True:
        Y = []
        Z = []

        for i in range(n):
            a = fp.readline().rstrip("\n").split(',')
            Y.append(a[0])
            Z.append(a[1])

        Y = np.array(Y,dtype=float)
        Z = np.array(Z,dtype=float)
        X = np.zeros(n)+x

        sectionArea.append(area_upto(Y,Z,upto(x, typeFunc ='calm')))

        sectionArea_x.append(x)
        Y_wp[c] = float(Y_waterplane(Y,Z,upto(x, typeFunc ='calm')))
        c += 1

        fp.readline()
        a1=fp.readline()
        a=a1.rstrip('\n').split(',')
        if a[0] == '':
            break

        x = float(a[0])
        n = int(a[1])

    sectionArea_x = np.array(sectionArea_x)
    sectionArea = np.array(sectionArea)
    sectionMass = sectionArea*density_seawater*2

    volume = underwaterVolume(sectionArea,sectionArea_x)
    weight = volume*density_seawater
    LCB = getLCB(sectionArea,sectionArea_x)
    WPA = waterplaneArea(sectionArea_x,Y_wp)
    LCF = getLCF(sectionArea_x,Y_wp)

    dict={"volume":volume,"weight":weight,"LCB":LCB,"WPA":WPA,"LCF":LCF,"sectionMass":sectionMass, "stations":sectionArea_x}
    return dict
