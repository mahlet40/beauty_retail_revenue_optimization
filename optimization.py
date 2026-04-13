import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. DATA ACQUISITION & CLEANING
# ==========================================
# Defining headers manually to avoid 'KeyError' and handle missing headers
column_names = [
    'Product_Name', 'Brand', 'Category', 'Usage_Frequency', 'Price_USD', 
    'Rating', 'Number_of_Reviews', 'Product_Size', 'Skin_Type', 
    'Gender_Target', 'Packaging_Type', 'Main_Ingredient', 'Cruelty_Free', 'Country_of_Origin'
]

# Loading with 'utf-8-sig' to handle invisible Excel formatting
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv', 
                 names=column_names, header=0, encoding='utf-8-sig')

# Data Prep: Remove spaces and drop empty rows for higher accuracy
df.columns = df.columns.str.strip()
df = df.dropna()

# ==========================================
# 2. ADVANCED ANALYTICAL TECHNIQUES
# ==========================================

# TECHNIQUE 1: Derived Metrics (Ratios)
# 'Revenue_Efficiency' tells us which products make the most money per unit of popularity
df['Estimated_Revenue'] = df['Price_USD'] * df['Number_of_Reviews']
df['Rev_Per_Review'] = df['Estimated_Revenue'] / df['Number_of_Reviews']

# TECHNIQUE 2: Percentile Analysis (Premium Segmentation)
# We calculate the 80th percentile to identify "High-Value" price points
premium_price_threshold = df['Price_USD'].quantile(0.80)

# TECHNIQUE 3: Cohort Analysis (Group Performance)
# Analyzing how average ratings differ across Skin Type cohorts
skin_cohorts = df.groupby('Skin_Type')['Rating'].mean().sort_values(ascending=False)

# TECHNIQUE 4: Cross-Tabulation (Interaction Mapping)
# This finds patterns between Skin Type and Category for bundling opportunities
bundle_map = pd.crosstab(df['Skin_Type'], df['Category'])

# ==========================================
# 3. REVENUE OPTIMIZATION STRATEGY
# ==========================================

# A. FOCUS: Identify High-Revenue Winners (Rating > 4.0)
winners = df[df['Rating'] > 4.0].nlargest(10, 'Estimated_Revenue')

# B. DECREASE: Identify Low-Quality Risks (Rating < 2.0)
risks = df[df['Rating'] < 2.0]

# C. CROSS-SELL: Bundle logic based on 'Main_Ingredient'
def recommend_bundle(ingredient):
    related = df[df['Main_Ingredient'] == ingredient].head(3)
    return related['Product_Name'].tolist()

# ==========================================
# 4. SIMPLIFIED VISUALIZATION
# ==========================================
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# Bar chart showing Revenue by Category
avg_rev = df.groupby('Category')['Estimated_Revenue'].sum().sort_values(ascending=False)
sns.barplot(x=avg_rev.values, y=avg_rev.index, palette="mako")

# Adding the 'Optimization Line' (Average Revenue)
plt.axvline(avg_rev.mean(), color='red', linestyle='--', label='Average Category Revenue')

plt.title('Retail Optimization: Revenue Distribution by Category', fontsize=14)
plt.xlabel('Total Estimated Revenue (USD)')
plt.legend()
plt.tight_layout()

# Save image for report
plt.savefig('beauty_optimization_final.png')

# ==========================================
# 5. AUTOMATED BUSINESS INSIGHTS
# ==========================================
print("\n" + "="*50)
print("     RETAIL REVENUE OPTIMIZATION SUMMARY")
print("="*50)
print(f"1. ANALYTICAL REACH: Analysis performed on {len(df)} beauty products.")
print(f"2. PREMIUM SEGMENT: Products priced above ${premium_price_threshold:.2f} are 'Premium'.")
print(f"3. TOP WINNER: {winners['Product_Name'].iloc[0]} (Brand: {winners['Brand'].iloc[0]})")
print(f"4. RISK ALERT: Found {len(risks)} items with low ratings needing optimization.")
print(f"5. BUNDLE IDEA: For 'Aloe Vera' fans, cross-sell: {recommend_bundle('Aloe Vera')}")
print("="*50)
print("ACTION: Closing chart window will finalize the process.")
plt.show()