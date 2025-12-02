import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
from datetime import datetime

# Set style
sns.set(style="whitegrid")

def load_and_clean_data(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # 1. Remove duplicates
    initial_len = len(df)
    df.drop_duplicates(inplace=True)
    print(f"Removed {initial_len - len(df)} duplicate rows.")
    
    # 2. Handle missing values
    df.dropna(subset=['Order Amount', 'Customer ID'], inplace=True)
    
    # 3. Filter invalid amounts
    df = df[df['Order Amount'] > 0]
    
    # Convert dates
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Signup Date'] = pd.to_datetime(df['Signup Date'])
    
    return df

def calculate_metrics(df):
    print("\n--- Customer Metrics ---")
    
    # Active Customers
    active_customers = df['Customer ID'].nunique()
    
    # Buying Frequency
    buying_freq = len(df) / active_customers
    
    # Revenue Contribution
    total_revenue = df['Order Amount'].sum()
    
    # Retention (Customers with > 1 order)
    order_counts = df.groupby('Customer ID').size()
    retained_customers = order_counts[order_counts > 1].count()
    retention_rate = (retained_customers / active_customers) * 100
    
    # --- New Metrics ---
    
    # Churn Rate (Inactive > 180 days)
    last_order_date = df.groupby('Customer ID')['Order Date'].max()
    # Assume "current date" is the max date in the dataset + 1 day
    current_date = df['Order Date'].max()
    days_inactive = (current_date - last_order_date).dt.days
    churned_customers = days_inactive[days_inactive > 180].count()
    churn_rate = (churned_customers / active_customers) * 100
    print(f"Churn Rate (Inactive > 180 days): {churn_rate:.2f}%")
    
    # Customer Segmentation (RFM-like: based on Revenue)
    customer_revenue = df.groupby('Customer ID')['Order Amount'].sum()
    # Simple segmentation: Top 20% = High Value, Next 30% = Medium, Bottom 50% = Low
    high_cutoff = customer_revenue.quantile(0.8)
    med_cutoff = customer_revenue.quantile(0.5)
    
    high_value_count = customer_revenue[customer_revenue >= high_cutoff].count()
    med_value_count = customer_revenue[(customer_revenue < high_cutoff) & (customer_revenue >= med_cutoff)].count()
    low_value_count = customer_revenue[customer_revenue < med_cutoff].count()
    
    print(f"High Value Customers (> ${high_cutoff:.2f}): {high_value_count}")
    
    metrics = {
        'Active Customers': int(active_customers),
        'Buying Frequency': float(buying_freq),
        'Total Revenue': float(total_revenue),
        'Retention Rate': float(retention_rate),
        'Churn Rate': float(churn_rate),
        'High Value Cutoff': float(high_cutoff),
        'High Value Count': int(high_value_count),
        'Medium Value Count': int(med_value_count),
        'Low Value Count': int(low_value_count)
    }
    
    with open('customer_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    return metrics

def generate_visualizations(df):
    print("\nGenerating Visualizations...")
    
    # 1. Revenue over time (Monthly)
    df['Month'] = df['Order Date'].dt.to_period('M')
    monthly_revenue = df.groupby('Month')['Order Amount'].sum().reset_index()
    monthly_revenue['Month'] = monthly_revenue['Month'].astype(str)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_revenue, x='Month', y='Order Amount', marker='o')
    plt.xticks(rotation=45)
    plt.title('Monthly Revenue Trend')
    plt.tight_layout()
    plt.savefig('viz_revenue_over_time.png')
    plt.close()
    
    # 2. Top Product Categories
    plt.figure(figsize=(10, 6))
    category_revenue = df.groupby('Category')['Order Amount'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=category_revenue, x='Category', y='Order Amount')
    plt.title('Revenue by Product Category')
    plt.tight_layout()
    plt.savefig('viz_category_revenue.png')
    plt.close()
    
    # 3. Order Amount Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Order Amount'], bins=50, kde=True)
    plt.title('Order Amount Distribution')
    plt.tight_layout()
    plt.savefig('viz_order_distribution.png')
    plt.close()
    
    # --- New Visualizations ---
    
    # 4. Sales by Day of Week
    df['DayOfWeek'] = df['Order Date'].dt.day_name()
    # Order days correctly
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = df['DayOfWeek'].value_counts().reindex(days_order).reset_index()
    day_counts.columns = ['Day', 'Orders']
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=day_counts, x='Day', y='Orders', palette='viridis')
    plt.title('Orders by Day of Week')
    plt.tight_layout()
    plt.savefig('viz_day_of_week.png')
    plt.close()
    
    # 5. Customer Segments (Pie Chart)
    # Re-calculate for viz
    customer_revenue = df.groupby('Customer ID')['Order Amount'].sum()
    high_cutoff = customer_revenue.quantile(0.8)
    med_cutoff = customer_revenue.quantile(0.5)
    
    high = customer_revenue[customer_revenue >= high_cutoff].count()
    med = customer_revenue[(customer_revenue < high_cutoff) & (customer_revenue >= med_cutoff)].count()
    low = customer_revenue[customer_revenue < med_cutoff].count()
    
    plt.figure(figsize=(8, 8))
    plt.pie([high, med, low], labels=['High Value', 'Medium Value', 'Low Value'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
    plt.title('Customer Segmentation by Revenue')
    plt.tight_layout()
    plt.savefig('viz_customer_segments.png')
    plt.close()

if __name__ == "__main__":
    if not os.path.exists('customer_transactions.csv'):
        print("Data file not found. Please run generate_data.py first.")
    else:
        df = load_and_clean_data('customer_transactions.csv')
        metrics = calculate_metrics(df)
        generate_visualizations(df)
        print("\nAnalysis Complete. Visualizations saved.")
