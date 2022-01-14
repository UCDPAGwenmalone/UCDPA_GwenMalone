#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import packages required
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


#Import first CSV file from a real world dataset into a pandas dataframe,and verify first few rows 
table_1 = pd.read_csv(r"C:\Users\Ruairi Murphy\OneDrive\New OneDrive\OneDrive\Documents\Data Analytics Project\marketing_campaign table1.csv")
table_1.head()


# In[3]:


#Import second CSV file from a real world dataset into a pandas dataframe,and verify first few rows
table_2 = pd.read_csv(r"C:\Users\Ruairi Murphy\OneDrive\New OneDrive\OneDrive\Documents\Data Analytics Project\marketing_campaign table2.csv")
table_2.head()


# In[4]:


#Look at dimensions (number of rows and columns) of table_1
print(table_1.shape)


# In[5]:


#Look at dimensions (number of rows and columns) of table_2
print(table_2.shape)


# In[6]:


#Show number of rows in both tables together
print("Number of rows table_1:", len(table_1))
print("Number of rows table_2:", len(table_2))


# In[7]:


#Show number of columns in both tables together
print("Number of columns table_1:", table_1.shape[1])
print("Number of columns table_2:", table_2.shape[1])


# In[8]:


#Inspect info for table_1 (note from this can see that the Income column is missing data as there are only 2216 non-nulls and therefore 24 nulls. Can also tell that the Dt_Customer column (date customer joined company) has a data type of object and not DateTime as would be expected)
print(table_1.info())


# In[9]:


#Inspect info for table_2 (note from this can see that there are no columns missing data)
print(table_2.info())


# In[10]:


#Merge table_1 and table_2 (inner join, store as tables, merged on ID column present in both tables)
tables1_2 = table_1.merge(table_2)


# In[11]:


#Verify merged tables
tables1_2.head()


# In[12]:


#Ensure shape of tables1_2 is correct after merge (note - 2240 rows is correct and 29 columns is correct as they were merged on the ID column)
print(tables1_2.shape)


# In[13]:


#Inspect tables1_2 info (note - as previously seen in left table, the Income column is missing data and the Dt_Customer column has a datatype of object)
print(tables1_2.info())


# In[14]:


#Using iloc and slicing, inspect the first 50 rows of columns 26 and 27 to understand the data in these rows better (unsure about 'Z_')
print(tables1_2.iloc[:50, 26:28])


# In[15]:


#From above, all values appear to be the same for both of these columns.
#using sorting, inspect range of values for all rows of these columns closer 
print(tables1_2['Z_CostContact'],tables1_2['Z_Revenue'].sort_values(ascending=True))


# In[16]:


#Above confirms all values are the same for all rows in both columns. 
#Using loc and slicing, create a new dataframe dropping both of these columns (all rows) 
tables = tables1_2.drop(tables1_2.loc[:, ['Z_CostContact', 'Z_Revenue']], axis=1)


# In[17]:


tables.head()


# In[18]:


#Verify new dataframe shape (note - still has 2240 rows but now has 27 columns - Z_CostContact and Z_Revenue have been dropped)
print(tables.shape) 


# In[19]:


#INCOME


# In[20]:


#Use sorting to look at min and max income values
print(tables['Income'].sort_values(ascending=False))


# In[21]:


#Define custom function to create reusable code - define Histogram plot, figure size, bin size, x and y axis labels and title.
def plot_hist(variable):
    plt.figure(figsize = (6,3))
    plt.hist(tables[variable], bins = 30)  
    plt.xlabel(variable)
    plt.ylabel("Frequency")
    plt.title("{} distribution".format(variable))
    plt.show()


# In[22]:


#Use custom funtion to plot Histogram to view distribution of values for different variables - in this case, Income
Inc = ["Income"]
for n in Inc:
    plot_hist(n)


# In[23]:


#Inspect Income distribution in a boxplot
sns.boxplot(x=tables["Income"], color="Blue")

plt.show()


# In[24]:


#Inspect Income values further
print(tables.Income.describe())


# In[25]:


#Another way to get Income mean - using mean() method
mean_income = tables["Income"].mean(skipna = True)
print("mean income:", mean_income)


# In[26]:


#Replace missing values in Income column with mean income
tables["Income"].fillna(52247.0, inplace = True)


# In[27]:


#Inspect tables info afer replacing missing values in Income column (note - can see that the Income column now has 2240 values and therefore has no missing values. It also has retained a data type of float).
print(tables.info())


# In[28]:


#Clarify that there is no longer any missing data in the merged table
print(tables.isnull().sum())


# In[29]:


#Calculate Income outliers using IQR
q1 = tables["Income"].quantile(0.25)
q3 = tables["Income"].quantile(0.75)
iqr = q3 - q1

print("Old shape:", tables.shape)
print("IQR:", iqr)

#Calculate upper and lower limits
upper = q3 + 1.5 * iqr
lower = q1 - 1.5 * iqr
print("Lower limit:", lower)
print("Upper limit:", upper)

#Using np.where, address incomes above upper limit and below lower limit: adjust the value of these incomes to be equal to the upper and lower limit values respectively
tables["Income"] = np.where(tables["Income"] > upper, upper, np.where(tables["Income"] < lower, lower, tables["Income"]))

#Show new shape (note - shows that the row numbers haven't changed and therefore outlier values have been adjusted)
print ("New shape:", tables.shape)

#Show new min and max values (note - no values lower than the lower limit therefore new min value hasn't changed)
New_max_value = tables["Income"].max()
New_min_value = tables["Income"].min()
print("New max income:", New_max_value)
print("New min income:", New_min_value)


# In[30]:


