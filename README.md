# Volleyball-Serve-Analytics-Engine

CLI analytics tool analyzing 2,639 professional volleyball matches using custom data structures, merge sort, and Plotly visualizations.

------------------------------------------------------------------------------------

**Overview**

I play volleyball competitively and wanted to combine that with what I was learning in data structures. This project goes through 2,639 matches across 23 professional teams, ranks them by ace rate, tracks how teams perform over time, and lets you search any team interactively with live Plotly charts.

Built for CS 313E (Elements of Software Design) at UT Austin.

------------------------------------------------------------------------------------

**Features**

Top 10 Rankings ranks all teams by ace rate using a merge sort

League Statistics shows mean, standard deviation, and range of serve accuracy across all teams

Best and Worst Teams automatically finds the highest and lowest performing teams

Interactive Team Search uses partial name matching so you can type "Asseco" to find "Asseco Resovia"

Per-Team Stats shows matches played, total aces, errors, serves, rolling average, trend, and league rank

Plotly Visualizations generates an interactive bar chart of the top 10 teams and a per-match trend line for any team you search

------------------------------------------------------------------------------------

**Data Structures and Algorithms**

Queue (FIFO) - Rolling window of last 5 match accuracies per team

Stack (LIFO) - Performance history for trend detection (improving/declining/stable)

Merge Sort - O(nlogn) ranking of all teams by ace rate

Recursive Variance - League-wide standard deviation calculation

------------------------------------------------------------------------------------

**Dataset**

PlusLiga Men's Volleyball 2008–2023
2,639 matches
23 unique teams
15 seasons
Source: Kaggle — PlusLiga Volleyball Dataset

------------------------------------------------------------------------------------

Installation

git clone https://github.com/Dxnton/volleyball-serve-analytics.git
cd volleyball-serve-analytics
pip3 install pandas plotly

Place the dataset CSV in the same folder as vball_serve.py before running

------------------------------------------------------------------------------------

Usage

When you run it the program will load all 2,639 matches, print the top 10 teams by ace rate, show the best and worst teams with their rolling averages and trends, display league wide statistics, open an interactive Plotly bar chart in your browser, then drop into a team search loop where you can look up any team by name.
Team search example:
Enter a team name to search (or 'quit' to exit): Asseco

  Asseco Resovia
  ============================================================
  Matches:      228
  Aces:         412
  Errors:       891
  Total Serves: 4976
  Accuracy:     0.083
  Rolling Avg:  0.081
  Trend:        stable
  League Rank:  #6 of 23
  ============================================================

  View match-by-match trend chart for this team? (y/n):

------------------------------------------------------------------------------------

**What I Learned
**
Building data structures from scratch makes you actually appreciate what libraries do for you. Rolling windows and stack based trend detection are pretty intuitive once you build them yourself. Making a CLI tool feel smooth takes more thought than the actual analysis. Connecting the data processing to visual output with Plotly was easier than I expected and way more satisfying than just printing tables.

------------------------------------------------------------------------------------

**Future Improvements
**
Add season by season filtering so you can compare a team across specific years
Expand beyond serve stats to include attack efficiency and blocking data
Export team reports as PDF summaries
