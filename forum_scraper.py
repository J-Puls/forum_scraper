##############################################################################################
# 
#     ___                                                                                     
#    / __)                                                                                    
#  _| |__ ___   ____ _   _ ____         ___  ____  ____ _____ ____  _____  ____ ____  _   _ 
# (_   __) _ \ / ___) | | |    \       /___)/ ___)/ ___|____ |  _ \| ___ |/ ___)  _ \| | | |
#   | | | |_| | |   | |_| | | | |_____|___ ( (___| |   / ___ | |_| | ____| |  _| |_| | |_| |
#   |_|  \___/|_|   |____/|_|_|_(_____|___/ \____)_|   \_____|  __/|_____)_| (_)  __/ \__  |
#                                                            |_|               |_|   (____/ 
# 
# forum_scraper.py
# Copywrite 2019 by Jeffrey Puls
# 
# This is a simple script used for scraping forum post data. In its current implementation,
# it has support for zilvia.net and rx7club.com. It outputs the contents of each forum thread
# into a .doc file with the filename set to the thread title.
# 
# To use the program, either:
#   - run "python forum_scraper.py" and follow the terminal prompts
# 
# OR
# 
#   - run "python forum_scraper.py" followed by arguments for origin_name (zilvia or rx7club), 
#       desired forum page url to be scraped (ex. 'https://zilvia.net/f/forumdisplay.php?f=97'),
#       and desired folder ID number (each time the program is run, it outputs the contents to a
#       new folder in the same directory as the script).
# 
# To run a demonstration execution without pulling live data, use "zilvia" for the forum name
# and "test" for the URL.
# 
# ********WARNING****************WARNING****************WARNING****************WARNING********
# 
# In its current implementation, this script will copy the contents of every forum thread it
# finds on the submitted URL! This can lead to very long run times, large file sizes, and 
# presents the possibility of crashing the forum server if abused. Please use this responsibly,
# avoiding pages with "sticky" threads without explicit permission, as these tend to be extremely
# large in size.
# 
# ********WARNING****************WARNING****************WARNING****************WARNING********
# 
##############################################################################################

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import io, sys, os

warning = """\n********************
WARNING!\n
While the act of scraping public data is not inherently illegal on its own, please be sure your
actions do not conflict with the forum's Terms of Service agreement. In addition, this program by
nature has the possibility to crash a weak server from the sheer number and speed at which it makes
requests. By running this tool, you accept full responsibility for your actions should you ignore
this warning.
\n********************\n
Press ctrl + c to exit."""

billboard = """
     ___                                                                                     
    / __)                                                                                    
  _| |__ ___   ____ _   _ ____         ___  ____  ____ _____ ____  _____  ____ ____  _   _ 
 (_   __) _ \ / ___) | | |    \       /___)/ ___)/ ___|____ |  _ \| ___ |/ ___)  _ \| | | |
   | | | |_| | |   | |_| | | | |_____|___ ( (___| |   / ___ | |_| | ____| |  _| |_| | |_| |
   |_|  \___/|_|   |____/|_|_|_(_____|___/ \____)_|   \_____|  __/|_____)_| (_)  __/ \__  |
                                                            |_|               |_|   (____/ 
"""

# prompt user for variable input if run without command line args
if len(sys.argv) < 2:
    print(billboard)
    print("""\nWelcome to forum_scraper.py!

To view a demo of this program's functionality, use 'zilvia' for the forum name and 'test' for the URL\n""")
    origin_name = input("Forum name (ex. zilvia, rx7club): ")
    if origin_name == "":
        print("\nForum name is required.")
        origin_name = input("Forum name (ex. zilvia, rx7club): ")

    print("\nEnter 'test' to view demo output.")
    forum_url = input("Forum URL: ")
    if forum_url == "":
        print("\nValid URL is required.")
        forum_url = input("Forum URL: ")
    elif forum_url.casefold() != "test":
        forum_url = 'http://phillippowers.com/redirects/get.php?file=' + forum_url

    folder_num = input("Desired folder ID: ")
    print(warning)
    input("\nPress ENTER to begin scraping")

# set variables if command line args used
else:
    try:
        origin_name = str(sys.argv[1])
        forum_url = str(sys.argv[2])
        forum_url = str(sys.argv[2])
        if forum_url != "test":
            forum_url = 'http://phillippowers.com/redirects/get.php?file=' + forum_url
        folder_num = str(sys.argv[3])
    except IndexError:
        print("Missing an argument (please use format 'origin_name url folder_num')")
        sys.exit()