#Inspect Income distribution (including adjusted outlier values) in a boxplot 
sns.boxplot(x=tables["Income"], color="blue")

plt.show()


# In[31]:


#Use custom function previously created to inspect Income distribution in a Histogram after replacing outliers 
for n in Inc:
    plot_hist(n)


# In[32]:


#Rename some columns by creating new columns for this data (to enable clearer labelling of these columns on graphs)
tables["Young_Children"] = tables["Kidhome"]
tables["Teenagers"] = tables["Teenhome"]
tables["Wines"] = tables["MntWines"]
tables["Fruits"] = tables["MntFruits"]
tables["Meat_Products"] = tables["MntMeatProducts"]
tables["Fish_Products"] = tables["MntFishProducts"]
tables["Sweet_Products"] = tables["MntSweetProducts"]
tables['Gold_Products'] = tables["MntGoldProds"]


# In[33]:


tables.head()


# In[34]:


#Verify tables (note - still has 2240 rows but now has 35 column after 8 above added)
print(tables.shape)


# In[35]:


#Using loc and slicing, and a list, drop the original columns above from the dataframe, now that copies of these columns have been made 
tables = tables.drop(tables.loc[:, ["Kidhome", "Teenhome", "MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]], axis=1)


# In[36]:


tables.head()


# In[37]:


#Verify tables (note - still has 2240 rows but now has 27 column after 8 above removed)
print(tables.shape)


# In[38]:


#Add new column showing customer total spend for the last 2 years, obtained by adding the amount spent on wines, fruits,meat, fish, sweet products and gold.
tables["Tot_Spend"] = tables["Wines"]+ tables["Fruits"]+ tables["Meat_Products"]+ tables["Fish_Products"]+ tables["Sweet_Products"]+ tables["Gold_Products"]
print(tables["Tot_Spend"].head())


# In[39]:


#Use sorting to find min and max total spend
print(tables['Tot_Spend'].sort_values(ascending=True))


# In[40]:


#Add new column showing customer total number of purchases, obtained by adding deal purchases, web purchases, catalogue purchases and store purchases
tables['Tot_Purchases'] = tables['NumDealsPurchases'] + tables['NumWebPurchases'] + tables['NumCatalogPurchases'] + tables['NumStorePurchases']


# In[41]:


#Use sorting to find min and max total purchases
print(tables['Tot_Purchases'].sort_values(ascending=True))


# In[42]:


#Investigate income versus total spent
fig, ax = plt.subplots(figsize=(7,5))
fig.suptitle("Income Vs Total Spent")

sns.regplot(y="Income", x="Tot_Spend", data=tables, line_kws={"color": "red"})

plt.show()


# In[43]:


#Investigate income versus amount spent on different categories of purchases (wines, fruit, meat, fish, sweet products, gold)
fig, axes = plt.subplots(3, 2, sharex=True, figsize=(15,7))
fig.suptitle("Income Vs Amount Spent on Products by Category")

sns.regplot(y="Wines", x="Income", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Fruits", x="Income", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Meat_Products", x="Income", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Fish_Products", x="Income", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Sweet_Products", x="Income", data=tables, ax=axes[2,0], line_kws={"color": "red"})

sns.regplot(y="Gold_Products", x="Income", data=tables, ax=axes[2,1], line_kws={"color": "red"})

plt.show()


# In[44]:


#Investigate income versus total purchases (New Tot_Purchases column already created)
fig, ax = plt.subplots(figsize=(7,5))
fig.suptitle("Income Vs Total Purchases")

sns.regplot(x="Tot_Purchases", y="Income", data=tables, line_kws={"color": "red"})

plt.show()


# In[45]:


#Investigate income versus types of purchase (in store, online, catalogue, deals) in regplots
fig, axes = plt.subplots(2, 2, sharex=True, figsize=(15,7))
fig.suptitle("Income Vs Types of Purchases")

sns.regplot(x="NumWebPurchases", y="Income", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(x="NumDealsPurchases", y="Income", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(x="NumCatalogPurchases", y="Income", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(x="NumStorePurchases", y="Income", data=tables, ax=axes[1,1], line_kws={"color": "red"})

plt.show()


# In[46]:


#Investigate income versus types of purchase (in store, online, catalogue, deals) in regplots
fig, axes = plt.subplots(2, 2, sharex=True, figsize=(15,7))
fig.suptitle("Income Vs Types of Purchases")

sns.regplot(x="NumWebPurchases", y="Income", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(x="NumDealsPurchases", y="Income", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(x="NumCatalogPurchases", y="Income", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(x="NumStorePurchases", y="Income", data=tables, ax=axes[1,1], line_kws={"color": "red"})

plt.show()


# In[47]:


#EDUCATION


# In[48]:


#Inspect Education column using sorting and indexing
print("Total categories in Education column :")
ed = tables.pivot_table(index = ['Education'], aggfunc = 'size') 
ed = ed.reset_index()
ed.columns= ["Education", "Counts"]
ed = ed.sort_values("Counts", ascending = False)
print(ed)


# In[49]:


#Simplify education levels by combining into less groups using dictionaries
tables["Education_Level"]=tables["Education"].replace({"Basic":"Undergraduate","2n Cycle":"Undergraduate", 
                                                   "Graduation":"Graduate", "Master":"Postgraduate", "PhD":"Postgraduate"})
print(tables["Education_Level"].head())


# In[50]:


#Inspect new Education_Level column using sorting and indexing
print("Total categories in Education Level column :")
el = tables.pivot_table(index = ['Education_Level'], aggfunc = 'size') 
el = el.reset_index()
el.columns= ["Education_Level", "Counts"]
el = el.sort_values("Counts", ascending = False)
print(el)


# In[51]:


#Investigate Total Spent (new Tot_Spend column already created) by Education and Grouped Education using barplots (grouped education uses new column 'Education_Level' which combines basic and 2n cycle into 1 group 'undergraduate', and combines master ad PhD into another group ' postgraduate')
fig, axes = plt.subplots(1, 2, figsize=(15,5))
fig.suptitle("Education Vs Total Spent")

sns.barplot(x='Education', y='Tot_Spend', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[0]).set(title='Education')

sns.barplot(x='Education_Level', y='Tot_Spend', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[1]).set(title='Grouped Education')

plt.show()

#Using groupby,look at mean total spend by marital status, and mean total spend by relationship status

print(tables.groupby('Education')['Tot_Spend'].mean())
print(tables.groupby('Education_Level')['Tot_Spend'].mean())


# In[52]:


#Investigate amount spent on different categories by education
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Education Vs Amount Spent on Products by Category')

sns.barplot(y='Wines', x='Education', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[0,0])

sns.barplot(y='Fruits', x='Education', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[0,1])

sns.barplot(y='Meat_Products', x='Education', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[1,0])

sns.barplot(y='Fish_Products', x='Education', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[1,1])

sns.barplot(y='Sweet_Products', x='Education', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[2,0])

sns.barplot(y='Gold_Products', x='Education', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[2,1])

plt.show()


# In[53]:


#Investigate amount spent on different categories by Grouped Education Level
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Grouped Education Vs Amount Spent on Products by Category')

sns.barplot(y='Wines', x='Education_Level', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[0,0])

sns.barplot(y='Fruits', x='Education_Level', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[0,1])

sns.barplot(y='Meat_Products', x='Education_Level', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[1,0])

sns.barplot(y='Fish_Products', x='Education_Level', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[1,1])

sns.barplot(y='Sweet_Products', x='Education_Level', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[2,0])

sns.barplot(y='Gold_Products', x='Education_Level', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[2,1])

plt.show()


# In[54]:


#Investigate total purchases (new Tot_Purchases column already created) by Education and Grouped Education 
fig, axes = plt.subplots(1, 2, figsize=(15,5))
fig.suptitle("Education Vs Total Purchases")

sns.barplot(x='Education', y='Tot_Purchases', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[0]).set(title="Education")

sns.barplot(x='Education_Level', y='Tot_Purchases', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[1]).set(title="Grouped Education")

plt.show()

#Using groupby,look at mean total spend by marital status, and mean total spend by relationship status

print(tables.groupby('Education')['Tot_Purchases'].mean())
print(tables.groupby('Education_Level')['Tot_Purchases'].mean())


# In[55]:


#Investigate types of purchases by Education
fig, axes = plt.subplots(2, 2, figsize=(15,10))
fig.suptitle('Education Vs Types of Purchases')

sns.barplot(y='NumWebPurchases', x='Education', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[0,0])

sns.barplot(y='NumDealsPurchases', x='Education', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[0,1])

sns.barplot(y='NumCatalogPurchases', x='Education', order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], data=tables, ax=axes[1,0])

sns.barplot(y='NumStorePurchases', x='Education', order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], data=tables, ax=axes[1,1])


plt.show()


# In[56]:


#Investigate types of purchases by Grouped Education 
fig, axes = plt.subplots(2, 2, figsize=(15,10))
fig.suptitle('Grouped Education Vs Types of Purchases')

sns.barplot(y='NumWebPurchases', x='Education_Level', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[0,0])

sns.barplot(y='NumDealsPurchases', x='Education_Level', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[0,1])

sns.barplot(y='NumCatalogPurchases', x='Education_Level', order=['Undergraduate', 'Graduate', 'Postgraduate'], data=tables, ax=axes[1,0])

sns.barplot(y='NumStorePurchases', x='Education_Level', order=['Undergraduate', 'Graduate', 'Postgraduate'], data=tables, ax=axes[1,1])


plt.show()


# In[57]:


#Investigate the relationship between Income and Education using barplot (including list of data passed in for order)
fig, axes = plt.subplots(1, 2, figsize=(15,5))
fig.suptitle("Education Vs Income")

sns.barplot(x='Education', y='Income', data=tables, order=['Basic', '2n Cycle', 'Graduation', 'Master', 'PhD'], ax=axes[0]).set(title='Education')

sns.barplot(x='Education_Level', y='Income', data=tables, order=['Undergraduate', 'Graduate', 'Postgraduate'], ax=axes[1]).set(title='Grouped Education')

plt.show()

#Using groupby,look at mean Income grouped by Education

print(tables.groupby('Education')['Income'].mean())
print(tables.groupby('Education_Level')['Income'].mean())


# In[58]:


#Investigate new columns Tot_Spend and Tot_Purchases Versus Income, adding education as another variable
fig, axes = plt.subplots(1, 2, figsize=(15,5))
fig.suptitle('Income and Education Vs Total Spent and Total Purchases')

sns.scatterplot(x='Tot_Spend', y='Income', data=tables, hue="Education", ax=axes[0]).set(title="Total Spent")

sns.scatterplot(x='Tot_Purchases', y='Income', data=tables, hue="Education", ax=axes[1]).set(title="Total Purchases")

plt.show()


# In[59]:


#Revisit investigatation of new columns Tot_Spend and Tot_Purchases Versus Income, adding simplified education levels as another variable
#Also use dictionary to set hue palette
fig, axes = plt.subplots(1, 2, figsize=(20,5))
fig.suptitle('Income and Grouped Education Vs Total Spent and Total Purchases')
hue_colors = {"Undergraduate": "purple", "Graduate": "Orange", "Postgraduate": "green"}

sns.scatterplot(x='Tot_Spend', y='Income', data=tables, hue="Education_Level", palette=hue_colors, style="Education_Level", alpha=0.8, ax=axes[0]).set(title="Total Spent")

sns.scatterplot(x='Tot_Purchases', y='Income', data=tables, hue="Education_Level", palette=hue_colors, style="Education_Level", alpha=0.8, ax=axes[1]).set(title="Total Purchases")

plt.show()


# In[60]:


#AGE


# In[61]:


#Use sorting to find min and max year of birth
print(tables['Year_Birth'].sort_values(ascending=True))


# In[62]:


#Add new column showing customer age, obtained by subracting column Year_Birth from current year
tables["Age"] = 2021-tables["Year_Birth"]
print(tables["Age"].head())


# In[63]:


#Use custom fuction previously created to inspect customer age distribution in a Histogram
Age = ["Age"]
for n in Age:
    plot_hist(n)


# In[64]:


#Inspect Age distribution in a boxplot 
sns.boxplot(x=tables["Age"], color="blue")

plt.show()


# In[65]:


#Use sorting to show min and max age
print(tables['Age'].sort_values(ascending=True))


# In[66]:


#Inspect Age column stats further
print(tables.Age.describe())


# In[67]:


#use looping to find out how many people are older than 100 - mark values in Age column >= 100 as 'Fail'
result = []
for value in tables["Age"]:
    if value >= 100:
        result.append("Fail")
    else: 
        result.append("Pass")
        
print(result)


# In[68]:


#Find out how many 'Fail' values there are (how many values are >=100)
fail_count = result.count('Fail')
print('Number of Fails (ie people >100 years old) :', fail_count)


# In[69]:


#Use numpy - another way to find out how many people are >100, and also determine what those values are: convert Age column in dataframe to np array and use np.logical_not to find ages not less than 100
age_array = np.array(tables["Age"])
print("Age values of people >100 years old:", age_array[np.logical_not(age_array <100)])


# In[70]:


#Can reasonably assume that these age values are incorrect - will substitute them with mean age value.
#Replace Age values >100 with mean age value of 52
s = tables["Age"]
tables["Age"].where(s < 100, other = 52, inplace=True)
print(tables["Age"].describe())


# In[71]:


#use looping to find out how many people are now older than 100 post adjustment - mark values in Age column >= 100 as 'Fail'
result2 = []
for value in tables["Age"]:
    if value >= 100:
        result2.append("Fail")
    else: 
        result2.append("Pass")
        
print(result2)


# In[72]:


#Find out how many 'Fail' values there are post-replacement of outliers (how many values are >=100)
fail_count2 = result2.count('Fail')
print('Number of Fails (ie people >100 years old) :', fail_count2)


# In[73]:


#Use iterrows to display which customers have a year of birth >100 years ago and now have an age of 52 (customer ID included)
for index, row in tables.iterrows():
    print("ID:", row ["ID"], ", Birth Year older than 1921:", row ["Year_Birth"] < 1921, ", Age 52:", row ["Age"] == 52)


# In[74]:


#Using numpy arrays and np.logical_not(), show new adjusted age values of people born  before 1921 (ie who are >100 years old)
age_array2 = np.array(tables["Age"])
birth_year = np.array(tables["Year_Birth"])
print("New age values of people >100 years old:", age_array2[np.logical_not(birth_year > 1921)])


# In[75]:


#Use custom function previously defined to inspect Age distribution in a Histogram after replacing outliers 
for n in Age:
    plot_hist(n)


# In[76]:


#Inspect adjusted Age distribution in a boxplot after replacing outliers
sns.boxplot(x=tables["Age"], color="blue")

plt.show()


# In[77]:


#Look at the relationship between customer age and income using a seaborn regplot for linear regression (note that this shows that the older the customer, the more they tend to earn)
fig, ax = plt.subplots(figsize=(7,5))
fig.suptitle("Age Vs Income")

sns.regplot(y='Income', x='Age', data=tables, line_kws={"color": "red"})

plt.show()


# In[78]:


#Investigate relationship between customer age and total purchases using regplot
fig, ax = plt.subplots(figsize=(7,5))
fig.suptitle("Age Vs Total Purchases")

sns.regplot(y="Age", x="Tot_Purchases", data=tables, line_kws={"color": "red"})

plt.show()


# In[79]:


#Investigate age versus types of purchase (in store, online, catalogue, deals) in regplots
fig, axes = plt.subplots(2, 2, sharex=True, figsize=(15,7))
fig.suptitle("Age Vs Types of Purchases")

sns.regplot(x="NumWebPurchases", y="Age", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(x="NumDealsPurchases", y="Age", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(x="NumCatalogPurchases", y="Age", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(x="NumStorePurchases", y="Age", data=tables, ax=axes[1,1], line_kws={"color": "red"})

plt.show()


# In[80]:


#Investigate age versus total spent in regplot
fig, ax = plt.subplots(figsize=(7,5))
fig.suptitle("Age Vs Total Spent")

sns.regplot(y="Tot_Spend", x="Age", data=tables, line_kws={"color": "red"})

plt.show()


# In[81]:


#Investigate age versus amount spent on different categories of purchases (wines, fruit, meat, fish, sweet products, gold) in regplots
fig, axes = plt.subplots(3, 2, sharex=True, figsize=(15,7))
fig.suptitle("Age Vs Amount Spent on Products by Category")

sns.regplot(y="Wines", x="Age", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Fruits", x="Age", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Meat_Products", x="Age", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Fish_Products", x="Age", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Sweet_Products", x="Age", data=tables, ax=axes[2,0], line_kws={"color": "red"})

sns.regplot(y="Gold_Products", x="Age", data=tables, ax=axes[2,1], line_kws={"color": "red"})

plt.show()


# In[82]:


#MARITAL STATUS


# In[83]:


#Inspect number and names of categories for marital status
print(tables["Marital_Status"].value_counts())


# In[84]:


#Create a new column, Relationship Status - reduce the 8 categories in Marital Status to 2 categories using dictionary
tables["Relationship_Status"]=tables["Marital_Status"].replace({"Married":"In a relationship", "Together":"In a relationship",
                                                    "Absurd":"Single", "Widow":"Single", "YOLO":"Single", 
                                                    "Divorced":"Single", "Single":"Single", "Alone":"Single"})
print(tables["Relationship_Status"].head())


# In[85]:


#Inspect new Relationship_Status column using sorting and indexing
print("Total categories in Relationship_Status column :")
rs = tables.pivot_table(index = ['Relationship_Status'], aggfunc = 'size') 
rs = rs.reset_index()
rs.columns= ["Relationship_Status", "Counts"]
rs = rs.sort_values("Counts", ascending = False)
print(rs)


# In[86]:


#Using iterrows, display customer marital Status and what it was converted to in the new relationship Status column. Customer ID also included
for index, row in tables.iterrows():
    print(row ["ID"], ":", row ["Marital_Status"], "converted to", row ["Relationship_Status"])


# In[87]:


#In existing Marital Status Column, replace Alone, Absurd and YOLO with Single using lists (these represent only 7 customers and would be better grouped with Single)
tables["Marital_Status"] = tables["Marital_Status"].replace(['Alone','Absurd','YOLO'],['Single','Single','Single'])
print(tables["Marital_Status"].value_counts())


# In[88]:


#Investigate Total Spent (new column already created) by Marital Status, and by Relationship Status using barplots
fig, axes = plt.subplots(1, 2, figsize=(15,5))
fig.suptitle("Marital Status and Relationship Status Vs Total Spent")

sns.barplot(x='Marital_Status', y='Tot_Spend', data=tables, ax=axes[0]).set(title="Marital Status")

sns.barplot(x='Relationship_Status', y='Tot_Spend', data=tables, ax=axes[1]).set(title="Relationship Status")

plt.show()

#Using groupby,look at mean total spend by marital status, and mean total spend by relationship status

print(tables.groupby('Marital_Status')['Tot_Spend'].mean())
print(tables.groupby('Relationship_Status')['Tot_Spend'].mean())


# In[89]:


#Investigate amount spent on different categories by marital status
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Marital Status Vs Amount Spent on Products by Category')

sns.barplot(y='Wines', x='Marital_Status', data=tables, ax=axes[0,0])

sns.barplot(y='Fruits', x='Marital_Status', data=tables, ax=axes[0,1])

sns.barplot(y='Meat_Products', x='Marital_Status', data=tables, ax=axes[1,0])

sns.barplot(y='Fish_Products', x='Marital_Status', data=tables, ax=axes[1,1])

sns.barplot(y='Sweet_Products', x='Marital_Status', data=tables, ax=axes[2,0])

sns.barplot(y='Gold_Products', x='Marital_Status', data=tables, ax=axes[2,1])

plt.show()


# In[90]:


#Widows seem to spend more money in total and across each category - perhaps this is due to higher income - Look at income versus marital status
fig, axes = plt.subplots(1,2, figsize=(15,5))
fig.suptitle('Income by Marital Status and Relationship Status')

sns.barplot(x='Marital_Status', y='Income', data=tables, ax=axes[0]).set(title="Marital Status")

sns.barplot(x='Relationship_Status', y='Income', data=tables, ax=axes[1]).set(title="Relationship Status")

plt.show()

#Using groupby,look at mean income by marital status

print(tables.groupby('Marital_Status')['Income'].mean())
print(tables.groupby('Relationship_Status')['Income'].mean())


# In[91]:


#Investigate amount spent on different categories by relationship status
fig, axes = plt.subplots(3, 2, sharex=True, figsize=(15,10))
fig.suptitle('Relationship Status Vs Amount Spent on Products by Category')

sns.barplot(y='Wines', x='Relationship_Status', data=tables, ax=axes[0,0])

sns.barplot(y='Fruits', x='Relationship_Status', data=tables, ax=axes[0,1])

sns.barplot(y='Meat_Products', x='Relationship_Status', data=tables, ax=axes[1,0])

sns.barplot(y='Fish_Products', x='Relationship_Status', data=tables, ax=axes[1,1])

sns.barplot(y='Sweet_Products', x='Relationship_Status', data=tables, ax=axes[2,0])

sns.barplot(y='Gold_Products', x='Relationship_Status', data=tables, ax=axes[2,1])

plt.show()


# In[92]:


#Investigate total purchases by marital status and relationship status (new 'Tot_Purchases' column already created)
fig, axes = plt.subplots(1, 2, figsize=(15,5))
fig.suptitle('Marital Status and Relationship Status Vs Total Purchases')

sns.barplot(x='Marital_Status', y='Tot_Purchases', data=tables, ax=axes[0]).set(title="Marital Status")

sns.barplot(x='Relationship_Status', y='Tot_Purchases', data=tables, ax=axes[1]).set(title="Relationship Status")

plt.show()

#Using .groupby,look at mean total spend by marital status, and mean total spend by relationship status

print(tables.groupby('Marital_Status')['Tot_Purchases'].mean())
print(tables.groupby('Relationship_Status')['Tot_Purchases'].mean())


# In[93]:


#Investigate types of purchase by marital status (in store, online, catalogue, deals) 
fig, axes = plt.subplots(2, 2, figsize=(15,10))
fig.suptitle('Marital Status Vs Types of Purchases')

sns.barplot(y='NumWebPurchases', x='Marital_Status', data=tables, ax=axes[0,0])

sns.barplot(y='NumDealsPurchases', x='Marital_Status', data=tables, ax=axes[0,1])

sns.barplot(y='NumCatalogPurchases', x='Marital_Status', data=tables, ax=axes[1,0])

sns.barplot(y='NumStorePurchases', x='Marital_Status', data=tables, ax=axes[1,1])


plt.show()


# In[94]:


#Investigate types of purchase by relationship status
fig, axes = plt.subplots(2, 2, sharex=True, figsize=(15,10))
fig.suptitle('Relationship Status Vs Types of Purchases')

sns.barplot(y='NumWebPurchases', x='Relationship_Status', data=tables, ax=axes[0,0])

sns.barplot(y='NumDealsPurchases', x='Relationship_Status', data=tables, ax=axes[0,1])

sns.barplot(y='NumCatalogPurchases', x='Relationship_Status', data=tables, ax=axes[1,0])

sns.barplot(y='NumStorePurchases', x='Relationship_Status', data=tables, ax=axes[1,1])

plt.show()


# In[95]:


#Investigate total spend and total purchases Versus income, adding customer relationship status as another variable
fig, axes = plt.subplots(1, 2, figsize=(20,5))
fig.suptitle('Income and Relationship Status Vs Total Spent and Total Purchases')

sns.scatterplot(x='Tot_Spend', y='Income', data=tables, hue='Relationship_Status', style='Relationship_Status', ax=axes[0])

sns.scatterplot(x='Tot_Purchases', y='Income', data=tables, hue='Relationship_Status', style='Relationship_Status', ax=axes[1])

plt.show()


# In[96]:


#Number AND CATEGORIES OF PEOPLE IN CUSTOMER HOUSE


# In[97]:


#Add new column showing total number of adults in the house, obtained by replacing the category statuses with 2 (people) and 1(person) respectively. (Will assume for the purposes of analysis that the status of 'together' refers to people who live together)
tables["Tot_Adults"] = tables["Marital_Status"].replace({"Married": 2, "Together": 2, "Single": 1, "Divorced": 1, "Widow":1})
print(tables["Tot_Adults"].value_counts())


# In[98]:


#Add new column showing total number of non-adults in the house, obtained by adding young children and teenager columns
tables["Tot_Children"] = tables["Young_Children"]+ tables["Teenagers"]
print(tables["Tot_Children"].value_counts())


# In[99]:


#Add new column showing total number of people in the house, obtained by adding Tot_Adults and Tot_Children columns
tables["Tot_PeopleinHouse"] = tables["Tot_Adults"]+ tables["Tot_Children"]
print(tables["Tot_PeopleinHouse"].value_counts())


# In[100]:


#View total people in the house in a countplot
sns.countplot(x="Tot_PeopleinHouse", data=tables).set(title='Number of People in House')

plt.show()


# In[101]:


#View breakdown of adults and children in household
fig, axes = plt.subplots(2, 2, figsize=(15,10))
fig.suptitle("Breakdown of People in Household")

sns.countplot(x='Tot_Adults', data=tables, ax=axes[0,0])

sns.countplot(x='Tot_Children', data=tables, ax=axes[0,1])

sns.countplot(x='Young_Children', data=tables, ax=axes[1,0])

sns.countplot(x='Teenagers', data=tables, ax=axes[1,1])

plt.show()


# In[102]:


#Compare categories of people in the house with total spend
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Total Spent")
fig.delaxes(axes[2,1])

sns.regplot(y="Tot_Spend", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Tot_Spend", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Tot_Spend", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Tot_Spend", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Tot_Spend", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[103]:


#Compare categories of people in the house with product bought: WINES
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Amount Spent on Wine")
fig.delaxes(axes[2,1])

sns.regplot(y="Wines", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Wines", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Wines", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Wines", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Wines", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[104]:


#Compare categories of people in the house with product bought: FRUITS
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Amount Spent on Fruits")
fig.delaxes(axes[2,1])

sns.regplot(y="Fruits", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Fruits", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Fruits", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Fruits", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Fruits", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[105]:


#Compare categories of people in the house with product bought: MEAT PRODUCTS
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Amount Spent on Meat Products")
fig.delaxes(axes[2,1])

sns.regplot(y="Meat_Products", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Meat_Products", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Meat_Products", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Meat_Products", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Meat_Products", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[106]:


#Compare categories of people in the house with product bought: FISH PRODUCTS
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Amount Spent on Fish Products")
fig.delaxes(axes[2,1])

sns.regplot(y="Fish_Products", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Fish_Products", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Fish_Products", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Fish_Products", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Fish_Products", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[107]:


#Compare categories of people in the house with product bought: SWEET PRODUCTS
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Amount Spent on Sweet Products")
fig.delaxes(axes[2,1])

sns.regplot(y="Sweet_Products", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Sweet_Products", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Sweet_Products", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Sweet_Products", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Sweet_Products", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[108]:


#Compare categories of people in the house with product bought: GOLD PRODUCTS
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Amount Spent on Gold Products")
fig.delaxes(axes[2,1])

sns.regplot(y="Gold_Products", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Gold_Products", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Gold_Products", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Gold_Products", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Gold_Products", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[109]:


#Compare categories of people in the house with total purchases
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Total Purchases")
fig.delaxes(axes[2,1])

sns.regplot(y="Tot_Purchases", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="Tot_Purchases", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="Tot_Purchases", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="Tot_Purchases", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="Tot_Purchases", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[110]:


#Compare categories of people in the house with web purchases
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Web Purchases")
fig.delaxes(axes[2,1])

sns.regplot(y="NumWebPurchases", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="NumWebPurchases", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="NumWebPurchases", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="NumWebPurchases", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="NumWebPurchases", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[111]:


#Compare categories of people in the house with deals purchases
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Deals Purchases")
fig.delaxes(axes[2,1])

sns.regplot(y="NumDealsPurchases", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="NumDealsPurchases", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="NumDealsPurchases", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="NumDealsPurchases", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="NumDealsPurchases", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[112]:


#Compare categories of people in the house with catalog purchases
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Catalog Purchases")
fig.delaxes(axes[2,1])

sns.regplot(y="NumCatalogPurchases", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="NumCatalogPurchases", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="NumCatalogPurchases", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="NumCatalogPurchases", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="NumCatalogPurchases", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[113]:


#Compare categories of people in the house with store purchases
fig, axes = plt.subplots(3, 2, sharey=True, figsize=(15,10))
fig.suptitle("Categories of People in the House Vs Store Purchases")
fig.delaxes(axes[2,1])

sns.regplot(y="NumStorePurchases", x="Tot_PeopleinHouse", data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y="NumStorePurchases", x="Tot_Adults", data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y="NumStorePurchases", x="Tot_Children", data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(y="NumStorePurchases", x="Young_Children", data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(y="NumStorePurchases", x="Teenagers", data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[114]:


#Create new column Has Child to indicate whether the customer has a child or not
tables['Has_Child'] = np.where(tables['Tot_Children'] >0, 'Yes', 'No')
print(tables['Has_Child'].value_counts())


# In[115]:


#Look at the income of customers with and without children
sns.barplot(x='Has_Child', y='Income', data=tables).set(title='Income Vs Children')

plt.show()

#Using groupby,look at mean Income grouped by whether the customer has children or not

print(tables.groupby('Has_Child')['Income'].mean())


# In[116]:


#Investigate total spend and total purchases Versus income, adding whether customer has children as another variable
fig, axes = plt.subplots(1, 2, figsize=(20,5))
fig.suptitle('Income and Children Vs Total Spent and Total Purchases')

sns.scatterplot(x='Tot_Spend', y='Income', data=tables, hue='Has_Child', style='Has_Child', ax=axes[0])

sns.scatterplot(x='Tot_Purchases', y='Income', data=tables, hue='Has_Child', style='Has_Child', ax=axes[1])

plt.show()


# In[117]:


#Removing income, look at total spend Vs total purchases, with Has_Child 
fig, axes = plt.subplots(figsize=(7,5))

sns.scatterplot(x='Tot_Purchases', y='Tot_Spend', data=tables, hue='Has_Child', style='Has_Child').set(title="Has Child Vs Total Spent")

plt.show()


# In[118]:


#Look at total spend Vs total purchases by Has_Child (in separate graphs using relplot)
sns.relplot(x='Tot_Purchases', y='Tot_Spend', data=tables, kind='scatter', col='Has_Child')

plt.show()


# In[119]:


#Show income versus total spend by Has_Child
sns.relplot(x='Income', y='Tot_Spend', data=tables, kind='scatter', col='Has_Child')

plt.show()


# In[120]:


#PROMOTION CAMPAIGNS


# In[121]:


#Inspect columns relating to Promotion Campaigns by grouping them together in a list and plotting on a barplot to see how many customers accepted the offer on each campaign 
AcceptedCmp = tables[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']]
AcceptedCmp = AcceptedCmp.apply(pd.DataFrame.sum)

plt.figure(figsize=(10,5))
plt.title('Number of Customers who Accepted a Promotional Offer on each Campaign Attempt')
plt.xlabel('Campaign Number')

sns.barplot(x=AcceptedCmp.index, y=AcceptedCmp)

plt.show()


# In[122]:


#Inspect relationship between customer total spend and whether they availed of a promotion/deal campaign
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Acceptance of Promotion Campaign Vs Total Spent')
fig.delaxes(axes[2,1])

sns.regplot(x='AcceptedCmp1', y='Tot_Spend', data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp2', y='Tot_Spend', data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp3', y='Tot_Spend', data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp4', y='Tot_Spend', data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp5', y='Tot_Spend', data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[123]:


#Inspect relationship between total npurchases and whether the customer availed of a promotion/deal campaign
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Acceptance of Promotion Campaign Vs Total Purchases')
fig.delaxes(axes[2,1])

sns.regplot(x='AcceptedCmp1', y='Tot_Purchases', data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp2', y='Tot_Purchases', data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp3', y='Tot_Purchases', data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp4', y='Tot_Purchases', data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp5', y='Tot_Purchases', data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[124]:


#Inspect relationship between customer income and whether they availed of a promotion/deal campaign
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Acceptance of Promotion Campaign Vs Income')
fig.delaxes(axes[2,1])

sns.regplot(x='AcceptedCmp1', y='Income', data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp2', y='Income', data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp3', y='Income', data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp4', y='Income', data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp5', y='Income', data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[125]:


#Inspect relationship between total number of people in the house and whether the customer availed of a promotion/deal campaign
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Acceptance of Promotion Campaign Vs Number of People in House')
fig.delaxes(axes[2,1])

sns.regplot(x='AcceptedCmp1', y='Tot_PeopleinHouse', data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp2', y='Tot_PeopleinHouse', data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp3', y='Tot_PeopleinHouse', data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp4', y='Tot_PeopleinHouse', data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp5', y='Tot_PeopleinHouse', data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[126]:


#Inspect relationship between age and whether the customer availed of a promotion/deal campaign
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Acceptance of Promotion Campaign Vs Age')
fig.delaxes(axes[2,1])

sns.regplot(x='AcceptedCmp1', y='Age', data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp2', y='Age', data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp3', y='Age', data=tables, ax=axes[1,0], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp4', y='Age', data=tables, ax=axes[1,1], line_kws={"color": "red"})

sns.regplot(x='AcceptedCmp5', y='Age', data=tables, ax=axes[2,0], line_kws={"color": "red"})

plt.show()


# In[127]:


#Inspect relationship between marital status and whether the customer availed of a promotion/deal campaign
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Acceptance of Promotion Campaign Vs Marital Status')
fig.delaxes(axes[2,1])

sns.barplot(y='AcceptedCmp1', x='Marital_Status', data=tables, ax=axes[0,0])

sns.barplot(y='AcceptedCmp2', x='Marital_Status', data=tables, ax=axes[0,1])

sns.barplot(y='AcceptedCmp3', x='Marital_Status', data=tables, ax=axes[1,0])

sns.barplot(y='AcceptedCmp4', x='Marital_Status', data=tables, ax=axes[1,1])

sns.barplot(y='AcceptedCmp5', x='Marital_Status', data=tables, ax=axes[2,0])

plt.show()


# In[128]:


#Inspect relationship between relationship status and whether the customer availed of a promotion/deal campaign
fig, axes = plt.subplots(3, 2, figsize=(15,10))
fig.suptitle('Acceptance of Promotion Campaign Vs Relationship Status')
fig.delaxes(axes[2,1])

sns.barplot(y='AcceptedCmp1', x='Relationship_Status', data=tables, ax=axes[0,0])

sns.barplot(y='AcceptedCmp2', x='Relationship_Status', data=tables, ax=axes[0,1])

sns.barplot(y='AcceptedCmp3', x='Relationship_Status', data=tables, ax=axes[1,0])

sns.barplot(y='AcceptedCmp4', x='Relationship_Status', data=tables, ax=axes[1,1])

sns.barplot(y='AcceptedCmp5', x='Relationship_Status', data=tables, ax=axes[2,0])

plt.show()


# In[129]:


#Look at relationship between number of deals and in store purchases, web purchases, and catalog purchases
fig, axes = plt.subplots(2, 2, figsize=(15,10))
fig.suptitle('Number of Deals Vs Type of Purchase')
fig.delaxes(axes[1,1])

sns.regplot(y='NumStorePurchases', x='NumDealsPurchases', data=tables, ax=axes[0,0], line_kws={"color": "red"})

sns.regplot(y='NumWebPurchases', x='NumDealsPurchases', data=tables, ax=axes[0,1], line_kws={"color": "red"})

sns.regplot(y='NumCatalogPurchases', x='NumDealsPurchases', data=tables, ax=axes[1,0], line_kws={"color": "red"})

plt.show()


# In[130]:


#Look at the correlation between deals purchases and web, store and catalog purchases.
#(Note as per regplots, there is a higher correlation between deals purchases and web purchases (as well as web visits), than deals purchases and in store or catalog purchases)
tables[['NumWebPurchases', 'NumDealsPurchases','NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth', 'Response']].corr()


# In[131]:


#WEB VISITS


# In[132]:


#Investigate monthly number of web visits by total spend and total purchases
fig, axes = plt.subplots(1,2, figsize=(15,5))
fig.suptitle("Number of Web Visits per Month by Total Spent and Total Purchases")

sns.regplot(x='NumWebVisitsMonth', y='Tot_Spend', data=tables, ax=axes[0], line_kws={"color": "red"}).set(title="Total Spend")

sns.regplot(x='NumWebVisitsMonth', y='Tot_Purchases', data=tables, ax=axes[1], line_kws={"color": "red"}).set(title="Total Purchases")

plt.show()


# In[133]:


#Investigate monthly number of web visits by income
fig, axes = plt.subplots(figsize=(7,5))
fig.suptitle("Number of Web Visits per Month by Income")

sns.regplot(x='NumWebVisitsMonth', y='Income', data=tables, line_kws={"color": "red"})

plt.show()


# In[134]:


#Investigate monthly number of web visits by education
fig, axes = plt.subplots(1, 2, figsize=(15,5))
fig.suptitle("Number of Web Visits per Month by Education and Grouped Education")

sns.barplot(y='NumWebVisitsMonth', x='Education', data=tables, ax=axes[0]).set(title="Education")

sns.barplot(y='NumWebVisitsMonth', x='Education_Level', data=tables, ax=axes[1]).set (title="Grouped Education")

plt.show()


# In[135]:


#Investigate monthly number of web visits by age
fig, axes = plt.subplots(figsize=(7,5))
fig.suptitle("Number of Web Visits per Month by Age")

sns.regplot(x='NumWebVisitsMonth', y='Age', data=tables, line_kws={"color": "red"})

plt.show()


# In[136]:


#Investigate monthly number of web visits by customer marital status
fig, axes = plt.subplots(1, 2, figsize=(15,5))
fig.suptitle("Number of Web Visits per Month by Marital Status and Relationship Status")

sns.barplot(y='NumWebVisitsMonth', x='Marital_Status', data=tables, ax=axes[0]).set(title="Marital Status")

sns.barplot(y='NumWebVisitsMonth', x='Relationship_Status', data=tables, ax=axes[1]).set(title="Relationship Status")

plt.show()


# In[137]:


#Investigate monthly number of web visits of people with teenagers and young children respectively
fig, axes = plt.subplots(1, 2, figsize=(15,5))
fig.suptitle("Number of Web Visits per Month by Teenagers or Young Children in the House")

sns.regplot(x='NumWebVisitsMonth', y='Young_Children', data=tables, ax=axes[0], line_kws={"color": "red"})

sns.regplot(x='NumWebVisitsMonth', y='Teenagers', data=tables, ax=axes[1], line_kws={"color": "red"})

plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




