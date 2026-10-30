import pandas as pd
import numpy as np

df = pd.read_csv('File Date/ecommerce_orders_dataset.csv')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


print(df.head())
print(df.shape)
print(df.index)
print(df.info())
print(df.isnull().sum())
print(df.describe().T)
print(df['Order_ID'].count() == df['Customer_ID'].count())


df.columns = df.columns.str.strip().str.replace(' ', '_').str.capitalize()
print(df.head())

Text_columns = ['Customer_gender', 'Country', 'City', 'Customer_segment',
                'Product_category', 'Product_subcategory', 'Brand',
                'Coupon_used', 'Payment_method', 'Device_type', 'Traffic_source',
                'Membership_status', 'Shipping_method', 'Warehouse_region',
                'Order_status', 'Returned', 'Season']

for i in Text_columns:
    df[i] = df[i].astype(str).str.strip().str.title()
print(df.head())

df['Order_date'] = pd.to_datetime(df['Order_date'])
df['Year'] = pd.to_datetime(df['Order_date']).dt.year
df['Month'] = pd.to_datetime(df['Order_date']).dt.to_period('M')
df['Day'] = pd.to_datetime(df['Order_date']).dt.day

df = df.rename(columns={'Profit_amount': 'Total_profit'})


df['Total_amount'] = ((df['Unit_price'] * df['Quantity']) -
                      (df['Discount_amount'])) + (df['Shipping_cost'] + df['Tax_amount'])
print(df['Total_amount'].head())

df['Total_cost'] = df['Total_amount'] - df['Total_profit']
print(df['Total_cost'].head())

df['Profit_margin_percentage'] = round(
    (df['Total_profit'] / df['Total_amount']) * 100, 2)
print(df['Profit_margin_percentage'].head())


# Executive Overview
# KPI

Total_Revenue = round(df['Total_amount'].sum(), 2)
print(Total_Revenue)

Total_Quantity = df['Quantity'].sum()
print(Total_Quantity)

Total_cost = round(df['Total_cost'].sum(), 2)
print(Total_cost)

AVg_Review_Rating = round(df['Review_rating'].mean(), 2)
print(AVg_Review_Rating)

profit_Margin = round(
    (df['Total_profit'].sum() / df['Total_amount'].sum()) * 100, 2)
print(profit_Margin)


Revenue_Over_Time = df.groupby('Year').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Revenue_Over_Time)

Revenue_by_Country = df.groupby('Country').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Revenue_by_Country)

Revenue_by_brand = df.groupby('Brand').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Revenue_by_brand)

Total_Revenue_by_Season = df.groupby('Season').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Total_Revenue_by_Season)

Order_Statues_percentage = (df['Order_status'
                               ].value_counts(normalize=True) * 100).round(2)
print(Order_Statues_percentage)


# Product & Profitability
# KPI
Total_Profit = round(df['Total_profit'].sum(), 2)
print(Total_Profit)

Total_Quantity = df['Quantity'].sum()
print(Total_Quantity)

Total_Products = df['Product_id'].nunique()
print(Total_Products)


Revenue_by_Category = df.groupby('Product_category').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Revenue_by_Category)

Top10_Revenue_by_Subcategory = df.groupby('Product_subcategory').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Top10_Revenue_by_Subcategory.head(10))

Count_Product_by_Traffic_source = df.groupby('Traffic_source').agg(
    Total_Products=('Product_id', 'nunique')
).reset_index()
print(Count_Product_by_Traffic_source)

Per_revenue_by_Payment_method = (
    df.groupby('Payment_method')['Total_amount'].sum()
    / df['Total_amount'].sum() * 100
).round(2).reset_index(name='Percentage')
print(Per_revenue_by_Payment_method)


# Customer Analysis
# KPI

Avg_Customer_Age = round(df['Customer_age'].mean(), 2)
print(Avg_Customer_Age)

Total_Customer = df['Customer_id'].nunique()
print(Total_Customer)

Avg_Customer_Lifetime_Value = round(df['Customer_lifetime_value'].mean(), 2)
print(Avg_Customer_Lifetime_Value)


Total_revenue_by_Customer_Segment = df.groupby('Customer_segment').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Total_revenue_by_Customer_Segment)

Total_Coustomer_by_Traffic_Source = df.groupby('Traffic_source').agg(
    Total_Customer=('Customer_id', 'nunique')
).reset_index()
print(Total_Coustomer_by_Traffic_Source)

Avg_Review_Rating_over_time = (
    df.groupby('Order_date')['Review_rating'
                             ].mean().round(2).reset_index(name='Avg_Review_rating'))
print(Avg_Review_Rating_over_time)

Customer_Percentage_by_Gende = (
    df.drop_duplicates('Customer_id')
    ['Customer_gender'].value_counts(normalize=True) * 100).round(2)
print(Customer_Percentage_by_Gende)


# Marketing Performance
# KPI

Avg_order_value = round(df['Total_amount'].sum() / df['Order_id'].nunique(), 2)
print(Avg_order_value)

Avg_discount_Percent = df['Discount_percent'].mean().round(2)
print(Avg_discount_Percent)

Coupon_Used_Rate = round(
    (df['Coupon_used'].eq('Yes').sum() / len(df)) * 100, 2)
print(Coupon_Used_Rate)


Revenue_by_Traffic_source = df.groupby('Traffic_source').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Revenue_by_Traffic_source)

Revenue_by_Brand = df.groupby('Brand').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Revenue_by_Brand)

Total_Profit_by_months = df.groupby('Month').agg(
    Profit=('Total_profit', 'sum')
).sort_index().reset_index()
print(Total_Profit_by_months)

percent_of_Device_type = (
    df['Device_type'].value_counts(normalize=True) * 100
).round(2).reset_index(name='Percentage')
print(percent_of_Device_type)


# Delivery & Returns
# KPI

Avg_Delivery_Days = round(df['Delivery_days'].mean(), 2)
print(Avg_Delivery_Days)

Total_order_Returned = df['Returned'].eq('Yes').sum()
print(Total_order_Returned)

Percent_order_Returned = round(
    (df['Returned'].eq('Yes').sum() / len(df)) * 100, 2
)
print(Percent_order_Returned)


Revenue_by_Shipping_Method = df.groupby('Shipping_method').agg(
    Revenue=('Total_amount', 'sum')
).sort_values('Revenue', ascending=False).reset_index()
print(Revenue_by_Shipping_Method)

Return_Rate_by_Category = df.groupby('Product_category').agg(
    Percent=('Returned', lambda x: (x.eq('Yes').mean() * 100).round(2))
).sort_values('Percent', ascending=False).reset_index()
print(Return_Rate_by_Category)

Avg_Review_Rating_by_Delivery_Days = df.groupby('Delivery_days').agg(
    Avg_Review_Rating=('Review_rating', 'mean')
).round(2).sort_values('Avg_Review_Rating', ascending=False).reset_index()
print(Avg_Review_Rating_by_Delivery_Days)

Percent_of_Order_status = round(
    df['Order_status'].value_counts(normalize=True) * 100, 2
).reset_index(name='Percentage')
print(Percent_of_Order_status)

# df.to_csv('Ecommerce_orders_cleaning.csv', index=False)
