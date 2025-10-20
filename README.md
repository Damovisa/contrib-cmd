# GitHub Contribution Graph ASCII Viewer

A command-line tool that fetches and displays a GitHub user's contribution graph in ASCII art.

## Features

- Fetches contribution data from GitHub's API
- Displays contributions in a visual ASCII graph with density-based characters
- Shows month labels and weekday indicators
- Displays total contributions and date range
- Supports both command-line argument and interactive prompt modes

## Requirements

- Python 3.6 or higher
- `curl` command-line tool (usually pre-installed on macOS and Linux)

## Usage

### With command-line argument:

```bash
./github-contrib.py <username>
```

Example:
```bash
./github-contrib.py damovisa
```

### Interactive mode:

```bash
./github-contrib.py
```

The script will prompt you to enter a GitHub username.

## ASCII Representation

The contribution graph uses characters with increasing density to represent different contribution levels:

- ` ` (space) = Level 0 (no contributions)
- `░` = Level 1 (low contributions)
- `▒` = Level 2 (moderate contributions)
- `▓` = Level 3 (high contributions)
- `█` = Level 4 (very high contributions)

## Example Output

```
Fetching contribution data for 'damovisa'...

2024-10-20 to 2025-10-20
Total contributions: 299

     Oct Nov     Dec       Jan     Feb     Mar       Apr     May     Jun       Jul     Aug       Sep     Oct   

                                              ░                 █                                           ▒ 
Mon         ░                   ░         ░   ░                 ░                                     ░     █ 
    ▒                                   ░ ░   ░ ░     ░   ▓ ▓   ░         ░   ░                         ▓     
Wed ░                       ░   ░ ░       ░                   ░     ░     ░                   ░   ░     ░ ░   
    █                       ░               ░   ▒     █ ▒   █ ░       ░   █                       ░     ░     
Fri ▓                           ░           ░           ▒   ▓ ▒                 ░                       ░     
    ░                                       ░             ▓ █ ░                                               

Legend:  =0 ░=1 ▒=2 ▓=3 █=4 (contribution level)
```

## Error Handling

The tool provides helpful error messages for common issues:

- User not found
- Network connectivity issues
- Invalid JSON responses
- Missing dependencies (curl)

## Installation

1. Clone or download this repository
2. Make the script executable:
   ```bash
   chmod +x github-contrib.py
   ```
3. Run the script as shown in the Usage section

## License

This tool is provided as-is for educational and personal use.
