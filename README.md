# Volleyball-Serve-Analytics-Engine

CLI analytics tool analyzing 2,639 professional volleyball matches using custom data structures, merge sort, and Plotly visualizations.
A command-line analytics tool that analyzes 15 years of professional volleyball serve data from the Polish PlusLiga (2008–2023). Built from scratch using custom data structures and algorithms — no sklearn, no heavy ML libraries.

------------------------------------------------------------------------------------

Overview
This project processes 2,639 matches across 23 professional teams, ranking teams by ace rate, detecting performance trends, and letting you interactively explore any team's serve statistics with visual Plotly charts.
Built for CS 313E (Elements of Software Design) at UT Austin.

------------------------------------------------------------------------------------

Features

Top 10 Rankings — ranks all teams by ace rate using a custom merge sort implementation
League Statistics — mean, standard deviation, and range of serve accuracy across all teams
Best & Worst Teams — automatically surfaces the highest and lowest performing teams
Interactive Team Search — partial name matching; type "Asseco" to find "Asseco Resovia"
Per-Team Stats — matches played, total aces, errors, serves, rolling average, trend, and league rank
Plotly Visualizations — interactive bar chart of top 10 teams and a per-match trend line chart for any searched team

------------------------------------------------------------------------------------

Data Structures & Algorithms

This project was intentionally built without pandas for core logic to demonstrate understanding of underlying data structures:
ComponentPurposeQueue (FIFO)Rolling window of last 5 match accuracies per teamStack (LIFO)Performance history for trend detection (improving / declining / stable)Merge SortO(n log n) ranking of all teams by ace rateRecursive VarianceLeague-wide standard deviation calculation

------------------------------------------------------------------------------------

Technologies

Python 3
Pandas — CSV loading and column parsing
Plotly — interactive visualizations

------------------------------------------------------------------------------------

Dataset
PlusLiga Men's Volleyball 2008–2023

2,639 matches
23 unique teams
15 seasons

Source: Kaggle — PlusLiga Volleyball Dataset

------------------------------------------------------------------------------------

Installation
bash# Clone the repo
git clone https://github.com/Dxnton/volleyball-serve-analytics.git
cd volleyball-serve-analytics

# Install dependencies
pip3 install pandas plotly

# Place the dataset CSV in the same folder as vball_serve.py

------------------------------------------------------------------------------------

Usage
bashpython3 vball_serve.py

The program will:

Load and process all 2,639 matches
Print the top 10 teams by ace rate
Show best and worst teams with rolling averages and trends
Display league-wide statistics
Open an interactive Plotly bar chart in your browser
Drop into an interactive team search loop

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

------------------------------------------------------------------------------------

  View match-by-match trend chart for this team? (y/n):

Project Structure
volleyball-serve-analytics/
├── vball_serve.py                    # Main program
├── Mens-Volleyball-PlusLiga-2008-2023.csv   # Dataset
└── README.md

------------------------------------------------------------------------------------

What I Learned

Implementing core data structures (Queue, Stack) from scratch rather than relying on built-in libraries
How rolling windows and stack-based trend detection work at a low level
Building interactive CLI tools with clean user experience
Connecting backend data processing to frontend visualizations with Plotly

------------------------------------------------------------------------------------

Future Improvements

Add season-by-season filtering so you can compare a team across specific years
Expand beyond serve stats to include attack efficiency and blocking data
Export team reports as PDF summaries
