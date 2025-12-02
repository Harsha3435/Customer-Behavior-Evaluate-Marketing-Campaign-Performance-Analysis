import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

sns.set(style="whitegrid")

def load_and_clean_data(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # 1. Handle missing values
    df.dropna(subset=['Clicks', 'Spend'], inplace=True)
    
    # 2. Ensure non-negative/zero spend
    df = df[df['Spend'] > 0]
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def calculate_metrics(df):
    print("\n--- Marketing Campaign Metrics ---")
    
    # Overall Metrics
    total_impressions = df['Impressions'].sum()
    total_clicks = df['Clicks'].sum()
    total_conversions = df['Conversions'].sum()
    total_spend = df['Spend'].sum()
    total_revenue = df['Revenue'].sum()
    
    ctr = (total_clicks / total_impressions) * 100
    conversion_rate = (total_conversions / total_clicks) * 100
    cpl = total_spend / total_conversions
    roi = ((total_revenue - total_spend) / total_spend) * 100
    cac = cpl # Approximation
    
    # --- New Metrics ---
    
    # Campaign Performance
    campaign_stats = df.groupby('Campaign ID').agg({
        'Spend': 'sum',
        'Revenue': 'sum'
    }).reset_index()
    campaign_stats['ROI'] = ((campaign_stats['Revenue'] - campaign_stats['Spend']) / campaign_stats['Spend']) * 100
    
    top_campaign = campaign_stats.loc[campaign_stats['ROI'].idxmax()]
    bottom_campaign = campaign_stats.loc[campaign_stats['ROI'].idxmin()]
    
    print(f"Top Campaign: {top_campaign['Campaign ID']} (ROI: {top_campaign['ROI']:.2f}%)")
    print(f"Bottom Campaign: {bottom_campaign['Campaign ID']} (ROI: {bottom_campaign['ROI']:.2f}%)")
    
    metrics = {
        'CTR': float(ctr),
        'Conversion Rate': float(conversion_rate),
        'CPL': float(cpl),
        'ROI': float(roi),
        'CAC': float(cac),
        'Top Campaign': str(top_campaign['Campaign ID']),
        'Top Campaign ROI': float(top_campaign['ROI']),
        'Bottom Campaign': str(bottom_campaign['Campaign ID']),
        'Bottom Campaign ROI': float(bottom_campaign['ROI'])
    }
    
    with open('campaign_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    return metrics

def generate_visualizations(df):
    print("\nGenerating Visualizations...")
    
    # 1. ROI by Campaign
    campaign_metrics = df.groupby('Campaign ID').agg({
        'Spend': 'sum',
        'Revenue': 'sum'
    }).reset_index()
    campaign_metrics['ROI'] = ((campaign_metrics['Revenue'] - campaign_metrics['Spend']) / campaign_metrics['Spend']) * 100
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=campaign_metrics, x='Campaign ID', y='ROI', palette='coolwarm')
    plt.xticks(rotation=45)
    plt.title('ROI by Campaign')
    plt.tight_layout()
    plt.savefig('viz_campaign_roi.png')
    plt.close()
    
    # 2. Conversion Rate vs Spend
    df['Daily_Conv_Rate'] = (df['Conversions'] / df['Clicks']) * 100
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Spend', y='Daily_Conv_Rate', hue='Campaign ID', alpha=0.6)
    plt.title('Daily Conversion Rate vs Spend')
    plt.tight_layout()
    plt.savefig('viz_conv_rate_vs_spend.png')
    plt.close()
    
    # 3. Monthly Impressions Trend
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_impressions = df.groupby('Month')['Impressions'].sum().reset_index()
    monthly_impressions['Month'] = monthly_impressions['Month'].astype(str)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_impressions, x='Month', y='Impressions', marker='o')
    plt.xticks(rotation=45)
    plt.title('Monthly Impressions Trend')
    plt.tight_layout()
    plt.savefig('viz_impressions_trend.png')
    plt.close()
    
    # --- New Visualizations ---
    
    # 4. CTR Trend Over Time
    # Aggregate by month for smoother line
    monthly_ctr = df.groupby('Month').agg({
        'Clicks': 'sum',
        'Impressions': 'sum'
    }).reset_index()
    monthly_ctr['CTR'] = (monthly_ctr['Clicks'] / monthly_ctr['Impressions']) * 100
    monthly_ctr['Month'] = monthly_ctr['Month'].astype(str)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_ctr, x='Month', y='CTR', marker='o', color='purple')
    plt.xticks(rotation=45)
    plt.title('Monthly Click-Through Rate (CTR) Trend')
    plt.tight_layout()
    plt.savefig('viz_ctr_trend.png')
    plt.close()

if __name__ == "__main__":
    if not os.path.exists('marketing_campaigns.csv'):
        print("Data file not found. Please run generate_data.py first.")
    else:
        df = load_and_clean_data('marketing_campaigns.csv')
        metrics = calculate_metrics(df)
        generate_visualizations(df)
        print("\nCampaign Analysis Complete. Visualizations saved.")
