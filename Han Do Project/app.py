import streamlit as st
import pandas as pd
from io import StringIO

st.title("Baseball Pitching Stats Analyzer")

st.markdown("""
This app analyzes baseball pitching data from Trackman CSV files.
Upload your CSV files, select a team, and get detailed pitching statistics.
""")

# Team input
team = st.text_input("Enter the team you want to analyze (e.g., DAV_WIL):", "").strip()

# File uploader
uploaded_files = st.file_uploader("Upload Trackman CSV file(s)", type="csv", accept_multiple_files=True)

if st.button("Analyze Data") and team and uploaded_files:
    # Keep rel cols
    cols = [
        "Pitcher",
        "PitcherTeam",
        "BatterTeam",
        "TaggedPitchType",
        "RelSpeed",
        "InducedVertBreak",
        "HorzBreak"
    ]

    all_data = []

    for uploaded_file in uploaded_files:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        df = df[cols]
        df["PitcherTeam"] = df["PitcherTeam"].astype(str).str.strip()
        df["BatterTeam"] = df["BatterTeam"].astype(str).str.strip()
        all_data.append(df)

    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)

    # Filter for the selected team's pitchers only
    team_data = combined_df[combined_df["PitcherTeam"] == team].copy()

    if team_data.empty:
        st.error(f"No data found for team '{team}'. Please check the team name and uploaded files.")
    else:
        st.success(f"Analyzed {len(team_data)} pitches for team '{team}'")

        # Process data
        per_type = team_data.groupby(["Pitcher", "PitcherTeam", "TaggedPitchType"]).agg(
            Count=("TaggedPitchType", "size"),
            AvgVelo=("RelSpeed", "mean"),
            AvgVert=("InducedVertBreak", "mean"),
            AvgHorz=("HorzBreak", "mean"),
        ).reset_index()

        overall = team_data.groupby(["Pitcher", "PitcherTeam"]).agg(
            Count=("TaggedPitchType", "size"),
            AvgVelo=("RelSpeed", "mean"),
            AvgVert=("InducedVertBreak", "mean"),
            AvgHorz=("HorzBreak", "mean"),
        ).reset_index()

        overall["TaggedPitchType"] = "Overall"

        out = pd.concat([per_type, overall], ignore_index=True)
        out["__o"] = (out["TaggedPitchType"] == "Overall")
        out = out.sort_values(
            ["PitcherTeam", "Pitcher", "__o", "Count"],
            ascending=[True, True, True, False]
        ).drop(columns="__o")

        # Display results
        st.subheader("Pitching Statistics")
        st.dataframe(out)

        # Create text report
        text_report = []
        for (pitcher, team_name), sub in out.groupby(["Pitcher", "PitcherTeam"]):
            text_report.append(f"Pitcher: {pitcher} ({team_name})")
            text_report.append("-" * 60)
            for _, r in sub.iterrows():
                text_report.append(
                    f"{r['TaggedPitchType']:<14} | "
                    f"Count: {int(r['Count']):<4} | "
                    f"AvgVelo: {r['AvgVelo']:.2f} | "
                    f"AvgVert: {r['AvgVert']:.2f} | "
                    f"AvgHorz: {r['AvgHorz']:.2f}"
                )
            text_report.append("")

        text_content = "\n".join(text_report)

        # Download buttons
        csv_data = out.to_csv(index=False)
        st.download_button(
            label="Download CSV Report",
            data=csv_data,
            file_name=f"pitching_stats_{team}.csv",
            mime="text/csv"
        )

        st.download_button(
            label="Download Text Report",
            data=text_content,
            file_name=f"pitching_stats_{team}.txt",
            mime="text/plain"
        )

        # Show text report
        st.subheader("Text Report Preview")
        st.text_area("Report", text_content, height=300)

else:
    if not team:
        st.info("Please enter a team name.")
    if not uploaded_files:
        st.info("Please upload at least one CSV file.")