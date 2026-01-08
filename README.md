[Scroll down for English version]

## MyCalibre
我建立的個人閱讀紀錄app，用於記錄和分析我的閱讀歷史並一鍵生成視覺化報告。

### 功能特色
- 追蹤書籍的自訂資料（語言、譯者、類型、評分）
- 使用 SQLite 資料庫進行資料儲存
- 搜尋和篩選我的書籍
- 生成包含閱讀分析的 PDF 報告（語言分布、每月趨勢等）
- 匯出為 CSV 檔案以進行備份

### 使用python套件
- **圖形介面**: Tkinter
- **資料庫**: SQLite3
- **視覺化**: Matplotlib、Seaborn, Pandas
- **報告**: FPDF、Pandas

### 截圖
#### 主介面
![主介面](screenshots/main_interface.png)
*書籍記錄表單與功能按鈕*

#### View all books (檢視所有書籍)
![檢視所有書籍](screenshots/view_all_window.png)
*資料庫中所有書籍的清單視圖*

### 本地執行
```bash
pip install fpdf seaborn matplotlib pandas
python main.py
```

### 專案結構
- `main.py` - 程式進入點
- `gui.py` - Tkinter 使用者介面
- `database.py` - SQLite 資料庫操作
- `validation.py` - 輸入驗證與資料檢查
- `plot.py` - 資料視覺化與圖表生成
- `report.py` - PDF 報表生成

**備註**：此應用程式是為我的閱讀習慣量身打造（特定類型、評分系統等）。歡迎 fork 並根據您自己的需求進行調整！

---------------------------------------

## MyCalibre
A personal reading tracker I built to log and analyze my reading history with visual reports.

### Features
- Track books with custom metadata (language, translator, genre, rating)
- SQLite database for data storage
- Search and filter my collection
- Generate PDF reports with reading analytics (language distribution, monthly trends, etc.)
- Export to CSV for backup

### Python Packages Used
- **GUI**: Tkinter
- **Database**: SQLite3
- **Visualization**: Matplotlib, Seaborn, Pandas
- **Reports**: FPDF, Pandas

### Screenshots

#### Main Interface
![Main Interface](screenshots/main_interface.png)
*Book entry form with action buttons*

#### View All Books
![View All Books](screenshots/view_all_window.png)
*Complete list view of all books in the database*

### Running Locally
```bash
pip install fpdf seaborn matplotlib pandas
python main.py
```

### Project Structure
- `main.py` - Entry point
- `gui.py` - Tkinter interface
- `database.py` - SQLite operations
- `validation.py` - Input validation and data verification
- `plot.py` - Data visualization and chart generation
- `report.py` - PDF generation

**Note**: This app is personalized for my reading habits (specific genres, rating system, etc.). Feel free to fork and adapt for your own use!



