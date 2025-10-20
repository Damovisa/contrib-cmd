#!/usr/bin/env python3
"""
GitHub Contribution Graph ASCII Viewer
Fetches and displays a user's GitHub contribution graph in ASCII art.
"""

import sys
import json
import subprocess
from datetime import datetime


# ASCII characters with increasing density for levels 0-4
DENSITY_CHARS = ['·', '░', '▒', '▓', '█']

# ANSI color codes for GitHub-style green contribution levels
COLOR_LEVELS = [
    '\033[38;5;236m',  # Level 0: Dark gray (no contributions)
    '\033[38;5;22m',   # Level 1: Dark green
    '\033[38;5;28m',   # Level 2: Medium-dark green
    '\033[38;5;34m',   # Level 3: Medium-bright green
    '\033[38;5;40m',   # Level 4: Bright green
]
COLOR_RESET = '\033[0m'


def fetch_contributions(username):
    """Fetch contribution data from GitHub for the given username."""
    url = f"https://github.com/{username}.contribs"
    
    try:
        result = subprocess.run(
            ['curl', '-s', url],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"Error: Failed to fetch data (curl exit code {result.returncode})", file=sys.stderr)
            return None
        
        data = json.loads(result.stdout)
        
        # Check if the response contains an error
        if 'error' in data:
            print(f"Error: {data['error']} - User '{username}' may not exist.", file=sys.stderr)
            return None
        
        return data
        
    except subprocess.TimeoutExpired:
        print("Error: Request timed out.", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response - {e}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("Error: curl not found. Please install curl.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def render_contribution_graph(data):
    """Render the contribution graph as ASCII art."""
    weeks = data.get('weeks', [])
    months = data.get('months', [])
    
    if not weeks:
        print("No contribution data available.")
        return
    
    # Print header info
    print(f"\n{data.get('from', 'N/A')} to {data.get('to', 'N/A')}")
    print(f"Total contributions: {data.get('total_contributions', 0)}")
    print()
    
    # Print month labels
    month_line = "     "  # Offset for weekday labels
    current_pos = 0
    for month_info in months:
        month_name = month_info['month']
        total_weeks = month_info['total_weeks']
        # Each week is 2 chars wide (char + space)
        month_label = datetime.strptime(month_name, "%Y-%m").strftime("%b")
        
        if total_weeks >= 2:
            month_line += month_label[:3].ljust(total_weeks * 2)
        current_pos += total_weeks * 2
    
    print(month_line)
    print()
    
    # Weekday labels
    weekday_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    
    # Build the graph row by row (one row per weekday)
    for weekday in range(7):
        # Only show labels for Mon, Wed, Fri to reduce clutter
        if weekday in [1, 3, 5]:
            row = f"{weekday_labels[weekday]} "
        else:
            row = "    "
        
        for week in weeks:
            contribution_days = week.get('contribution_days', [])
            # Find the day for this weekday
            day_found = False
            for day in contribution_days:
                if day['weekday'] == weekday:
                    level = day['level']
                    row += COLOR_LEVELS[level] + DENSITY_CHARS[level] + COLOR_RESET + ' '
                    day_found = True
                    break
            
            if not day_found:
                row += '  '  # Empty space for missing days
        
        print(row)
    
    print()
    # Print legend
    print("Legend: ", end="")
    for i, char in enumerate(DENSITY_CHARS):
        print(f"{COLOR_LEVELS[i]}{char}{COLOR_RESET}={i}", end=" ")
    print("(contribution level)")
    print()


def get_username():
    """Prompt user for GitHub username."""
    try:
        username = input("Enter GitHub username: ").strip()
        if not username:
            print("Error: Username cannot be empty.", file=sys.stderr)
            return None
        return username
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.", file=sys.stderr)
        return None


def main():
    """Main entry point for the CLI application."""
    username = None
    
    # Check if username provided as command-line argument
    if len(sys.argv) > 1:
        username = sys.argv[1].strip()
    else:
        # Prompt for username
        username = get_username()
    
    if not username:
        sys.exit(1)
    
    print(f"Fetching contribution data for '{username}'...")
    data = fetch_contributions(username)
    
    if data:
        render_contribution_graph(data)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
