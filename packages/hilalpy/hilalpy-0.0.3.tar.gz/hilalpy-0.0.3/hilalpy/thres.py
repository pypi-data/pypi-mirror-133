import os,glob
#import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt
import seaborn as sns

def thres (path,figure,csv_stats,csv_maxmin,x):
    #convert all varible to positive.
    df = pd.read_csv(path)
    df[x] = abs(df[x])
    #df=df[(df[x] <= 20)]

    #Only take Visible Data
    df = df[df['V'] =='V']

    #Only Take Evening Observation
    df = df[df['O'] =='E']

    ##Generate the Boxplot
    a =sns.boxplot( y=df["M"], x=df[x],showfliers=False )
    plt.show()
    fig = a.get_figure()
    fig.savefig(figure)

    #Generate Statistics
    dft = df[["M",x]] 
    df_by_m = dft.groupby('M')
    df_by_m.describe().to_csv(csv_stats)

    #find Naked Eye Minimum
    dfne = df[df['M'] =='NE']
    dfne = dfne[dfne[x] == min(dfne[x])]

    #Find Optical Aided Minumum
    dfoa = df[df['M'] =='OA']
    dfoa = dfoa[dfoa[x] == min(dfoa[x])]

    #Combine Naked Eye & Optical Aided
    dfc=pd.concat([dfne, dfoa], axis=0)

    #Drop Unnesscary Column
    dfc=dfc.drop(['Phase Angle', 'Illuminated Fraction', 'Observed Moon Brightness', 'Twilight Sky Brightness', 'Contrast', 'Ele', 'Moonset', 'V', 'Sunset','TZ','O',"NE",'B','T','CCD','witness','Cloud Condition','Atmoshperic Condition','Moon Longitude','SML','Ref'], axis = 1)

    #Output Min Value
    dfc.to_csv( csv_maxmin, index=False, encoding='utf-8-sig')
    

