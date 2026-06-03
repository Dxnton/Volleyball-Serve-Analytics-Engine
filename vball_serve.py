#  File: vball_serve_enhanced.py

#  Description: Volleyball Serve Statistics Analyzer for PlusLiga dataset. analyzes serving performance across 15 years of professional 
#  volleyball matches using custom data structures and algorithms.

#  Student Name: Denton Le

#  Student UT EID: dkl782

#  Student Name: Samuel Li 

#  Student UT EID: scl2567

#  Course Name: CS 313E

#  Unique Number: 54595

#  Date Created: 11/14/2025

#  Date Last Modified: 11/14/2025
     
"""
Volleyball Serve Statistics Analyzer
Analyzes PlusLiga dataset (2008-2023) using Queue, Stack, merge sort, and recursion.
"""
import csv
import pandas as pd
import plotly.graph_objects as go

# -------------------------------
# Data Structures
# -------------------------------
class Queue:
    """FIFO queue for rolling window statistics."""
    def __init__(self, max_size=5):
        self.items = []
        self.max_size = max_size

    def enqueue(self, item):
        if len(self.items) >= self.max_size:
            self.items.pop(0)
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0) if self.items else None

    def get_average(self):
        return sum(self.items) / len(self.items) if self.items else 0.0

    def size(self):
        return len(self.items)


