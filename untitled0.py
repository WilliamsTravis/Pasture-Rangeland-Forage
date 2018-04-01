# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 12:39:24 2018

@author: trwi0358
"""

df = pd.read_csv("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\PRFIndex_specs.csv")
df = df.rename(columns = {'Unnamed: 0':'Index'})
df.columns
df.columns = ['i','D.I.','A.Y.','I.COV','S','B.R.','S.R.','T.S.',
              'MaxP.($)','MinP.($)','MedP.($)','MeanP.($)','P.SD',
              'M.P.SD', 'MeanPCF','PCFSD','M.PCFSD','MeanP.F.','M.P.FSD']

df = df.round(2)
df.to_csv("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\PRFIndex_specs.csv",index = False)
