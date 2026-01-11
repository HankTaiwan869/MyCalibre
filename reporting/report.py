import os
import sys
from fpdf import FPDF, XPos, YPos
import pandas as pd
from datetime import datetime
from reporting import plot

# Set font to support Chinese characters
import matplotlib
matplotlib.rc('font', family='Microsoft YaHei') 

START_YEAR = 2019

def get_base_dir():
    # Running as a bundled executable
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # Running as a script
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = get_base_dir()
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

def prepare_data(books):
    # Prepare dataframe for visualization
    columns = ["id", "title", "author", "time", "lang", "orig_lang", "genre", "rating", "note"]
    df = pd.DataFrame(books, columns=columns)
    df = df[df['time']>='2020-01']
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m').dt.to_period('M')
    return df

# Create pdf template
class PDFReport(FPDF):
    def header(self):
        self.set_font("Times", "B", 16)
        self.cell(
            0,
            10,
            "Book Report",
            border=False,
            align="C",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT
        )
        self.ln(10)
    
    def add_section_title(self, title):
        self.set_font("Times", "B", 14)
        self.cell(
            0,
            10,
            title,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT
        )
        self.ln(3)

    def add_paragraph(self, text):
        self.set_font("Times", "", 12)
        self.multi_cell(0, 8, text)
        self.ln(5)

    def add_image(self, image_path, w=180):
        self.image(image_path, x=(210 - w) / 2, w=w)
        self.ln(10)

def generate_report(books, output_file="report.pdf"):
    """Generate complete PDF report with yearly and overall summaries"""
    pdf = PDFReport()
    df = prepare_data(books)
    
    current_year = datetime.now().year
    books_this_year = len(df[df['time'].dt.year == current_year])
    
    # ===== YEARLY SUMMARY =====
    pdf.add_page()
    pdf.add_section_title(f"{current_year} Summary")
    pdf.add_paragraph(
        f"You have read {books_this_year} books this year! "
        f"Here are the breakdowns."
    )
    
    # Yearly plots
    # Plot 1: Language Distribution
    lang_plot = plot.create_yearly_language_plot(df, current_year)
    pdf.add_image(lang_plot, w=120)
    # Plot 2: Genre Distribution
    genre_plot = plot.create_yearly_genre_plot(df, current_year)
    pdf.add_image(genre_plot, w=150)
    # Plot 3: Rating Distribution
    rating_plot = plot.create_yearly_rating_plot(df, current_year)
    pdf.add_image(rating_plot, w=140)
    # Plot 4: Monthly Trend
    monthly_plot = plot.create_yearly_monthly_trend_plot(df, current_year)
    pdf.add_image(monthly_plot, w=170)
    
    # ===== OVERALL SUMMARY =====
    pdf.add_page()
    pdf.add_section_title("Overall Summary")
    pdf.add_paragraph(
        f"Since {START_YEAR}, you've read {len(df)} books. "
        f"Here's your overall reading journey."
    )
    
    # Overall plots
    # Plot 1: Yearly Trend
    yearly_trend = plot.create_overall_yearly_trend_plot(df)
    pdf.add_image(yearly_trend, w=170)
    # Plot 2: Top Authors
    top_authors = plot.create_top_authors_plot(df)
    pdf.add_image(top_authors, w=150)
    # Plot 3: Overall Ratings
    overall_rating = plot.create_overall_rating_plot(df)
    pdf.add_image(overall_rating, w=120)
    # Plot 4: Overall Languages
    overall_lang = plot.create_overall_language_plot(df)
    pdf.add_image(overall_lang, w=120)
    
    # Save PDF
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = f"report_{timestamp}.pdf"
    output_path = os.path.join(REPORTS_DIR, output_file)
    pdf.output(output_path)
    
    return output_path
    

if __name__ == "__main__":
    books_sample = [
    (1, "Harry Potter", "J.K. Rowling", "2022-07", "English", "English", "Fantasy", "Love", "Bestseller"),
    (2, "The Hobbit", "J.R.R. Tolkien", "2022-09", "English", "English", "Fantasy", "Like", ""),
    (3, "红楼梦", "曹雪芹", "2022-01", "Chinese", "Chinese", "Drama", "Fine", "Classic"),
    (4, "Les Misérables", "Victor Hugo", "2022-03", "French", "French", "Historical", "Meh", ""),
    (5, "1984", "George Orwell", "2022-06", "English", "English", "Dystopian", "Textbook", "Fiction"),
    (6, "Harry Potter", "J.K. Rowling", "2026-01", "English", "English", "Fantasy", "Love", "Bestseller")
    ]

    generate_report(books_sample)
    print(f"PDF saved!")

