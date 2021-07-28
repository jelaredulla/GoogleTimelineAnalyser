# GoogleTimelineAnalyser

It's tax time and you need to know how many hours you worked from home, huh? Except actually, working from home is very fun, so maybe it's easier to find out when you were in the office instead. After all, there's no guarantee that you were working from home, instead of sleeping from home.

1. Get your Google timeline data from Google. Go to https://timeline.google.com and click the gear icon for settings. Select the option "Download a copy of all your data", then follow the prompts to get your timeline.
2. Install Python 3 from https://www.python.org/downloads/. Make sure to check the option "Add Python 3.x to PATH", or add it yourself after the installation.
3. Run the script to analyse your timeline data:
```
python main.py <google_data_directory> [--tax_year | --output_dir]
```
