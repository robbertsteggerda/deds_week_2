import matplotlib.pyplot as plt
import pandas as pd
import pyodbc

DB = {"servername": "DESKTOP-OF0CT86\SQLEXPRESS",
      "database": "greatoutdoors"}

export_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + 
                             ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')


df = pd.read_sql("SELECT * FROM SALES_TargetData", export_conn)

# Plot 1 (2020)
c = df['SALES_YEAR'] == 2020
periods = df.loc[c, 'SALES_PERIOD'].drop_duplicates().to_list()
periods.sort()
print(periods)

x_axis_periods = periods
y_axis_amount_target = 0


# Per product       -       ID: 10
# Per Sales Staff   -       ID: 20

staff_condition = df['SALES_STAFF_CODE'] == 20
product_condition = df['PRODUCT_NUMBER'] == 10

df.loc[[staff_condition, product_condition], :]




# plt.plot(x, y, label = "Target") 
# plt.plot(y, x, label = "Werkelijk verkocht") 



# plt.plot([], [])
# df['SALES_PERIOD'].drop_duplicates().to_list()


# Plot 2 (2021)
# x_year_axis = [df.min()]
# y_target_axis



# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')

# plt.show()