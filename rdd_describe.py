# Import required libraries for RDD
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from sklearn.preprocessing import PolynomialFeatures

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

def describe(rdd_data, bandwidth):
    """ input rdd_data 
    input bandwith in meters
    returns the descriptives stats"""
    
    rdd_sample = rdd_data[abs(rdd_data['distance']) <= bandwidth]

    # RDD Visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # 1. Scatter plot of price vs distance
    axes[0,0].scatter(rdd_sample[rdd_sample['treatment']==0]['distance'], 
                    rdd_sample[rdd_sample['treatment']==0]['log_price'], 
                    alpha=0.6, color='red', label='Outside (Control)', s=20)
    axes[0,0].scatter(rdd_sample[rdd_sample['treatment']==1]['distance'], 
                    rdd_sample[rdd_sample['treatment']==1]['log_price'], 
                    alpha=0.6, color='blue', label='Inside (Treatment)', s=20)
    axes[0,0].axvline(x=0, color='black', linestyle='--', linewidth=2, label='Historic Boundary')
    axes[0,0].set_xlabel('Distance to Historic Boundary')
    axes[0,0].set_ylabel('Log Price ($ PSM)')
    axes[0,0].set_title('RDD Plot: Log Price vs Distance to Boundary')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)

    # 2. Binned scatter plot for cleaner visualization
    bin_size = 50  # meters
    bins = np.arange(rdd_sample['distance'].min(), rdd_sample['distance'].max() + bin_size, bin_size)
    bin_centers = []
    bin_means = []

    for i in range(len(bins)-1):
        mask = (rdd_sample['distance'] >= bins[i]) & (rdd_sample['distance'] < bins[i+1])
        if mask.sum() > 0:
            bin_centers.append((bins[i] + bins[i+1]) / 2)
            bin_means.append(rdd_sample[mask]['log_price'].mean())

    axes[0,1].plot(bin_centers, bin_means, 'o-', color='green', markersize=4)
    axes[0,1].axvline(x=0, color='black', linestyle='--', linewidth=2, label='Historic Boundary')
    axes[0,1].set_xlabel('Distance to Historic Boundary')
    axes[0,1].set_ylabel('Mean Log Price ($ psf)')
    axes[0,1].set_title('Binned RDD Plot')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)

    # 3. Histogram of running variable
    axes[1,0].hist(rdd_sample[rdd_data['treatment']==0]['distance'], 
                bins=30, alpha=0.7, color='red', label='Outside', density=True)
    axes[1,0].hist(rdd_sample[rdd_data['treatment']==1]['distance'], 
                bins=30, alpha=0.7, color='blue', label='Inside', density=True)
    axes[1,0].axvline(x=0, color='black', linestyle='--', linewidth=2, label='Boundary')
    axes[1,0].set_xlabel('Distance to Historic Boundary')
    axes[1,0].set_ylabel('Density')
    axes[1,0].set_title('Distribution of Running Variable')
    axes[1,0].legend()

    # 4. Price distribution by treatment
    axes[1,1].hist(rdd_sample[rdd_sample['treatment']==0]['log_price'], 
                bins=30, alpha=0.7, color='red', label='Outside', density=True)
    axes[1,1].hist(rdd_sample[rdd_sample['treatment']==1]['log_price'], 
                bins=30, alpha=0.7, color='blue', label='Inside', density=True)
    axes[1,1].set_xlabel('Log Price ($ PSM)')
    axes[1,1].set_ylabel('Density')
    axes[1,1].set_title('Price Distribution by Treatment Status')
    axes[1,1].legend()

    plt.tight_layout()
    plt.show()

    print(f"Sample size: {len(rdd_sample)}")
    print(f"Treatment group (inside): {rdd_sample['treatment'].sum()}")
    print(f"Control group (outside): {len(rdd_sample) - rdd_sample['treatment'].sum()}")
    print(f"Distance range: {rdd_sample['distance'].min():.2f} to {rdd_sample['distance'].max():.2f}")

    # Basic summary statistics
    print("\nSummary Statistics by Treatment Status:")
    print(rdd_sample.groupby('treatment')[['log_price', 'Unit Price ($ PSM)', 'distance']].describe())