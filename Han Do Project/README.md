# Baseball Pitching Stats Analyzer

A Streamlit web app for analyzing baseball pitching data from Trackman CSV files.

## Features

- Upload multiple Trackman CSV files
- Analyze pitching statistics for a specific team
- View detailed stats by pitch type and overall
- Download results as CSV or text reports

## How to Run Locally

1. Install Python (if not already installed)
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. Open your browser to the URL shown (usually http://localhost:8501)

## How to Use

1. Enter the team code you want to analyze (e.g., DAV_WIL)
2. Upload your Trackman CSV file(s) using the file uploader
3. Click "Analyze Data"
4. View the statistics table
5. Download the CSV or text reports

## Deploy to Web

You can deploy this app to Streamlit Cloud for free:

1. Create a GitHub repository with these files
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy!

## Requirements

- Trackman CSV files with columns: Pitcher, PitcherTeam, BatterTeam, TaggedPitchType, RelSpeed, InducedVertBreak, HorzBreak
- Team codes should match exactly as they appear in the CSV files