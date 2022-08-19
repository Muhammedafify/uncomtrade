import pandas as pd
import time
from timeit import default_timer as timer
start = timer()


#Here we can insert the link in the bottom of the inquiry in the UNcomtrade.com website 
# we should edit the following ("max=150000" instead of "max=502" , add "&fmt=csv" in the end , use "/get/plut?"  instead of "/get?" )
egy_general=   'http://comtrade.un.org/api/get/plus?max=150000&type=C&freq=A&px=HS&ps=2017&r=818&p=all&rg=2%2C1&cc=AG6&fmt=csv'
#Choose any years you want the data for 
years_list = [2015,2016,2017,2018,2019,2020,2021]
#same as URL above
req_urls = [egy_general] 
 # any name you wish for the output file
file_names = ['egy_general']




list_of_frames = []
for i in range(len(req_urls)): 
    query_url = req_urls[i]
    output_file_name = file_names[i]
    print('Working on {}.'.format(output_file_name))
    print(query_url)
    for year in years_list:
        print("-"*50)
        print('Now getting data for the year: {}'.format(year))
        print("-"*50)
        url = query_url[:query_url.index('ps=')+3] +str(year)+query_url[query_url.index('ps=')+3+4:]
        list_of_frames.append(pd.read_csv(url,low_memory=False))
        time.sleep(3)

df_total = pd.concat(list_of_frames)
df_total = df_total[['Year','Reporter','Partner','Mode of Transport','Commodity Code','Commodity','Trade Flow','Trade Value (US$)']]
df_total.to_csv(output_file_name+'.csv' , index =False)  #Saving raw data and then later will save a new file as analysis

df_exp = df_total.query("`Trade Flow` == 'X' & `Mode of Transport` == 'TOTAL MOT'")
df_exp.rename(columns ={"Trade Value (US$)":"exp_value (US$)"}, inplace = True)
df_imp = df_total.query("`Trade Flow` == 'M' & `Mode of Transport` == 'TOTAL MOT'")
df_imp.rename(columns ={"Trade Value (US$)":"imp_value (US$)"}, inplace = True)
df = pd.concat([df_exp,df_imp])
df.drop(['Trade Flow','Mode of Transport'], axis = 1,inplace = True)
df.to_csv(output_file_name+'_clean.csv' , index =False)

print(df_total.shape)
print(df_total['Year'].value_counts())
print(df_total.info())
print(df_total.head())
print("-"*50)
print("-"*50)
print("-"*50)
end = timer()
print("This script took {} seconds to operate.".format(end - start))
