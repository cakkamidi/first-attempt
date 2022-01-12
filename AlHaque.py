#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import matplotlib.pyplot as plt

def main():

 data_cust = pd.read_csv('olist_customers_dataset.csv')
 data_geo = pd.read_csv('olist_geolocation_dataset.csv')
 data_itm = pd.read_csv('olist_order_items_dataset.csv')
 data_pay = pd.read_csv('olist_order_payments_dataset.csv')
 data_rev = pd.read_csv('olist_order_reviews_dataset.csv')
 data_ord = pd.read_csv('olist_orders_dataset.csv')
 data_prod = pd.read_csv('olist_products_dataset.csv')
 data_prod_cat = pd.read_csv('product_category_name_translation.csv')
 data_sllr = pd.read_csv('olist_sellers_dataset.csv')



#Obtain Date Type Data
 data_ord['order_purchase_timestamp'] = pd.to_datetime(data_ord['order_purchase_timestamp'])



#Filter Completed Orders
 ord_status_deliv = data_ord.loc[data_ord['order_status'] == 'delivered']
 ord_status_deliv['order_id'].groupby([ord_status_deliv['order_purchase_timestamp'].dt.year, ord_status_deliv['order_purchase_timestamp'].dt.month]).agg({'count'})



#Monthly Revenue Data
 items = pd.merge(data_itm, ord_status_deliv, how='inner', on=['order_id'])
 revenue = (items['order_item_id'])*(items['price'])
 items['revenue'] = revenue
 total_revenue = items['revenue'].groupby([items['order_purchase_timestamp'].dt.year, items['order_purchase_timestamp'].dt.month]).sum()
 print(total_revenue)



#Customer Distribution Data
 print(data_cust['customer_state'].value_counts())



#Graph Monthly Revenue
 rvn = items['revenue'].groupby([items['order_purchase_timestamp'].dt.year, items['order_purchase_timestamp'].dt.month]).sum().plot(grid=True, kind = "bar", title='Monthly Revenue')
 rvn.set_xlabel("Month")
 rvn.set_ylabel("Revenue")
 rvn.ticklabel_format(useOffset=False, style='plain', axis='y')



#Filter Customer by Year
 cust = pd.merge(data_cust, items, how='inner', on=['customer_id'])
 cust_16 = cust.loc[cust['order_purchase_timestamp'].dt.year == 2016]
 cust_17 = cust.loc[cust['order_purchase_timestamp'].dt.year == 2017]
 cust_18 = cust.loc[cust['order_purchase_timestamp'].dt.year == 2018]



 cust_16.loc[~cust_16['customer_state'].isin(cust_16['customer_state'].value_counts()[:7].index), 'customer_state'] = 'Others'



#Graph Customers Distribution 2016
 cust_16['customer_state'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, title='Customers States Distribution 2016')


 cust_17.loc[~cust_17['customer_state'].isin(cust_17['customer_state'].value_counts()[:7].index), 'customer_state'] = 'Others'


#Graph Customers Distribution 2017
 cust_17['customer_state'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, title='Customers States Distribution 2017')


 cust_18.loc[~cust_18['customer_state'].isin(cust_18['customer_state'].value_counts()[:7].index), 'customer_state'] = 'Others'


#Graph Customers Distribution 2018
 cust_18['customer_state'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, title='Customers States Distribution 2018')

#Categorize Order Status
 data_ord.loc[~data_ord['order_status'].isin(['delivered','canceled','unavailable']), 'order_status'] = 'ongoing'
 data_ord.loc[~data_ord['order_status'].isin(['delivered','ongoing']), 'order_status'] = 'not processed'


#Completed Orders Percentage
 stts = data_ord['order_status'].value_counts().plot(kind='pie', startangle=90, title='Completed Orders', labels=None)
 stts.legend(loc=4, labels=data_ord['order_status'].value_counts().index)



#Top 10 Best Seller Categories
 prod_cat = pd.merge(items, data_prod, how='inner', on=['product_id'])
 prod_cat_eng = pd.merge(prod_cat, data_prod_cat, how='inner', on=['product_category_name'])

 print("Top 10 Best Selling Categories :\n\n", prod_cat_eng['product_category_name_english'].value_counts().head(10), "\n")



#Top Categories by Year
 prod_16 = prod_cat_eng.loc[prod_cat_eng['order_purchase_timestamp'].dt.year == 2016]
 prod_17 = prod_cat_eng.loc[prod_cat_eng['order_purchase_timestamp'].dt.year == 2017]
 prod_18 = prod_cat_eng.loc[prod_cat_eng['order_purchase_timestamp'].dt.year == 2018]

 print("2016 Top 10 Best Selling Categories :\n\n", prod_16['product_category_name_english'].value_counts().head(10), "\n")
 print("2017 Top 10 Best Selling Categories :\n\n", prod_17['product_category_name_english'].value_counts().head(10), "\n")
 print("2018 Top 10 Best Selling Categories :\n\n", prod_18['product_category_name_english'].value_counts().head(10), "\n")


#Users Active Time
 cust['order_purchase_timestamp'].dt.hour.value_counts().sort_index().plot(kind='bar', grid=True, title='Users Active Time')


if __name__ == "__main__":
 main()