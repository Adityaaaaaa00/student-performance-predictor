# 📚 Student Performance Tracker

A lightweight desktop app for recording students' daily study hours, viewing study trends, and getting a simple hour-based performance estimate. The project uses a familiar Tkinter interface and stores records locally in a CSV file.

> **Important:** The fail-risk and topper-chance figures are illustrative estimates based only on recorded study hours. They are not actual exam marks, a statistically validated prediction, or a guarantee of academic results.

## ✨ Features

- **Record a study session** with a student's name, date, hours studied, and roll number.
- **Keep records locally** in `study_data.csv`, next to the app.
- **View a bar chart** of total recorded study hours grouped by student name.
- **View a line chart** of recorded study hours over time, grouped by student name.
- **View a histogram** showing the distribution of individual recorded study-hour values.
- **Assess a student by roll number** using their cumulative recorded hours:
  - Estimated marks are calculated against a 100-hour reference target.
  - Below 30% estimated marks displays a **Risk Warning** with 99% fail risk.
  - Above 96% displays **CHEERS!** with 99% topper chance.
  - From 30% through 96%, inclusive, displays 50% fail risk and 50% topper chance.

## 🧰 Technologies

| Technology | Use |
| --- | --- |
| Python | Application logic |
| Tkinter (`tkinter`) | Desktop window, forms, buttons, and message dialogs |
| pandas | Reading, validating, aggregating, and appending CSV data |
| Matplotlib | Study charts |
| CSV | Simple local data storage |

`datetime`, `pathlib`, and `math` are Python standard-library modules used for date validation, locating the data file, and checking numeric input.

## ✅ Requirements

- Python 3.10 or later is recommended.
- Tkinter must be available in the Python installation.
- The third-party packages `pandas` and `matplotlib`.

## 🚀 Setup and run

Open PowerShell or a terminal in the project folder, then install the dependencies:

```powershell
python -m pip install pandas matplotlib
```

Launch the application:

```powershell
python app.py
```

On Windows, if `python` is not on your PATH, use the full path to your Python executable, for example:

```powershell
& "C:\Path\To\Python\python.exe" app.py
```

The main entry point is `app.py`. Run the command from the project folder, or use an absolute path to `app.py`; the CSV data file is located relative to the script itself.

## 🖱️ How to use

### Save a study session

1. Start the app using the command above.
2. Fill in **Name**, **Date**, **Hours Studied**, and **Roll Number**.
3. Enter the date as `YYYY-MM-DD`, for example `2026-10-14`.
4. Enter a finite, non-negative number of hours. Decimal values are allowed.
5. Select **Save Data**. On success, the record is appended to `study_data.csv` and the form is cleared.

All four fields are required. Invalid dates and negative, non-numeric, infinite, or NaN hour values are rejected with an error dialog.

### View charts

Select any of the chart buttons in the main window:

- **Show Bar Graph** sums hours by name across saved records.
- **Show Line Graph** plots each recorded session's hours over its date, grouped by name.
- **Show Histogram** shows the distribution of hours per saved session.

Charts require a readable CSV containing valid records. If no usable data is available, the app displays an error dialog.

### Assess risk or topper chance

1. Select **Assess Risk / Topper Chance**.
2. Enter the student's roll number exactly as saved.
3. The app adds the student's hours across all matching records and compares the result to the 100-hour reference target.

The estimate is capped at 100% and calculated as:

```text
estimated marks (%) = min(cumulative study hours / 100 × 100, 100)
```

For example, 25 cumulative hours produce an estimated 25%; 100 or more hours produce an estimated 100%. The app uses strict threshold comparisons: exactly 30% and exactly 96% are in the middle range.

### Understand the estimate

Study hours alone do not determine exam marks. Results do not account for subject difficulty, learning quality, attendance, prior knowledge, assessment format, or many other factors. Treat the percentages as a simple demonstration based on the app's fixed rules, **not reliable academic or career advice**.

## 🗃️ Project files

```text
student project/
├── app.py             # Main application
├── StudentTracker.py  # Earlier version of the tracker
├── study_data.csv     # Saved study records (created/updated by the app)
└── README.md          # Project documentation
```

The app reads and writes `study_data.csv` beside `app.py`. Its expected columns are:

```csv
Name,Date,Hours Studied,Roll Number
```

Each saved session is a separate row. Assessment totals include every valid record with the matching roll number. Keep a backup of the CSV if you want to preserve your records; deleting it removes the saved data.

## 🛠️ Troubleshooting

| Problem | What to check |
| --- | --- |
| `can't open file ... app.py` | Change to the project folder and confirm the file is named `app.py`. |
| `No module named 'pandas'` or `No module named 'matplotlib'` | Install dependencies with `python -m pip install pandas matplotlib` using the same Python interpreter used to launch the app. |
| Tkinter/Tk is unavailable | Use a Python distribution that includes Tk support. Tkinter is separate from the two pip-installed packages. |
| No data or invalid-record message | Check that `study_data.csv` is beside `app.py`, has the expected column headers, and contains valid rows. |
| No matching student during assessment | Check the roll number against the records in `study_data.csv`. |

## 🔒 Data and privacy

Study records are stored in a plain-text CSV file on the local machine. The application does not require an account or a network connection. Avoid sharing the CSV publicly if it contains student names or identifying roll numbers.