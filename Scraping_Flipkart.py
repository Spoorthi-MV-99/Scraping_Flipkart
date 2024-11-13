#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


# In[3]:


url = 'https://www.flipkart.com/search?q=mobile+phones+under+50000&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_6_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_6_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=mobile+phones+under+50000&requestId=f6d522a6-3960-4b67-8d1f-a7804de10186&page=1'


# In[4]:


r = requests.get(url , headers = headers)
print(r)


# In[5]:


soup = BeautifulSoup(r.text, 'lxml')


# In[6]:


np = soup.find('a', class_ = '_9QVEpD').get('href')
print(np)


# In[7]:


cnp = "https://www.flipkart.com/" + np
print(cnp)


# In[8]:


for i in range(2, 21):
    url = 'https://www.flipkart.com/search?q=mobile+phones+under+50000&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_6_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_6_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=mobile+phones+under+50000&requestId=f6d522a6-3960-4b67-8d1f-a7804de10186&page=' + str(i)
    r = requests.get(url, headers=headers)
    print(f"Status Code for Page: {r.status_code}")

    soup = BeautifulSoup(r.text, 'lxml')
    
    # Attempt to find the element
    np_element = soup.find('a', class_='_9QVEpD')
    if np_element:
        np = np_element.get('href')
        cnp = 'https://www.flipkart.com' + np
        print(cnp)
    else:
        print(f"Element with class '_9QVEpD' not found on page {i}")


# In[16]:


Names_list = []
Price_list = []
Desc_list = []
Reviews_list = []


for i in range(10,40):
    

    url = 'https://www.flipkart.com/search?q=mobile+phones+under+50000&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_6_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_6_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=mobile+phones+under+50000&requestId=f6d522a6-3960-4b67-8d1f-a7804de10186&page='+ str(i)
    r = requests.get(url , headers = headers)
    print(r)
     
    soup = BeautifulSoup(r.text, 'lxml')

    box = soup.find('div', class_ = 'DOjaWF gdgoEp')

    names = box.find_all('div', class_ = 'KzDlHZ')

    for i in names:
        n = i.text
        Names_list.append(n)
    print(Names_list)

    prices = box.find_all('div', class_ = 'Nx9bqj _4b5DiR')

    for i in prices:
        p = i.text
        Price_list.append(p)
    print(Price_list)

    desc = box.find_all('ul', class_ = 'G4BRas')

    for i in desc:
        d = i.text
        Desc_list.append(d)
    print(Desc_list)


    reviews = box.find_all('div', class_ = 'XQDdHH')

    for i in reviews:
        rev = i.text
        Reviews_list.append(rev)
    print(Reviews_list)


# In[17]:


print(len(Names_list))
print(len(Price_list))
print(len(Desc_list))
print(len(Reviews_list))


# In[18]:


df = pd.DataFrame({'Product Name': Names_list,'Product Price': Price_list, 'Product Description': Desc_list, 'Reviews': Reviews_list})
print(df)

df.to_csv("FlipkartMobiles.csv")


# In[20]:


df.to_csv("FlipKartMobiles.csv")


# ### Lets us Load and Inspect Data

# In[5]:


import pandas as pd

file_path = "C:\\Users\\brunda\\anaconda3\\Python\\WebScrapping\\FlipkartMobiles.csv"
data = pd.read_csv(file_path)


# In[6]:


data.head()


# ### Data Cleaning

# In[7]:


missing_values = data.isnull().sum()
print(missing_values)


# In[9]:


duplicates = data.duplicated().sum()
print(duplicates)


# In[11]:


data_types = data.dtypes
print(data_types)


# In[14]:


# Remove non-numeric characters and convert to float
data['Product Price'] = data['Product Price'].replace('[\$,₹]', '', regex=True)  # Adjust symbol as needed
data['Product Price'] = data['Product Price'].replace(',', '', regex=True)       # Remove commas if present
data['Product Price'] = data['Product Price'].astype(float)  # Convert to float

# Verify the conversion
data['Product Price'].dtypes, data['Product Price'].head()


# ### Exploratory Data Analysis (EDA)
# 

# In[15]:


data.describe()


# In[16]:


# Count unique values in categorical columns to identify the categories present
categorical_columns = data.select_dtypes(include=['object']).columns
unique_values = {col: data[col].nunique() for col in categorical_columns}
unique_values


# ### Distribution of key variables
# 

# In[17]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[19]:


