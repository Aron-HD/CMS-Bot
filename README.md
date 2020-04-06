# CMS Bot

This automation project serves multiple functions for interacting with the Content Management System that we use.

I plan on rolling this out to the wider production team, particularly for adding videos - which the dev team haven't currently added batch functionality for - and indexing.

To do this i need to make it more robust and use a py installer to make it into an executable.

This would also raise issues of installing the .exe file due to local admin rights and IT shenanigans.

### To use

Currently have to paste the relevant information into csv columns and then select 1, 2 or 3 to run different function.

### In progress

- cms_batch_actions.py

Started developing batch functionality - running into issues with interacting with table objects as have to match text (no ids or names).

### Improvements

- check whether Video links exist before trying to add them
       
Would stop duplication but might screw up if trying to add a v02 or v03 if v01 already exists due to link numbering. The link would become AddedVideo0 for v02 rather than AddedVideo1. 

Could probably work around this by getting a count function and using AddedVideo{count} to match if v02 or v03 is the 1st or 2nd video to be added.
    - if video1 doesn't exist, count ++; else move to v02
    - if v02 doesn't exist, count ++; else move to v03

- use pandas to read directly from the 'Videos' tab of the EDIT excel spreadsheet

This would be easier than pasting or exporting to a csv. Having the csv provides more control though, which is preferable.

- Use input for specifying a csv file 

This means that it doesn't have to be in the same folder as the .py file.

- create a script selector

In the short term, I can just do the usual interactive input() functions. In the longer term, using a GUI with buttons.

**GUI**

I've used tkinter to make them before, but the aesthetics aren't great. I might just host it on localhost using HTML and CSS.
