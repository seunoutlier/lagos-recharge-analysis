"""
Identifying Optimal Rainfall Conditions for Groundwater Recharge
Using Machine Learning: Evidence from Lagos Megacity

Author: [Oluwaseun Franklin Olabode]
Institution: [University of Aberdeen]
Email: [oluwaseun.folabode@gmail.com]

Presented at: Alan Turing Institute PhD Presentation Day (March 2026)

Key Finding: Lagos lost 38 percentage points of recharge efficiency at 
moderate rainfall (150-200mm) between the 1980s and 2010s (p=0.0015).

Paper Reference: 
Olabode & Comte (2025). Long-term groundwater security in the fast-growing 
coastal megacity of Lagos, Nigeria. Hydrological Sciences Journal.
DOI: 10.1080/02626667.2025.2505171
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
np.random.seed(42)


# =============================================================================
# DATA LOADING
# =============================================================================

def load_data(filepath):
    """Load and prepare the Lagos water balance dataset."""
    df = pd.read_excel(filepath)
    print(f"Loaded {len(df)} records ({int(df.Year.min())}-{int(df.Year.max())})")
    return df


# =============================================================================
# EFFICIENCY CALCULATION
# =============================================================================

def calculate_efficiency(df, min_precip=10):
    """Calculate recharge and runoff efficiency."""
    df_analysis = df[df['Precipitation_mm'] > min_precip].copy()
    
    df_analysis['Recharge_eff'] = (
        df_analysis['Recharge_mm'] / df_analysis['Precipitation_mm']
    ) * 100
    
    df_analysis['Runoff_eff'] = (
        df_analysis['Runoff_mm'] / df_analysis['Precipitation_mm']
    ) * 100
    
    return df_analysis


# =============================================================================
# DECADE ASSIGNMENT
# =============================================================================

def assign_decades(df):
    """Assign decade labels to each record."""
    def get_decade(year):
        if year < 1990:
            return '1980s'
        elif year < 2000:
            return '1990s'
        elif year < 2010:
            return '2000s'
        else:
            return '2010s'
    
    df['Decade'] = df['Year'].apply(get_decade)
    return df


# =============================================================================
# DECADAL ANALYSIS
# =============================================================================

def analyze_by_decade(df):
    """Calculate efficiency by precipitation bin for each decade."""
    
    bins = [0, 50, 100, 150, 200, 250, 300, 400, 700]
    labels = ['0-50', '50-100', '100-150', '150-200', 
              '200-250', '250-300', '300-400', '400+']
    
    df['Precip_bin'] = pd.cut(df['Precipitation_mm'], bins=bins, labels=labels)
    
    decades = ['1980s', '1990s', '2000s', '2010s']
    results = {}
    
    print("\nOptimal Recharge Zone by Decade:")
    print("-" * 55)
    print(f"{'Decade':<10} {'Optimal Zone':<15} {'Peak Efficiency':<18}")
    print("-" * 55)
    
    for decade in decades:
        df_decade = df[df['Decade'] == decade]
        efficiency = df_decade.groupby('Precip_bin')['Recharge_eff'].agg(['mean', 'std', 'count'])
        
        optimal_bin = efficiency['mean'].idxmax()
        optimal_eff = efficiency['mean'].max()
        
        results[decade] = {
            'efficiency': efficiency,
            'optimal_bin': optimal_bin,
            'optimal_eff': optimal_eff,
            'n': len(df_decade)
        }
        
        print(f"{decade:<10} {optimal_bin:<15} {optimal_eff:>6.1f}%")
    
    return results, labels


# =============================================================================
# STATISTICAL TESTING
# =============================================================================

def test_significance(df, precip_range='150-200'):
    """Perform t-test comparing 1980s vs 2010s efficiency."""
    
    df_1980s = df[(df['Decade'] == '1980s') & 
                  (df['Precip_bin'] == precip_range)]['Recharge_eff']
    df_2010s = df[(df['Decade'] == '2010s') & 
                  (df['Precip_bin'] == precip_range)]['Recharge_eff']
    
    if len(df_1980s) >= 3 and len(df_2010s) >= 3:
        mean_1980s = df_1980s.mean()
        mean_2010s = df_2010s.mean()
        change = mean_2010s - mean_1980s
        t_stat, p_value = stats.ttest_ind(df_1980s, df_2010s)
        
        print(f"\nStatistical Test: {precip_range} mm/month")
        print("-" * 50)
        print(f"1980s mean: {mean_1980s:.1f}%")
        print(f"2010s mean: {mean_2010s:.1f}%")
        print(f"Change: {change:+.1f}%")
        print(f"p-value: {p_value:.4f}")
        print(f"Significant: {'YES' if p_value < 0.05 else 'No'}")
        
        return {
            'mean_1980s': mean_1980s,
            'mean_2010s': mean_2010s,
            'change': change,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    else:
        print(f"Insufficient data for {precip_range}")
        return None


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_decadal_shift(results, labels, output_path='Figure_Decadal_Shift.png'):
    """Create main figure showing decadal shift in efficiency."""
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    decades = ['1980s', '1990s', '2000s', '2010s']
    colors = ['#1a5276', '#2e86ab', '#f39c12', '#c0392b']
    markers = ['o', 's', '^', 'D']
    bin_centers = [25, 75, 125, 175, 225, 275, 350, 500]
    
    for decade, color, marker in zip(decades, colors, markers):
        efficiency = results[decade]['efficiency']
        means = []
        for label in labels:
            try:
                means.append(efficiency.loc[label, 'mean'])
            except:
                means.append(np.nan)
        
        ax.plot(bin_centers, means, marker=marker, color=color, linewidth=2.5,
                markersize=10, label=decade, markeredgecolor='white', markeredgewidth=2)
    
    # Highlight significant decline zone
    ax.axvspan(150, 200, alpha=0.2, color='red', label='Significant decline zone')
    
    ax.annotate('SIGNIFICANT DECLINE\n-37.8% (p=0.0015)',
                xy=(175, 55), xytext=(280, 65),
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    
    ax.set_xlabel('Monthly Precipitation (mm)', fontsize=14)
    ax.set_ylabel('Recharge Efficiency (%)', fontsize=14)
    ax.set_title('TEMPORAL SHIFT IN RECHARGE EFFICIENCY\nLagos Megacity: 1980s → 2010s',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, title='Decade', title_fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 550)
    ax.set_ylim(0, 80)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_efficiency_decline(results, output_path='Figure_Efficiency_Decline.png'):
    """Create bar chart showing efficiency decline."""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    decades = ['1980s', '1990s', '2000s', '2010s']
    colors = ['#1a5276', '#2e86ab', '#f39c12', '#c0392b']
    
    # Left: Peak efficiency
    ax1 = axes[0]
    peak_effs = [results[d]['optimal_eff'] for d in decades]
    bars = ax1.bar(decades, peak_effs, color=colors, edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars, peak_effs):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{val:.1f}%', ha='center', fontsize=12, fontweight='bold')
    
    ax1.set_ylabel('Peak Recharge Efficiency (%)', fontsize=12)
    ax1.set_xlabel('Decade', fontsize=12)
    ax1.set_title('Peak Efficiency is DECLINING', fontsize=13, fontweight='bold')
    ax1.set_ylim(0, 85)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Right: Efficiency at 150-200mm
    ax2 = axes[1]
    eff_150_200 = []
    for decade in decades:
        try:
            val = results[decade]['efficiency'].loc['150-200', 'mean']
            eff_150_200.append(val)
        except:
            eff_150_200.append(np.nan)
    
    bars2 = ax2.bar(decades, eff_150_200, color=colors, edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars2, eff_150_200):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{val:.1f}%', ha='center', fontsize=12, fontweight='bold')
    
    ax2.annotate('', xy=(3, eff_150_200[3]), xytext=(0, eff_150_200[0]),
                 arrowprops=dict(arrowstyle='->', color='red', lw=3))
    ax2.text(1.5, 55, f'-37.8%\n(p=0.0015)', fontsize=12, fontweight='bold',
             color='red', ha='center')
    
    ax2.set_ylabel('Recharge Efficiency (%)', fontsize=12)
    ax2.set_xlabel('Decade', fontsize=12)
    ax2.set_title('Efficiency at 150-200mm: COLLAPSED', fontsize=13, fontweight='bold')
    ax2.set_ylim(0, 85)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main(filepath):
    """Run complete analysis."""
    
    print("=" * 65)
    print("IDENTIFYING OPTIMAL RAINFALL CONDITIONS FOR GROUNDWATER RECHARGE")
    print("Evidence from Lagos Megacity")
    print("=" * 65)
    
    # Load data
    df = load_data(filepath)
    
    # Calculate efficiency
    df_analysis = calculate_efficiency(df)
    
    # Assign decades
    df_analysis = assign_decades(df_analysis)
    
    # Analyze by decade
    results, labels = analyze_by_decade(df_analysis)
    
    # Statistical test
    stats_result = test_significance(df_analysis, '150-200')
    
    # Create figures
    plot_decadal_shift(results, labels)
    plot_efficiency_decline(results)
    
    # Print summary
    print("\n" + "=" * 65)
    print("KEY FINDING")
    print("=" * 65)
    print("""
Lagos lost 38 percentage points of recharge efficiency at moderate 
rainfall (150-200mm) between the 1980s and 2010s (p=0.0015).

The city's hydrological sweet spot has been paved over.
    """)
    
    return results, stats_result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "data/lagos_water_balance.xlsx"
    
    main(filepath)
