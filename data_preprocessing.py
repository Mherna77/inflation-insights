"""
Data Pre-processing for World Bank Data 2025
Simplified version for GitHub - uses relative paths within repository
"""

import pandas as pd
from pathlib import Path


def load_data(data_path):
    """Load the dataset from the data folder"""
    df = pd.read_csv(data_path)
    print(f"✓ Loaded data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def clean_data(df):
    """Clean and preprocess the dataset"""
    print("\nCleaning data...")
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Convert year to integer
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    
    # Remove rows where ALL economic indicators are missing
    economic_cols = [col for col in df.columns if col not in ['country_name', 'country_id', 'year']]
    df = df.dropna(subset=economic_cols, how='all')
    
    # Sort by country and year
    df = df.sort_values(['country_name', 'year']).reset_index(drop=True)
    
    print(f"✓ Cleaned data: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"  - Countries: {df['country_name'].nunique()}")
    print(f"  - Year range: {df['year'].min()} - {df['year'].max()}")
    
    return df


def main():
    """Main preprocessing pipeline"""
    print("="*60)
    print("World Bank Data Pre-processing")
    print("="*60)
    
    # Use relative path from repository root
    data_path = Path("data/world_bank_data_2025.csv")
    
    # Load and clean data
    df = load_data(data_path)
    df_clean = clean_data(df)
    
    # Create output directory
    output_dir = Path("preprocessed_data")
    output_dir.mkdir(exist_ok=True)
    
    # Save cleaned data
    output_path = output_dir / "world_bank_data_cleaned.csv"
    df_clean.to_csv(output_path, index=False)
    print(f"\n✓ Saved cleaned data to: {output_path}")
    
    # Save report
    report_path = output_dir / "preprocessing_report.txt"
    with open(report_path, 'w') as f:
        f.write("Data Pre-processing Report\n")
        f.write("="*60 + "\n\n")
        f.write(f"Input: {data_path}\n")
        f.write(f"Output: {output_path}\n\n")
        f.write(f"Shape: {df_clean.shape}\n")
        f.write(f"Countries: {df_clean['country_name'].nunique()}\n")
        f.write(f"Years: {df_clean['year'].min()} - {df_clean['year'].max()}\n\n")
        f.write("Missing values:\n")
        f.write(df_clean.isnull().sum().to_string())
    
    print(f"✓ Saved report to: {report_path}")
    print("\n" + "="*60)
    print("✓ Pre-processing complete!")
    print("="*60)


if __name__ == "__main__":
    main()
