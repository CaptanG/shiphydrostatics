def weight():    
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    file_path = 'Ship_Data_Modified.xlsx'

    df = pd.read_excel(file_path, sheet_name="Sheet7")


    i = 0
    wt = []
    x = []

    while i<83:
        a = round((df.iloc[i,1]-df.iloc[i,0])/0.1)
        for j in range (a): 
            wt.append(df.iloc[i,2])
        
        i += 1
    c = 0
    for j in range(1133):
        x.append(round(c,2))
        c += 0.1

    for j in range(60):
        wt[90+j] = wt[90+j] + 8.43

    for j in range(50):
        wt[20+j] = wt[20+j] + 10.11


    total_wt = np.trapz(wt, x)
    sum = 0

    for j in range(1133):
        sum += wt[j]*x[j]

    LCG = (sum*0.1)/total_wt
    return (wt,x)