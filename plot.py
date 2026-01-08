import os
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
 
# Set font to support Chinese characters
import matplotlib
matplotlib.rc('font', family='Microsoft YaHei') 


# Prepare folders
def get_base_dir():
    """Get the directory where the app is running from"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

PALETTE = "Set2"


# ===== YEARLY SUMMARY PLOTS =====

def create_yearly_language_plot(df, year):
    """Pie chart of languages read in a specific year"""

    df_year = df[df['time'].dt.year == year]
    lang_count = df_year['lang'].value_counts()
    
    plt.figure(figsize=(5, 5))
    plt.pie(
        lang_count,
        labels=lang_count.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("Set2", n_colors=len(lang_count))
    )
    plt.title(f"Languages Read in {year}")
    plot_file = os.path.join(PLOTS_DIR, f"yearly_language_{year}.png")
    plt.savefig(plot_file, bbox_inches='tight')
    plt.close()
    return plot_file

def create_yearly_genre_plot(df, year):
    """Bar chart of genres read in a specific year"""
    df_year = df[df['time'].dt.year == year]
    genre_count = df_year['genre'].value_counts()
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x=genre_count.values, y=genre_count.index, hue=genre_count.index, palette= PALETTE)
    plt.title(f"Genres Read in {year}")
    plt.xlabel("Number of Books")
    plt.ylabel("Genre")
    plot_file = os.path.join(PLOTS_DIR, f"yearly_genre_{year}.png")
    plt.savefig(plot_file, bbox_inches='tight')
    plt.close()
    return plot_file

def create_yearly_rating_plot(df, year):
    """Bar chart of ratings in a specific year"""
    df_year = df[df['time'].dt.year == year]
    rating_count = df_year['rating'].value_counts()
    
    # Define rating order and colors
    rating_order = ['Love', 'Like', 'Fine', 'Meh', 'Textbook']
    rating_colors = {'Love': '#E74C3C', 'Like': '#3498DB', 'Fine': '#95A5A6', 
                     'Meh': '#2C3E50', 'Textbook': '#C77DFF'}
    
    # Reindex to ensure order and fill missing ratings with 0
    rating_count = rating_count.reindex(rating_order, fill_value=0)
    colors = [rating_colors.get(r, '#999999') for r in rating_count.index]
    
    plt.figure(figsize=(7, 5))
    plt.bar(rating_count.index, rating_count.values, color=colors)
    plt.title(f"Ratings Distribution in {year}")
    plt.xlabel("Rating")
    plt.ylabel("Number of Books")
    plot_file = os.path.join(PLOTS_DIR, f"yearly_rating_{year}.png")
    plt.savefig(plot_file, bbox_inches='tight')
    plt.close()
    return plot_file

def create_yearly_monthly_trend_plot(df, year):
    """Bar chart of monthly reading trend for a specific year compared to previous year"""
    # Get data for current year and previous year
    df_current = df[df['time'].dt.year == year]
    df_previous = df[df['time'].dt.year == year - 1]
    
    # Group by month for current year
    monthly_current = (
        df_current.groupby(df_current['time'].dt.month)['id']
        .count()
        .reindex(range(1, 13), fill_value=0)  # Ensure all 12 months exist
        .reset_index(name='book_count')
    )
    monthly_current['year'] = year
    monthly_current.rename(columns={'index': 'month'}, inplace=True)
    
    # Group by month for previous year
    monthly_previous = (
        df_previous.groupby(df_previous['time'].dt.month)['id']
        .count()
        .reindex(range(1, 13), fill_value=0)  # Ensure all 12 months exist
        .reset_index(name='book_count')
    )
    monthly_previous['year'] = year - 1
    monthly_previous.rename(columns={'index': 'month'}, inplace=True)
    
    # Combine both years
    monthly_combined = pd.concat([monthly_previous, monthly_current], ignore_index=True)
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=monthly_combined, x='time', y='book_count', hue='year', palette=PALETTE)
    plt.title(f"Monthly Reading Trend: {year-1} vs {year}")
    plt.xlabel("Month")
    plt.ylabel("Number of Books")
    plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Year')
    plot_file = os.path.join(PLOTS_DIR, f"yearly_monthly_{year}.png")
    plt.savefig(plot_file, bbox_inches='tight')
    plt.close()
    return plot_file
# ===== OVERALL SUMMARY PLOTS =====

def create_overall_yearly_trend_plot(df):
    """Bar chart showing total books read per year"""
    df_copy = df.copy()
    df_copy['year'] = df_copy['time'].dt.year
    
    yearly_count = (
        df_copy.groupby('year')['id']
        .count()
        .sort_index()
        .reset_index(name='book_count')
    )
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=yearly_count, x='year', y='book_count', hue='year', palette=PALETTE)
    plt.title("Yearly Reading Trend")
    plt.xlabel("Year")
    plt.ylabel("Number of Books")
    plot_file = os.path.join(PLOTS_DIR, "overall_yearly_trend.png")
    plt.savefig(plot_file, bbox_inches='tight')
    plt.close()
    return plot_file

def create_top_authors_plot(df):
    """Bar chart of top 5 authors"""
    author_count = df['author'].value_counts().head(5)
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x=author_count.values, y=author_count.index, hue=author_count.index, palette=PALETTE)
    plt.title("Top 5 Authors")
    plt.xlabel("Number of Books")
    plt.ylabel("Author")
    plot_file = os.path.join(PLOTS_DIR, "top_authors.png")
    plt.savefig(plot_file, bbox_inches='tight')
    plt.close()
    return plot_file

def create_overall_rating_plot(df):
    """Pie chart of overall ratings distribution"""
    rating_count = df['rating'].value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(
        rating_count,
        labels=rating_count.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("Set2", n_colors=len(rating_count))
    )
    plt.title("Overall Ratings Distribution")
    plot_file = os.path.join(PLOTS_DIR, "overall_rating.png")
    plt.savefig(plot_file, bbox_inches='tight')
    plt.close()
    return plot_file

def create_overall_language_plot(df):
    """Pie chart of overall languages distribution"""
    lang_count = df['lang'].value_counts()
    
    plt.figure(figsize=(6, 6))
    plt.pie(
        lang_count,
        labels=lang_count.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("Set2", n_colors=len(lang_count))
    )
    plt.title("Overall Languages Read")
    plot_file = os.path.join(PLOTS_DIR, "overall_language.png")
    plt.savefig(plot_file, bbox_inches='tight')
    plt.close()
    return plot_file
