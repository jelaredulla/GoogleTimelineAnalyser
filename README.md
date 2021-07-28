# GoogleTimelineAnalyser

It's tax time and you need to know how many hours you worked from home, huh? Except actually, working from home is very fun, so maybe it's easier to find out when you were in the office instead. After all, there's no guarantee that you were working from home, instead of sleeping from home.

1. Get your Google timeline data from Google. Go to https://timeline.google.com and click the gear icon for settings. Select the option "Download a copy of all your data", then follow the prompts to get your timeline.
2. Install Python 3 from https://www.python.org/downloads/. Make sure to check the option "Add Python 3.x to PATH", or add it yourself after the installation.
3. Use `pip` to install `pandas`, a required Python library that unfortunately isn't a Python 3 built-in. Open a command prompt window and type in:
 ```pip install pandas```   
4. Download the script `main.py` from this repo. Consider double-checking that the source code is benign, and doesn't send your data to one of my secret servers. The other option is to blindly trust this script you found on the internet.
5. Run the script to analyse your timeline data.
  In a command prompt window, navigate to the same directory as `main.py`:
  ```
  cd "C:\Users\<user.name>\Downloads\GoogleTimelineAnalyser"
  ```
  Then, run the main script using Python:
  ```
  python main.py <google_data_directory> [--tax_year | --output_dir]
  ```
  e.g.
  ```
  python main.py "C:\Users\<user.name>\Downloads\takeout-20210717T103515Z-001\Takeout" --tax_year 2020 --output_dir "C:\Users\<user.name>\Documents\Timeline Summary"
  Output directory does not exist, so making it...
  Parsing file "2020_JULY.json"...
  Parsing file "2020_AUGUST.json"...
  Parsing file "2020_SEPTEMBER.json"...
  Parsing file "2020_OCTOBER.json"...
  Parsing file "2020_NOVEMBER.json"...
  Parsing file "2020_DECEMBER.json"...
  Parsing file "2021_JANUARY.json"...
  Parsing file "2021_FEBRUARY.json"...
  Parsing file "2021_MARCH.json"...
  Parsing file "2021_APRIL.json"...
  Parsing file "2021_MAY.json"...
  Parsing file "2021_JUNE.json"...



  Days in the office: <xx>
  Total time in the office: <hhh>:<mm>
  ```
