
This is a python script for downloading all Channels and TV Shows from tvguide.com/listings page. The table that you see in that page is actually a PDF file. And they are generated from a javascript function. So they are not embedded in the page source.

This script takes control over various page elements and run that javascript method which generates PDF file eventually. Then download that PDF file and parse it to make final csv output with Channel and TV Shows.

Each pdf contains 2hrs program. So you have to load browser 12times with different time frame and you will get 12 pdf files.

To accomplish that, I used selenium web driver with Firefox browser(version 3.6.13). 

This script does following tasks step by step:

1) Load page with Firefox browser
2) Using selenium webdriver, select time(12:00am) from drop-down list and click on GO button. Wait. The page will load with program list starting from 12:00am to 2:00am
3) From page source find link for pdf and download it with no user prompt
4) Repeat step 2-3 with 2hr interval


Now its time to parse those pdf files. Here I used PDFMiner module

Texts are read as TextBox style with their (x,y) position. pdfminer does not read them orderly rather randomly. And therefore its very difficult to know which one is Channel and which one is a TV Show. 
So for each pdf page, I maintained two Hashtable. One to keep position (y, x) of a text box and another to keep text (y, text). Then sorted all y values and from that I found out Channel and their corresponding tv shows in a single pdf page

5) Read each pdf file page by page

For each page:
6) Find out HorizontalTextBoxes along their (y, x) 
7) Populate a list y0set with y0 and a Hashtable y0x0 with (y0, x0) value of a Box
8) Populate a Hashtable with (y0, Text) value of a Box
9) Sort y0set. 

y0 value for all boxes in a row are very close to each other. Most of the cases they are same
y0 value between two rows are differ more than 20 point. 
So from that info, we can find out boxes that are in a same row.

10) From y0set, find out boxes that are in a same row
11) For same row boxes, rearrange them against their x0 value. First element is Channel name and the rest are all Tv Shows
12) Put them onto global Channel list and TV Show(Show_Table) Hashtable
13) Also make sure that two consecutive tv shows are unique

Now we have a Channel list and a <Channel, TVShowList> hashtable.

Sometimes it happens for pdfminer that it counts two consecutive box as single one. So two tv show names will be merged as a single one. To solve this, I further checked each tvshow of a channel with others in the same list. And separated them as individual name.

14) Make csv output using Channel list and <Channel, TVShowList> hashtable.

