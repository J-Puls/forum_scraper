# forum_scraper
This is a simple script used for scraping forum post data. In its current implementation, it has support for zilvia.net and rx7club.com. It outputs the contents of each forum thread into a .doc file with the filename set to the thread title.

# Usage
To run a demonstration execution without pulling live data, use `python forum_scraper.py zilvia test 1` or use "zilvia" for the forum name and "test" for the URL.
To use the program, either:
   - run `python forum_scraper.py` and follow the terminal prompts

OR

  - run `python forum_scraper.py` followed by arguments for origin_name (zilvia or rx7club), desired forum page url to be scraped (ex. 'https://zilvia.net/f/forumdisplay.php?f=97'), and desired folder ID number (each time the program is run, it outputs the contents to a new folder in the same directory as the script file). 
  
    ex. `python forum_scraper.py zilvia https://zilvia.net/f/forumdisplay.php?f=97 1`

# WARNING!

In its current implementation, this script will copy the contents of every forum thread it finds on the submitted URL! This can lead to very long run times, large file sizes, and  presents the possibility of crashing the forum server if abused. Please use this responsibly, avoiding pages with "sticky" threads without explicit permission, as these tend to be extremely large in size.