def scrape_zilvia_forum(forum_url, folder_num):
    # if test is selected, pull information from local test file
    if forum_url == "test":
        with open("test_page.html", encoding="utf-8") as f:
            page_soup = soup(f, 'html.parser')
        test_file = True
        f.close()

    # if live URL, get and parse HTML to usable form
    else:
        myUrl = forum_url
        uClient = urlopen(myUrl)
        page_html = uClient.read()
        page_soup = soup(page_html, 'html.parser')

    # find all thread links on the page
    threads = page_soup.findAll('a', id=lambda x: x and x.startswith('thread_title_'))
    thread_data = []

    # if no threads are found, display message and exit program
    if len(threads) == 0:
        print("No threads Found. Please check the URL and try agian.")
        sys.exit()

    # if threads found, find thread title, OP username, and thread URL
    else:
        print(str(len(threads)) + ' threads found.')
        for thread in threads:
            tObj = {}
            tObj['title'] = thread.text
            tObj['op'] = thread.find_parent().find_next_sibling().text.replace('\n', '')
            tObj['url'] = thread['href'].split('t=', 1)
            thread_data.append(tObj) 

    # make new folder in current directory with user input folder ID number
    os.mkdir('zilvia_threads_' + folder_num)
    posts = 0
    
    # dispose of the source URL 
    if not test_file:
        uClient.close()

    # for each thread found, parse the post messages and dates
    for thread in thread_data:
        if not test_file:
            myUrl = 'http://phillippowers.com/redirects/get.php?file=https://zilvia.net/f/showthread.php?t='+ thread['url'][1]
            uClient = urlopen(myUrl)
            print('Scraping content at:\n' + str(myUrl.split("e=")[1]) + '\n')
            page_html = uClient.read()
            page_soup = soup(page_html, 'html.parser')
        else:
            with open(str(thread['url'][0]), encoding="utf-8") as f:
                page_soup = soup(f, 'html.parser')
            f.close()
        messages = page_soup.findAll('div', id=lambda x: x and x.startswith('post_message_'))
        dates = page_soup.findAll('table', id=lambda x: x and x.startswith('post'))

        # feedback to user
        print(str(len(messages)) + ' messages found')

        thread_messages = []

        # copy post messages and dates
        for m, message in enumerate(messages, start=0):
            mObj = {}
            mObj['date'] = dates[m].td.text.replace('\n', '')
            mObj['content'] = message.text.replace('\n\n', '\n').replace('\ud83e\udd26', '')
            thread_messages.append(mObj)
            posts+=1

        # replace any illegal filename characters in title
        illegal_chars = ["<", ">", ":", "/", "\\", "|", "?", "*", "\"", "\'", ",", "!"]
        safe_title = thread['title']
        safe_title = safe_title.replace("\n", " ").replace("\t", " ").replace(" ","_")
        for char in illegal_chars:
            safe_title = safe_title.replace(char, "#")

        # create new .doc file with the contents of the thread
        filename = 'zilvia_threads_' + str(folder_num) + '/' + safe_title + '.doc'
        with open(filename, "w", encoding="utf-8") as f:
            f.write('Thread title: ' + thread['title']+ '\n')
            f.write('Thread OP: ' + thread['op'] + '\n\n')
            for t in thread_messages:
                f.write('Date posted: ' + t['date'] + '\n' + t["content"] + '\n\n\n')
        f.close()
        
        # feedback to user & increment file number
        print('File saved successfully!')
        
    print('\n\nProcess finished.\nFound '+ str(len(threads))+' threads.\nSaved '+ str(posts) +' posts to doc files in /zilvia_threads_'+ folder_num +'.')

def scrape_rx7_forum(forum_url, folder_num):
    # abort if user tries to run test with rx7club
    if forum_url == "test":
        print('\nThe test function only works for forum name "zilvia"\n')
        sys.exit()

    myUrl = forum_url
    uClient = urlopen(myUrl)
    page_html = uClient.read()
    page_soup = soup(page_html, 'html.parser')

    threads = page_soup.findAll('a', id=lambda x: x and x.startswith('thread_title_'))
    thread_data = []
    if len(threads) == 0:
        print("No threads Found. Please check the URL and try agian.")
        sys.exit()
    else:
        print('Found ' + str(len(threads)) + ' threads.')
        for thread in threads:
            tObj = {}
            tObj['title'] = thread.text
            tObj['op'] = thread.find_parent().find_parent().find_next_sibling().span.text
            tObj['url'] = thread['href']
            thread_data.append(tObj)
            

    os.mkdir('rx7club_threads_' + folder_num)
    
    posts = 0
    uClient.close()
    for thread in thread_data:
        myUrl = 'http://phillippowers.com/redirects/get.php?file='+ thread['url']
        uClient = urlopen(myUrl)
        print('Scraping content at:\n' + str(myUrl.split("e=")[1]) + '\n')
        page_html = uClient.read()
        page_soup = soup(page_html, 'html.parser')

        messages = page_soup.findAll('div', id=lambda x: x and x.startswith('post_message_'))
        
        print(str(len(messages)) + ' messages found')

        thread_messages = []
        for m, message in enumerate(messages, start=0):
            mObj = {}
            # mObj['date'] = dates[m].td.text.replace('\n', '')
            mObj['content'] = message.text.replace('\n\n', '\n').replace('\ud83e\udd26', '')
            thread_messages.append(mObj)
            posts+=1

         # replace any illegal filename characters in title
        illegal_chars = ["<", ">", ":", "/", "\\", "|", "?", "*", "\"", "\'"]
        safe_title = thread['title']
        safe_title = safe_title.replace("\n", " ").replace("\t", " ").replace(" ","_")
        for char in illegal_chars:
            safe_title = safe_title.replace(char, "#")

        # create new Word doc with the contents of the thread
        filename = 'rx7club_threads_' + str(folder_num) + '/' + safe_title + '.doc'
        with open(filename, "w", encoding="utf-8") as f:
            f.write('Thread title: ' + thread['title']+ '\n')
            f.write('Thread OP: ' + thread['op'] + '\n\n')
            for t in thread_messages:
                f.write('Date posted: ' + '\n' + t["content"] + '\n\n\n')
        f.close()
        print('File saved successfully!')
    print('\n\nProcess finished.\nFound '+ str(len(threads))+' threads.\nSaved '+ str(posts) +' posts to doc files in /rx7club_threads_'+ folder_num +'.')

# execute script based on chosen origin
if origin_name.casefold() == "zilvia":
    try: 
        scrape_zilvia_forum(forum_url, folder_num)
    except Exception as e:
        print("Error! " + str(e))
        sys.exit()
    
elif origin_name.casefold() == "rx7club":
    try: 
        scrape_rx7_forum(forum_url, folder_num)
    except Exception as e:
        print("Error! " + str(e))
        sys.exit()


