import pandas as pd
import streamlit as st

url = 'https://raw.githubusercontent.com/NelliKS/Final_project/refs/heads/main/Electricity_20-09-2024.csv?token=GHSAT0AAAAAACZWTALD2HI4KIIL6QEVSURMZZCTHXQ'
url2 = os.getcwd() + '/Desktop/Data_analytics/data_maths/final work/data/sahkon-hinta-010121-240924.csv'
df_electricity = pd.read_csv(url, delimiter=';', decimal = ',')

df_price = pd.read_csv(path2)

df_electricity['Time'] = pd.to_datetime(df_electricity['Time'], format = 'mixed')
df_price['Time'] = pd.to_datetime(df_price['Time'], format = '%d-%m-%Y %H:%M:%S')


df_merged = pd.merge(df_electricity,df_price,on=['Time'], how ='left')

df_merged['bill'] = df_merged['Energy (kWh)']*df_merged['Price (cent/kWh)']

#streamlit data input
start_date = st.date_input('Start date') 
end_date = st.date_input('End date') 
df_range = df_merged[df_merged['Time'].isin(pd.date_range(start_date,end_date))]

#df_merged[(df_merged['Time'] >= start_date) & (df_merged['Time'] <= end_date)]
#variables
total_consumption = df_range['Energy (kWh)'].sum()
total_bill = df_range['bill'].sum() / 100
avg_hourly_price = df_range['Price (cent/kWh)'].mean()

#show chosen date range
st.write('Showing range ', start_date, ' - ',end_date)
st.write('Total comsumption over the period:', total_consumption ,' kWh') #define here the variable that gives this
st.write('Total bill over the period: ',total_bill, '€')
st.write('Average hourly price: ',avg_hourly_price, 'cents')
#st.write('Average paid price')


#averaging period
avg_options = ['Daily','Weekly','Monthly']
option_selected = st.selectbox('Averaging period:', options = avg_options)

if option_selected == 'Daily':
    chosen_option = 'd'
elif option_selected == 'Weekly':
    chosen_option = '7d'
elif option_selected == 'Monthly':
    chosen_option = 'm'

df_visu = (df_range.groupby(pd.Grouper(key = 'Time', freq = chosen_option))[['Price (cent/kWh)', 'Temperature','Energy (kWh)', 'bill']].mean()).reset_index()

#draw electricity consumption
st.line_chart(df_visu, x = 'Consumption' ,y= df_visu['Energy (kWh)'], y_label='Electricity consumption (kWh)')

#draw electricity price
st.line_chart(df_visu, y= df_visu['Price (cent/kWh)'], y_label='Electricity price (cents)')

#draw bill amount
st.line_chart(df_visu, y = df_visu['bill'], y_label='Electricity bill (€')

#draw temperature
st.line_chart(df_visu, y = df_visu['emperature'], y_label='Temperature')
