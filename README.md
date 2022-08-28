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
  python main.py
  ```
  Follow the prompts, e.g.
  ```
  Tax year (e.g. 2021): 2021

  Path to Google location history (should end in "Semantic Location History"): C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History

  Directory where results will be written (defaults to "C:\Users\jelar\Documents\git\GoogleTimelineAnalyser\GoogleTimelineAnalyser Output"):
  Summary data will be written to: C:\Users\jelar\Documents\git\GoogleTimelineAnalyser\GoogleTimelineAnalyser Output

  Enter substring for home (e.g. suburb or postcode): Homebush
  Addresses with any of the substrings ['Homebush'] will be identified as home
  If these are all the substrings to use, hit Enter to continue
  Enter substring for home (e.g. suburb or postcode): 2140
  Addresses with any of the substrings ['Homebush', '2140'] will be identified as home
  If these are all the substrings to use, hit Enter to continue
  Enter substring for home (e.g. suburb or postcode):

  Enter substring for the office (e.g. suburb or postcode): Sydney
  Addresses with any of the substrings ['Sydney'] will be identified as the office
  If these are all the substrings to use, hit Enter to continue
  Enter substring for the office (e.g. suburb or postcode): 2000
  Addresses with any of the substrings ['Sydney', '2000'] will be identified as the office
  If these are all the substrings to use, hit Enter to continue
  Enter substring for the office (e.g. suburb or postcode):

  What time do you start work usually (HH:MM)? 08:30
  What time do you end work usually (HH:MM)? 17:30

  What timezone are you in (defaults to "Australia/Sydney")?
  Using timezone: Australia/Sydney

  Analysing timeline for the 2021-2022 tax_year...

  Attempting to parse file "2021_JULY.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2021\2021_JULY.json")    - file exists so parsing it...
  Attempting to parse file "2021_AUGUST.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2021\2021_AUGUST.json")    - file exists so parsing it...
  Attempting to parse file "2021_SEPTEMBER.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2021\2021_SEPTEMBER.json")    - file exists so parsing it...
  Attempting to parse file "2021_OCTOBER.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2021\2021_OCTOBER.json")    - file exists so parsing it...
  Attempting to parse file "2021_NOVEMBER.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2021\2021_NOVEMBER.json")    - file exists so parsing it...
  Attempting to parse file "2021_DECEMBER.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2021\2021_DECEMBER.json")    - file exists so parsing it...
  Attempting to parse file "2022_JANUARY.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2022\2022_JANUARY.json")    - file exists so parsing it...
  Attempting to parse file "2022_FEBRUARY.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2022\2022_FEBRUARY.json")    - file exists so parsing it...
  Attempting to parse file "2022_MARCH.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2022\2022_MARCH.json")    - file exists so parsing it...
  Attempting to parse file "2022_APRIL.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2022\2022_APRIL.json")    - file exists so parsing it...
  Attempting to parse file "2022_MAY.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2022\2022_MAY.json")    - file exists so parsing it...
  Attempting to parse file "2022_JUNE.json" (full path is "C:\Users\jelar\Downloads\takeout-20220821T020506Z-001\Takeout\Location History\Semantic Location History\2022\2022_JUNE.json")    - not found.

  There were 261 work days in the 2021-2022 tax year
  There were <xx> work dates with no location data whatsoever

  Spent <xxx> days in the office
  Spent <xxx> days at home on working days
  Spent <xxx> days elsewhere on working days

  NOTE: this does not take into account public holidays or your days on leave
  ```
