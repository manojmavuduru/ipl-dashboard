import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Header Configuration
st.set_page_config(page_title="IPL Analytics", layout="wide")
st.title("🏏 IPL Cricket Executive Dashboard")
st.markdown("---")

# 2. Load the Data (Task 3: Analysis)
# This reads the deliveries.csv file we just unzipped
df = pd.read_csv("deliveries.csv")

# 3. Create a Sidebar Option for the Bosses
st.sidebar.header("Filter Options")
all_teams = sorted(df['batting_team'].unique())
selected_team = st.sidebar.selectbox("Select Batting Team", all_teams)

# Filter the data based on what team they click
filtered_df = df[df['batting_team'] == selected_team]

# 4. Show a summary of stats (Task 3: Insights)
st.subheader(f"📊 Quick Metrics for {selected_team}")
total_runs = filtered_df['total_runs'].sum()
total_wide_runs = filtered_df['wide_runs'].sum()

# Display them side-by-side in neat cards
col1, col2 = st.columns(2)
col1.metric("Total Runs Scored", f"{total_runs:,}")
col2.metric("Total Wide Balls Given", f"{total_wide_runs:,}")

# 5. Build an Interactive Chart (Task 4: Visualization)
st.subheader("Top 10 Batsmen by Runs")
# Calculate the highest run scorers for that selected team
top_batsmen = filtered_df.groupby('batsman')['batsman_runs'].sum().reset_index()
top_batsmen = top_batsmen.sort_values(by='batsman_runs', ascending=False).head(10)

fig = px.bar(top_batsmen, x='batsman', y='batsman_runs', 
             labels={'batsman': 'Batsman Name', 'batsman_runs': 'Runs'},
             color='batsman_runs', color_continuous_scale='Viridis')

st.plotly_chart(fig, use_container_width=True)
# 6. Add a Second Chart for Deeper Insight
st.markdown("---")
st.subheader("Extra Runs Analysis (Wides vs No Balls)")

# Calculate total wides and noballs for the selected team
extras_data = filtered_df.groupby('match_id')[['wide_runs', 'noball_runs']].sum().reset_index()
total_wides = extras_data['wide_runs'].sum()
total_noballs = extras_data['noball_runs'].sum()

# Put them into a simple comparison table
extras_summary = pd.DataFrame({
    'Extra Type': ['Wide Runs', 'No Ball Runs'],
    'Count': [total_wides, total_noballs]
})

# Create a beautiful Pie Chart to show the comparison
fig_pie = px.pie(extras_summary, values='Count', names='Extra Type', 
                 title='Distribution of Discipline Extras',
                 color_discrete_sequence=['#2adb8f', '#ff4b4b'])

st.plotly_chart(fig_pie, use_container_width=True)