# Plotting price distribution
plt.figure(figsize=(10, 6))
sns.histplot(data['Product Price'], kde=True, bins=30)
plt.title("Price Distribution of Mobiles")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()


# - The distribution appears to be right-skewed, with a few mobiles at high price points pulling the tail to the right.
# - The majority of mobiles are in the budget to mid-range category, with fewer premium or high-cost mobiles.

# ### Plotting rating distribution

# In[20]:


plt.figure(figsize=(10, 6))
sns.histplot(data['Reviews'], kde=True, bins=20)
plt.title("Rating Distribution of Mobiles")
plt.xlabel("Reviews")
plt.ylabel("Frequency")
plt.show()


# - The distribution looks approximately normal (bell-shaped), centered around a rating of 4 to 4.5, indicating that most mobiles have received average to good ratings.
# - Ratings lower than 3.5 or higher than 4.5 are less common, suggesting that mobile ratings tend to cluster around the middle-to-high range.
# - This indicates that mobile performance and customer satisfaction are generally consistent and satisfactory across most models.

# ### Visualization by Categories
# 

# In[25]:


# Calculate the average price by brand and sort to get the top 10
top_10_brands_by_price = data.groupby('Product Name')['Product Price'].mean().sort_values(ascending=False).head(10)
print(top_10_brands_by_price)


# In[41]:


# Plotting the top 10 brands by average price
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
top_10_brands_by_price.plot(kind='barh', color='skyblue')
plt.title("Top 10 Mobiles by Average Price")
plt.xlabel("Average Price")
plt.ylabel("Product")
plt.gca().invert_yaxis()  # Invert y-axis to show the highest price at the to
plt.ylabel("Product")
plt.show()


# In[28]:


# Calculate the average price by brand and sort to get the Least 10
bottom_10_brands_by_price = data.groupby('Product Name')['Product Price'].mean().sort_values(ascending=False).tail(10)
print(bottom_10_brands_by_price)


# In[40]:


plt.figure(figsize=(12, 8))
bottom_10_brands_by_price.plot(kind='barh', color='skyblue')
plt.title("Top 10 Mobiles by Average Price")
plt.xlabel("Average Price")
plt.ylabel("Product")
plt.gca().invert_yaxis()  # Invert y-axis to show the highest price at the to
plt.ylabel("Product")
plt.show()


# #### Top 10 Brands by Average Rating

# In[30]:


# Calculate the average rating by brand and sort to get the top 10
top_10_by_rating = data.groupby('Product Name')['Reviews'].mean().sort_values(ascending=False).head(10)
print(top_10_by_rating)



# In[39]:


# Plotting the top 10 brands by average rating
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
top_10_by_rating.plot(kind='barh', color='salmon')
plt.title("Top 10 Mobiles by Average Rating")
plt.xlabel("Average Rating")
plt.ylabel("Product")
plt.gca().invert_yaxis()  # Invert y-axis to show the highest rated brands at the top
plt.show()


# #### Least 10 Products by Average Rating:

# In[37]:


# Calculate the average rating by brand and sort to get the least 10
least_10_by_rating = data.groupby('Product Name')['Reviews'].mean().sort_values(ascending=True).head(10)
print(least_10_by_rating)


# In[38]:


# Plotting the least 10 brands by average rating
plt.figure(figsize=(12, 8))
least_10_by_rating.plot(kind='barh', color='lightgreen')
plt.title("Least 10 Mobiles by Average Rating")
plt.xlabel("Average Rating")
plt.ylabel("Product")
plt.gca().invert_yaxis()  # Invert y-axis to show the lowest rated brands at the top
plt.show()


# In[42]:


# Correlation matrix
correlation_matrix = data.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Matrix")
plt.show()


# #### High-Priority Segmentation Analysis
# Goal: Segment customers or devices by price tiers (e.g., budget, mid-range, premium).
# Method: Define tiers based on price ranges, then analyze the number of models, average rating, and common features in each segment.

# In[52]:


bins = [0, 10000, 20000, 50000, 100000]  # Adjust as necessary
labels = ['Budget', 'Mid-Range', 'High-End', 'Premium']
data['Price_Tier'] = pd.cut(data['Product Price'], bins=bins, labels=labels)
tier_analysis = data.groupby('Price_Tier').agg({
    'Product Name': 'count',
    'Reviews': 'mean'
})
tier_analysis.plot(kind='bar', title="Device Segmentation by Price Tier")


# In[50]:


print(tier_analysis)


# In[ ]:




