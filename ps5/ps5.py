# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        """
        globally unique identifier (GUID) - a string
        title - a string
        description - a string
        link to more content - a string
        pubdate - a datetime        
        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate
    


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    '''
    take in a trigger phrase as an argument
    '''
    def __init__(self, phrase):
        self.phrase = phrase
    
    def is_phrase_in(self, text):
        '''
        determine if phrase is in the text
        '''
        #change phrase into lowercase
        phrase = self.phrase.lower()
        
        #manipulate text to be in lowercase and without punctuation or extra spaces
        text = text.lower()
        for char in text:
            if char in string.punctuation:
                text = text.replace(char, ' ')#remove punctuation

        li = text.split()#put words in s into a list
        phrase_len = len(phrase.split())
        res = False
        for i in range(len(li)):
            check = ' '.join(li[i: i + phrase_len])
            if check == phrase:
                res = True
                break
        return res
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        '''
        story is a NewsStory object
        '''
        return self.is_phrase_in(story.title)
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        '''
        story is a NewsStory object
        '''
        return self.is_phrase_in(story.description)
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time_string):
        from datetime import datetime
        self.time =datetime.strptime(time_string, '%d %b %Y %H:%M:%S')
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, time_string):
        TimeTrigger.__init__(self, time_string)
        
    def evaluate(self, story):
        return story.pubdate < self.time

class AfterTrigger(TimeTrigger):
    def __init__(self, time_string):
        TimeTrigger.__init__(self, time_string)
        
    def evaluate(self, story):
        return story.pubdate > self.time
# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
        
    def evaluate(self, story):
        return not self.trigger.evaluate(story)
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        
    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        
    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    filtered = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered.append(story)
        continue
   
    stories = filtered
    return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_string_dict = {'TITLE': TitleTrigger, 'DESCRIPTION': DescriptionTrigger, 
                           'NOT': NotTrigger, 'AND': AndTrigger, 
                           'OR': OrTrigger, 'BEFORE': BeforeTrigger,
                           'AFTER': AfterTrigger}
    trigger_dict = {}
    trigger_list = []
    for item in lines:
        li = item.split(',')
        if li[0] != 'ADD':
            if len(li) == 3:
                trigger_dict[li[0]] = trigger_string_dict[li[1]](li[2])
            else:
                trigger_dict[li[0]] = trigger_string_dict[li[1]](trigger_dict[li[2]], 
                                                                 trigger_dict[li[3]])
        else:
            for i in range(1, len(li)):
                trigger_list.append(trigger_dict[li[i]])
    
    return trigger_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Biden")
        t2 = DescriptionTrigger("Tax")
        t3 = DescriptionTrigger("increase")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