class Stack:
    """LIFO stack for performance history tracking."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None

    def get_trend(self):
        if len(self.items) < 2:
            return "insufficient data"
        recent = self.items[-3:] if len(self.items) >= 3 else self.items
        increases = sum(1 for i in range(1, len(recent)) if recent[i] > recent[i-1])
        decreases = sum(1 for i in range(1, len(recent)) if recent[i] < recent[i-1])
        if increases > decreases:
            return "improving"
        elif decreases > increases:
            return "declining"
        return "stable"

    def size(self):
        return len(self.items)


# -------------------------------
# File I/O and Parsing
# -------------------------------
def read_csv(filename):
    """Read CSV file and return lines (kept for compatibility)."""
    try:
        with open(filename, "r", encoding='utf-8') as f:
            return list(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []


def parse_data(filename):
    """Load and parse CSV using pandas, returning match records as a list.
    Pandas handles column selection and type conversion cleanly,
    feeding into our custom data structures for analysis.
    """
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

    records = []
    for _, row in df.iterrows():
        try:
            records.append([
                str(row['Date']).strip(),           # date
                str(row['Team_1']).strip(),          # team1
                int(float(row['T1_Srv_Ace'])),       # t1 ace
                int(float(row['T1_Srv_Err'])),       # t1 err
                int(float(row['T1_Srv_Sum'])),       # t1 sum
                str(row['Team_2']).strip(),          # team2
                int(float(row['T2_Srv_Ace'])),       # t2 ace
                int(float(row['T2_Srv_Err'])),       # t2 err
                int(float(row['T2_Srv_Sum'])),       # t2 sum
            ])
        except (ValueError, KeyError):
            continue
    return records


def build_team_stats(records):
    """Aggregate statistics for each team."""
    team_stats = {}
    
    for r in records:
        for team, ace, err, serves in [(r[1], r[2], r[3], r[4]), (r[5], r[6], r[7], r[8])]:
            if team not in team_stats:
                team_stats[team] = {
                    'aces': 0, 'errors': 0, 'serves': 0, 'matches': 0,
                    'queue': Queue(5), 'stack': Stack()
                }
            
            team_stats[team]['aces'] += ace
            team_stats[team]['errors'] += err
            team_stats[team]['serves'] += serves
            team_stats[team]['matches'] += 1
            
            accuracy = (ace - err) / serves if serves > 0 else 0.0
            team_stats[team]['queue'].enqueue(accuracy)
            team_stats[team]['stack'].push(accuracy)
    
    return team_stats


# -------------------------------
# Algorithms
# -------------------------------
def merge_sort_teams(team_list):
    """Sort teams by accuracy using merge sort (O(n log n))."""
    if len(team_list) <= 1:
        return team_list
    
    mid = len(team_list) // 2
    left = merge_sort_teams(team_list[:mid])
    right = merge_sort_teams(team_list[mid:])
    
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] >= right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def calculate_variance_recursive(values, mean, index=0):
    """Recursively calculate variance."""
    if index >= len(values):
        return 0.0
    return (values[index] - mean) ** 2 + calculate_variance_recursive(values, mean, index + 1)


# -------------------------------
# Analysis
# -------------------------------
def compute_averages(team_stats):
    """Calculate overall accuracy for each team."""
    return {team: stats['aces'] / stats['serves']
            if stats['serves'] > 0 else 0.0
            for team, stats in team_stats.items()}


def find_best_worst(averages):
    """Find teams with highest and lowest accuracy."""
    if not averages:
        return None, None
    return max(averages, key=averages.get), min(averages, key=averages.get)


# -------------------------------
# Visualization
# -------------------------------
def plot_top_teams(sorted_teams, n=10):
    """Bar chart of top N teams by serve accuracy.
    sorted_teams is already sorted highest -> lowest from merge_sort_teams().
    We reverse it so the best team appears at the top of the horizontal bar chart.
    """
    top = sorted_teams[:n]
    teams = [t for t, _ in reversed(top)]   # team names (reversed for readability)
    accs  = [a for _, a in reversed(top)]   # accuracy values

    fig = go.Figure(go.Bar(
        x=accs,
        y=teams,
        orientation='h',                     # horizontal bars
        marker_color='steelblue',
        text=[f"{a:.3f}" for a in accs],     # show value on each bar
        textposition='outside'
    ))
    fig.update_layout(
        title=f"Top {n} Teams by Ace Rate (PlusLiga 2008–2023)",
        xaxis_title="Ace Rate  (aces / total serves)",
        yaxis_title="Team",
        margin=dict(l=200),
        height=400
    )
    fig.show()   # opens in your default browser as an interactive HTML page


def plot_team_trend(team, records):
    """Line chart of a single team's serve accuracy match by match over time.
    records is the raw list built by parse_data(); we filter to rows involving
    the requested team and compute per-match accuracy in chronological order.
    """
    dates   = []
    accs    = []

    for r in records:
        # r layout: [date, team1, t1_ace, t1_err, t1_sum, team2, t2_ace, t2_err, t2_sum]
        if r[1] == team:
            ace, err, serves = r[2], r[3], r[4]
        elif r[5] == team:
            ace, err, serves = r[6], r[7], r[8]
        else:
            continue

        if serves > 0:
            dates.append(r[0])
            accs.append(ace / serves)

    if not dates:
        print(f"  No match data found for '{team}'.")
        return

    fig = go.Figure(go.Scatter(
        x=list(range(1, len(dates) + 1)),   # match number on x-axis
        y=accs,
        mode='lines+markers',               # line with dots at each match
        marker=dict(size=5),
        line=dict(color='steelblue'),
        hovertext=dates,                    # hovering shows the actual date
        hoverinfo='text+y'
    ))
    fig.update_layout(
        title=f"{team} — Ace Rate Per Match",
        xaxis_title="Match Number (chronological)",
        yaxis_title="Ace Rate (aces / total serves)",
        height=400
    )
    fig.show()


# -------------------------------
# Main Program
# -------------------------------
def main():
    filename = "Mens-Volleyball-PlusLiga-2008-2023.csv"
    
    print("\n" + "="*60)
    print(" VOLLEYBALL SERVE STATISTICS ANALYZER")
    print("="*60)
    
    lines = read_csv(filename)
    if not lines:
        return
    
    records = parse_data(filename)
    print(f"\nDataset: {filename}")
    print(f"Matches processed: {len(records)}")
    
    team_stats = build_team_stats(records)
    print(f"Teams analyzed: {len(team_stats)}")
    
    averages = compute_averages(team_stats)
    sorted_teams = merge_sort_teams([(t, a) for t, a in averages.items()])
    best, worst = find_best_worst(averages)
    
    # Display top teams
    print("\n" + "="*60)
    print(" TOP 10 TEAMS BY SERVE ACCURACY")
    print("="*60)
    print(f"{'Rank':<6} {'Team':<30} {'Accuracy':<10} {'Rolling':<10} {'Trend'}")
    print("-"*60)
    for rank, (team, acc) in enumerate(sorted_teams[:10], 1):
        rolling = team_stats[team]['queue'].get_average()
        trend = team_stats[team]['stack'].get_trend()
        print(f"{rank:<6} {team:<30} {acc:>6.3f}    {rolling:>6.3f}    {trend}")
    
    # Display best and worst
    print("\n" + "="*60)
    print(" BEST AND WORST TEAMS")
    print("="*60)
    if best and worst:
        print(f"\n🏆 Best:  {best} (Accuracy: {averages[best]:.3f}, Matches: {team_stats[best]['matches']})")
        print(f"   Rolling Avg: {team_stats[best]['queue'].get_average():.3f}, Trend: {team_stats[best]['stack'].get_trend()}")
        print(f"\n📉 Worst: {worst} (Accuracy: {averages[worst]:.3f}, Matches: {team_stats[worst]['matches']})")
        print(f"   Rolling Avg: {team_stats[worst]['queue'].get_average():.3f}, Trend: {team_stats[worst]['stack'].get_trend()}")
    
    # League statistics
    all_accuracies = list(averages.values())
    mean = sum(all_accuracies) / len(all_accuracies)
    variance = calculate_variance_recursive(all_accuracies, mean) / len(all_accuracies)
    
    print("\n" + "="*60)
    print(" LEAGUE STATISTICS")
    print("="*60)
    print(f"Mean Accuracy: {mean:.4f}")
    print(f"Std Deviation: {variance**0.5:.4f}")
    print(f"Range: {min(all_accuracies):.4f} to {max(all_accuracies):.4f}")
    print("\n" + "="*60 + "\n")

    # Auto-show bar chart of top 10 teams
    plot_top_teams(sorted_teams)

    # Interactive team search
    print(" TEAM SEARCH")
    print("="*60)
    while True:
        query = input("\nEnter a team name to search (or 'quit' to exit): ").strip()
        if query.lower() == 'quit':
            print("\nGoodbye!\n")
            break

        # exact match first, then partial
        matches = [t for t in team_stats if query.lower() in t.lower()]

        if not matches:
            print(f"  No teams found matching '{query}'. Try a partial name.")
            continue

        if len(matches) > 1:
            print(f"  Multiple matches found:")
            for m in matches:
                print(f"    - {m}")
            print(f"  Showing first match: {matches[0]}")

        team = matches[0]
        acc = averages[team]
        rolling = team_stats[team]['queue'].get_average()
        trend = team_stats[team]['stack'].get_trend()
        rank = next(i+1 for i, (t, _) in enumerate(sorted_teams) if t == team)

        print(f"\n{'='*60}")
        print(f"  {team}")
        print(f"{'='*60}")
        print(f"  Matches:      {team_stats[team]['matches']}")
        print(f"  Aces:         {team_stats[team]['aces']}")
        print(f"  Errors:       {team_stats[team]['errors']}")
        print(f"  Total Serves: {team_stats[team]['serves']}")
        print(f"  Accuracy:     {acc:.3f}")
        print(f"  Rolling Avg:  {rolling:.3f}")
        print(f"  Trend:        {trend}")
        print(f"  League Rank:  #{rank} of {len(sorted_teams)}")
        print(f"{'='*60}")

        # Offer trend chart for the searched team
        chart = input("\n  View match-by-match trend chart for this team? (y/n): ").strip().lower()
        if chart == 'y':
            plot_team_trend(team, records)


# -------------------------------
# Test Cases
# -------------------------------
def run_tests():
    """Simple test suite - basic functionality checks."""
    print("\n" + "="*60)
    print(" RUNNING TEST CASES")
    print("="*60)
    
    # TEST 1: Queue basic operations
    print("\n[1/3] Testing Queue...")
    q = Queue(3)
    q.enqueue(0.1)
    q.enqueue(0.2)
    q.enqueue(0.3)
    
    if q.size() == 3:
        print("  ✓ Queue size is correct (3)")
    else:
        print("  ✗ Queue size is wrong")
    
    avg = q.get_average()
    expected = 0.2
    if abs(avg - expected) < 0.01:  # Allow small difference for floating point
        print("  ✓ Queue average is correct (0.2)")
    else:
        print(f"  ✗ Queue average is wrong (got {avg})")
    
    # TEST 2: Stack basic operations
    print("\n[2/3] Testing Stack...")
    s = Stack()
    s.push(0.05)
    s.push(0.10)
    s.push(0.08)
    
    if s.size() == 3:
        print("  ✓ Stack size is correct (3)")
    else:
        print("  ✗ Stack size is wrong")
    
    top = s.pop()
    if top == 0.08:
        print("  ✓ Stack pop is correct (0.08)")
    else:
        print(f"  ✗ Stack pop is wrong (got {top})")
    
    # TEST 3: Sorting
    print("\n[3/3] Testing Merge Sort...")
    teams = [("Team A", 0.05), ("Team B", 0.12), ("Team C", 0.03)]
    sorted_teams = merge_sort_teams(teams)
    
    if sorted_teams[0][0] == "Team B":
        print("  ✓ First team is correct (Team B with highest accuracy)")
    else:
        print(f"  ✗ First team is wrong (got {sorted_teams[0][0]})")
    
    if sorted_teams[2][0] == "Team C":
        print("  ✓ Last team is correct (Team C with lowest accuracy)")
    else:
        print(f"  ✗ Last team is wrong (got {sorted_teams[2][0]})")
    
    print("\n" + "="*60)
    print(" Tests complete - check results above")
    print("="*60 + "\n")


# -------------------------------
# Run Program
# -------------------------------
if __name__ == "__main__":
    import os
    if os.environ.get('RUN_TESTS') == '1':
        run_tests()
    else:
        main()