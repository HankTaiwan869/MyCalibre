# important: this part is unfinished, plan to add more plots and summary text

import os
import sys
from fpdf import FPDF
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

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

def create_plots(books, type = "language"):

    # Prepare dataframe for visualization
    columns = ["id", "title", "author", "time", "lang", "orig_lang", "genre", "rating", "note"]
    df = pd.DataFrame(books, columns=columns)
    df = df[df['time']>='2020-01']
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m').dt.to_period('M')
    
    plot_file = None
    
    if type == "language":
        lang_count = df['lang'].value_counts()
        plt.figure(figsize=(4,4))
        plt.pie(
            lang_count,
            labels=lang_count.index,
            autopct='%1.1f%%',
            startangle=90
        )
        plt.title("Language Read")
        plot_file = os.path.join(PLOTS_DIR, "language_plot.png")
        plt.savefig(plot_file)
        plt.close()  # close figure to avoid overlapping

    elif type == "trend":
        plt.figure(figsize=(8, 7))

        # Aggregate
        df_time = (
            df.groupby('time')['id']
            .count()
            .sort_index()
            .reset_index(name='book_count')
        )

        # Convert Period -> string for proper axis labels
        df_time['time'] = df_time['time'].astype(str)

        # Plot
        sns.barplot(
            data=df_time,
            x='time',
            y='book_count'
        )

        plt.title("Monthly Trend of Books Reading")
        plt.xlabel("Time")
        plt.ylabel("Number of Books")

        # Show every 3rd label
        ticks = range(0, len(df_time), 3)
        plt.xticks(ticks, df_time['time'].iloc[ticks], rotation=45)


        plot_file = os.path.join(PLOTS_DIR, "trend_plot.png")
        plt.savefig(plot_file)
        plt.close()
    
    return plot_file

# Create pdf template
class PDFReport(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "Book Report", border=False, ln=True, align="C")
        self.ln(10)

    def add_paragraph(self, text):
        self.set_font("helvetica", "", 12)
        self.multi_cell(0, 8, text)
        self.ln(5)

    def add_image(self, image_path, w=180):
        self.image(image_path, x=(210-w)/2, w=w)
        self.ln(10)

def generate_report(books, output_file="report.pdf"):
    pdf = PDFReport()
    pdf.add_page()

    
    # Add plot
    plot_file = create_plots(books, type = "language")
    pdf.add_image(plot_file, w = 120)
    
    plot_file = create_plots(books, type = "trend")
    pdf.add_image(plot_file)

    # Save PDF in reports folder
    timestamp = datetime.now().strftime("%Y%m%d")
    output_file = f"report_{timestamp}.pdf"
    output_path = os.path.join(REPORTS_DIR, output_file)
    pdf.output(output_path)
    print(f"PDF saved to {output_path}")

if __name__ == "__main__":
    books_sample = [
    (1, "Harry Potter", "J.K. Rowling", "2022-07", "English", "English", "Fantasy", "4.8", "Bestseller"),
    (2, "The Hobbit", "J.R.R. Tolkien", "2022-09", "English", "English", "Fantasy", "4.7", ""),
    (3, "红楼梦", "曹雪芹", "2022-01", "Chinese", "Chinese", "Drama", "4.9", "Classic"),
    (4, "Les Misérables", "Victor Hugo", "2022-03", "French", "French", "Historical", "4.6", ""),
    (5, "1984", "George Orwell", "2022-06", "English", "English", "Dystopian", "4.5", "Fiction")
    ]
    #generate_report(books_sample)
    generate_report(books_sample)


