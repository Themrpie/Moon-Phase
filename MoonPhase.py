import math, csv, random

import numpy as np
import pandas as pd
import talib
import ephem
import datetime as dt
import datetime

## ------------------------------------------------
##  DEFAULT VARIABLES (do not delete them)
##
file_name_base = "C:/Users/pietr/TradersToolbox/TradersToolbox/Data/GCRaw.txt"
file_name_market2 = None
file_name_market3 = None
file_name_Vix = None
start = dt.datetime(2010,1,1)
stop  = dt.datetime(2011,1,1)
df1, df2, df3, dfV = None, None, None, None

## ------------------------------------------------
##  Read data
##
def ReadData():
        global df1
        df1 = pd.read_csv(file_name_base, delimiter=',', index_col='Date', parse_dates=True)
        df1 = df1[df1.index >= start]
        df1 = df1[df1.index <= stop]

        if file_name_market2 != None and len(file_name_market2) > 0:
                global df2
                df2 = pd.read_csv(file_name_market2, delimiter=',', index_col='Date', parse_dates=True)
                df2 = df2[df2.index >= start]
                df2 = df2[df2.index <= stop]

        if file_name_market3 != None and len(file_name_market3) > 0:
                global df3
                df3 = pd.read_csv(file_name_market3, delimiter=',', index_col='Date', parse_dates=True)
                df3 = df3[df3.index >= start]
                df3 = df3[df3.index <= stop]

        if file_name_Vix != None and len(file_name_Vix) > 0:
                global dfV
                dfV = pd.read_csv(file_name_Vix, delimiter=',', index_col='Date', parse_dates=True)
                dfV = dfV[dfV.index >= start]
                dfV = dfV[dfV.index <= stop]


## ------------------------------------------------
##  USER VARIABLES and CODE section
##
def get_phase_on_day(year,month,day):
          """Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new"""
          #Ephem stores its date numbers as floating points, which the following uses
          #to conveniently extract the percent time between one new moon and the next
          #This corresponds (somewhat roughly) to the phase of the moon.

          date=ephem.Date(datetime.date(year,month,day))

          nnm = ephem.next_new_moon(date)
          pnm = ephem.previous_new_moon(date)

          lunation=(date-pnm)/(nnm-pnm)
          #lunation=0
          #Note that there is a ephem.Moon().phase() command, but this returns the
          #percentage of the moon which is illuminated. This is not really what we want.

          return lunation

## ------------------------------------------------
##  CUSTOM INDICATOR FUNCTION
##  (main entry point called from TradersToolbox)
##
def GetCustomSignal():
        ReadData()
        ## -------------------------------------------------
        ## Write signal calculation here
        ##
        global df1
        df1['DateDate'] = [d.to_pydatetime() for d in df1.index]
        df1['Lunation'] = [get_phase_on_day(d.year,d.month,d.day) for d in df1['DateDate']]
        Signal = [1 if l < 0.52 and l > 0.48 else 0 for l in df1['Lunation']]
        
        ## -------------------------------------------------
        ## Should return list of int (same length as Close)
        ##
        return Signal
