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
  cd <timeline_analyser_directory>
  ```
  e.g.
  ```
  cd "C:\Users\<user.name>\Downloads\GoogleTimelineAnalyser"
  ```
  Then, run the main script using Python:
  ```
  python main.py "<Google Semantic Location History directory>"
  
  # optionally specify the tax year as well
  python main.py "<Google Semantic Location History directory>" --tax_year 2018
  
  # optionally specify the output directory
  python main.py "<Google Semantic Location History directory>" --output_dir "<path to output directory>"
  ```
  e.g.
  ```
  python main.py "C:\Users\jelar\Downloads\takeout-20210717T103515Z-001\Takeout\Location History\Semantic Location History"
  
  Input directory: C:\Users\jelar\Downloads\takeout-20210717T103515Z-001\Takeout\Location History\Semantic Location History
  
  Analysing timeline for the 2020 tax_year...
  
  Summary data will be written to: C:\Users\jelar\Documents\git\GoogleTimelineAnalyser\GoogleTimelineAnalyser Output
  
  Attempting to parse file "2020_JULY.json" - file exists so parsing it...
  Attempting to parse file "2020_AUGUST.json" - file exists so parsing it...
  Attempting to parse file "2020_SEPTEMBER.json" - file exists so parsing it...
  Attempting to parse file "2020_OCTOBER.json" - file exists so parsing it...
  Attempting to parse file "2020_NOVEMBER.json" - file exists so parsing it...
  Attempting to parse file "2020_DECEMBER.json" - file exists so parsing it...
  Attempting to parse file "2021_JANUARY.json" - file exists so parsing it...
  Attempting to parse file "2021_FEBRUARY.json" - file exists so parsing it...
  Attempting to parse file "2021_MARCH.json" - file exists so parsing it...
  Attempting to parse file "2021_APRIL.json" - file exists so parsing it...
  Attempting to parse file "2021_MAY.json" - file exists so parsing it...
  Attempting to parse file "2021_JUNE.json" - file exists so parsing it...
  
  Days in the office: <xx>
  Total time in the office: <hhh>:<mm>
  ```
  
  
  Note: this script assumes you've tagged your office location as "Work" in your Google Maps profile. It filters the timeline activity data for "place visits" with semantic type "TYPE_WORK". If you have multiple offices / haven't tagged your place(s) of work as Work, you will need to tweak the script. I suggest modifying `get_office_days` to filter by address instead, for example. 
