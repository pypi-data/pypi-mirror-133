#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Chia Wei Lim
# Created Date: 2021-12-08
# version ='1.0'
# ---------------------------------------------------------------------------
"""Module related to appending period time"""
# ---------------------------------------------------------------------------
from datetime import date
import pandas as pd
import os

class CustomPeriod:

    def __init__(self):
        pathtofile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metadata", "period_dict.csv")
        self.perioddf = pd.read_csv(pathtofile)
        
        self.perioddf = self.perioddf.drop(['month_', 'quarter_', 'half_year_', 'db_month_'], axis = 1)

    def appendperiod(self, df, left_on = "period_code", right_on = "period_code"):

        if left_on not in df.columns: 

            print(f"{left_on} not found in dataframe. Cant append period")
            
        # add checking for df[refcolumn] datatype to check if compatible
        
        return self.perioddf.merge(df, left_on = left_on, right_on = right_on)
        