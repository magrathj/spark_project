# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% [markdown]
# # Reading and Writing Data with Spark
# 
# This notebook contains the code from the previous screencast. The only difference is that instead of reading in a dataset from a remote cluster, the data set is read in from a local file. You can see the file by clicking on the "jupyter" icon and opening the folder titled "data".
# 
# Run the code cell to see how everything works. 
# 
# First let's import SparkConf and SparkSession


#%%
import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession
import zipfile, io, os
import pandas as pd 
from pyspark import SparkContext, SparkConf



#%% [markdown]
# Since we're using Spark locally we already have both a sparkcontext and a sparksession running. We can update some of the parameters, such our application's name. Let's just call it "Our first Python Spark SQL example"



#%%
spark = SparkSession.builder.appName("NFIP Dataset").getOrCreate()

#%% [markdown]
# Let's check if the change went through

#%%
spark.sparkContext.getConf().getAll()


#%%
spark




#%% [markdown]
# Lets grab all the files in the directory

#%% 

import glob

path = 'C:\\Users\\jmagr\\Downloads\\policy_output'
files = [f for f in glob.glob(path + "**/*.csv", recursive=True)]

for f in files:
    print(f)




#%% [markdown]
# And just split them into claims and policy dataframes


#%% 

claims_path = [filename for filename in files if filename.endswith("openFEMA_claims20190531.csv")]
df_claims = spark.read.format("csv").option("header","true").option("mode","DROPMALFORMED").load(claims_path[0])

df_claims.printSchema() 



#%% 

policies_path = [filename for filename in files if not filename.endswith("openFEMA_claims20190531.csv")]
df_policies_1 = spark.read.format("csv").option("header","true").option("mode", "DROPMALFORMED").load(policies_path[0])

df_policies_1.printSchema() 


#%% 

for policies in policies_path[1:]:
    df_policies = spark.read.format("csv").option("header","true").option("mode","DROPMALFORMED").load(policies) 
    df_policies_1.union(df_policies)


df_policies_1.printSchema() 


#%%
df_claims.describe().show()


#%%
df_policies_1.describe().show()


#%% [markdown]
# Now lets cut the policy and claims dataset down to just NY
# then lets write to disk



#%%
df_claims_out = df_claims.filter(df_claims.state == "NY")
df_claims_out.take(1)



#%%
df_policies_1_out = df_policies_1.filter(df_policies_1.propertystate == "NY")
df_policies_1_out.take(1)



#%%
df_claims_out.toPandas().to_csv('claims.csv')


#%%
df_policies_1_out.toPandas().to_csv('policies.csv')



#%%


