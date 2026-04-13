import pandas as pd


#error 1: get team from user input
MY_TEAM = input("Enter the team you want to analyze (e.g., DAV_WIL): ").strip()


#change 1: file list for more dynamic use
files = [
   "wilsonfield1.csv",
   "wilsonfield.csv"
]

# note: user, please select files via terminal (drag/drop). Press Enter to use defaults.
s = input("Drag Trackman CSV file(s) here, separate with comma, or press Enter to use defaults: ").strip()
if s:
    files = [p.strip().strip('"').strip("'") for p in s.split(",") if p.strip()]


#keep rel cols
cols = [
   "Pitcher",
   "PitcherTeam",
   "BatterTeam",
   "TaggedPitchType",
   "RelSpeed",
   "InducedVertBreak",
   "HorzBreak"
]


def deliverable2_table(df):
   per_type = df.groupby(["Pitcher", "PitcherTeam", "TaggedPitchType"]).agg(
       Count=("TaggedPitchType", "size"),
       AvgVelo=("RelSpeed", "mean"),
       AvgVert=("InducedVertBreak", "mean"),
       AvgHorz=("HorzBreak", "mean"),
   ).reset_index()


   overall = df.groupby(["Pitcher", "PitcherTeam"]).agg(
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


   return out


def write_txt_report(df, filename):
   lines = []


   for (pitcher, team), sub in df.groupby(["Pitcher", "PitcherTeam"]):
       lines.append(f"Pitcher: {pitcher} ({team})")
       lines.append("-" * 60)
       for _, r in sub.iterrows():
           lines.append(
               f"{r['TaggedPitchType']:<14} | "
               f"Count: {int(r['Count']):<4} | "
               f"AvgVelo: {r['AvgVelo']:.2f} | "
               f"AvgVert: {r['AvgVert']:.2f} | "
               f"AvgHorz: {r['AvgHorz']:.2f}"
           )
       lines.append("")


   with open(filename, "w") as f:
       f.write("\n".join(lines))


def process_file(current):
   df = pd.read_csv(current)


   df = df[cols]


   df["PitcherTeam"] = df["PitcherTeam"].astype(str).str.strip()
   df["BatterTeam"] = df["BatterTeam"].astype(str).str.strip()


   # Filter for the selected team's pitchers only
   team_data = df[df["PitcherTeam"] == MY_TEAM].copy()


   print("file:", current)
   print("team analyzed:", MY_TEAM)
   print(team_data["Pitcher"].value_counts(dropna=False))


   out = deliverable2_table(team_data)


   # note: handle full file paths safely
   base = str(current).split("/")[-1].replace(".csv", "")
   out.to_csv(f"{base}_{MY_TEAM}_pitching_stats.csv", index=False)
   write_txt_report(out, f"{base}_{MY_TEAM}_pitching_stats.txt")


for f in files:
   process_file(f)

