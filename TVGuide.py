
#### 	Downloading TVShow list from tvguide.com/listings    ####
#### 	                  Done by Asraf                      ####



import os
import sys
import re
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTTextLineHorizontal, LTTextBoxHorizontal, LTTextContainer, LTLine, LTFigure
from pyvirtualdisplay import Display


Show_Table = dict()		# <Channel, TV Show List>
Channel_List = []

res_dir = "/Asraf/D/Office_NU/TVGuide.com/Resources/"


def removeFiles():		
	files = os.listdir(res_dir)	
	try:
		for f in files:		
			if(f.endswith(".pdf")):
				os.remove(res_dir + f)
	except Exception as err:
		print "Error in removeFiles(): " + str(err)


def downloadFiles():			
	try:		
		#display = Display(visible=0, size=(800, 600))
		#display.start()			
						
		fp = webdriver.FirefoxProfile()		
		fp.set_preference("browser.download.dir", res_dir)
		fp.set_preference("browser.download.folderList",2)
		fp.set_preference("browser.download.manager.showWhenStarting",False)		
		fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")		
		
		browser = webdriver.Firefox(firefox_profile=fp)				
		
		browser.get("http://www.tvguide.com/Listings/") 		# Load page		
		
		'''
		am_pm_list = ["12:00am", "2:00am", "4:00am", "6:00am", "8:00am", "10:00am", "12:00pm", "2:00pm", "4:00pm", "6:00pm", "8:00pm", "10:00pm"]
		for am_pm in am_pm_list:			
			elem = browser.find_element_by_id("timeSelect")			
			elem.send_keys(am_pm + Keys.RETURN)			# Set Time						
		
			browser.find_element_by_id("btnGoButton").click()	#Press 'GO'			
			time.sleep(5) 						# Let the page load, will be added to the API				
		
			browser.find_element_by_id("printlinkv2").click()	#Download PDF file that attached to the form
		'''
		
		n = 1
		while n <= 12:
			elem = browser.find_element_by_id("timeSelect")			
			if n == 1:
				elem.send_keys("12:00am" + Keys.RETURN)			# Set Time
			elif n == 2:
				elem.send_keys("2:00am" + Keys.RETURN)			# Set Time
			elif n == 3:
				elem.send_keys("4:00am" + Keys.RETURN)			# Set Time
			elif n == 4:
				elem.send_keys("6:00am" + Keys.RETURN)			# Set Time
			elif n == 5:
				elem.send_keys("8:00am" + Keys.RETURN)			# Set Time
			elif n == 6:
				elem.send_keys("10:00am" + Keys.RETURN)			# Set Time
			elif n == 7:
				elem.send_keys("12:00pm" + Keys.RETURN)			# Set Time
			elif n == 8:
				elem.send_keys("2:00pm" + Keys.RETURN)			# Set Time
			elif n == 9:
				elem.send_keys("4:00pm" + Keys.RETURN)			# Set Time
			elif n == 10:
				elem.send_keys("6:00pm" + Keys.RETURN)			# Set Time	
			elif n == 11:
				elem.send_keys("8:00pm" + Keys.RETURN)			# Set Time
			elif n == 12:
				elem.send_keys("10:00pm" + Keys.RETURN)			# Set Time
				
			browser.find_element_by_id("btnGoButton").click()	#Press 'GO'			
			time.sleep(5) 						# Let the page load, will be added to the API				
		
			browser.find_element_by_id("printlinkv2").click()	#Download PDF file that attached to the form
			
			n += 1
		
		browser.close()		
		#display.stop()
		
	except Exception as err:
		print "Error in downloadFiles(): " + str(err)



def readFiles(path):	
	try:         
		fp = open(path, 'rb')			# Open a PDF file
		parser = PDFParser(fp)			# Create a PDF parser object associated with the file object.
		doc = PDFDocument()			# Create a PDF document object that stores the document structure
		parser.set_document(doc)		# Connect the parser and document objects
		doc.set_parser(parser)			
		doc.initialize("")			# Supply the password for Initialization. If no password then put an empty string
				
		rsrcmgr = PDFResourceManager()		# Create a PDF resource manager object that stores shared resources.
		
		laparams = LAParams()			# Set parameters for analysis.
		
		device = PDFPageAggregator(rsrcmgr, laparams=laparams)		# Create a PDF page aggregator object.
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		
		for page in doc.get_pages():				# Process each page in the document
			interpreter.process_page(page)			
			layout = device.get_result()			# receive the LTPage object for the page.
			parsePage(layout)
			#break					
		
	except Exception as err:
		print "error in readFiles(): " + str(err)



def formatText(text):
	res=""
	char_list = ["<", "<<", ">", ">>"]
	i = 0
	while i < len(text):
		if text[i] not in char_list:
			if(text[i] == "\n"):
				res += " "
			else:
				res += text[i]
		i += 1
	return res.strip()


def validText(text):
	str_list = ["TVGuide", "TV Listings", "http://", "Date:", "view your", " AM\n", " PM\n", "LEGEND", "MOVIES", "SPORTS","FAMILY", "NEWS", "Copyright", "Page "]
	for item in str_list:
		if item in text:
			return 0		
	return 1	





def reArrangeList(xl, show):	
	done = 1	
	for i in range(0, len(xl)):			# Bubble Sort
		done = 1
		for j in range(1, len(xl)):
			if xl[j-1] > xl[j]:
				tmp = xl[j]
				xl[j] = xl[j-1]
				xl[j-1] = tmp
			
				tmp = show[j]
				show[j] = show[j-1]
				show[j-1] = tmp
				
				done = 0
		if done:
			break
	i = 1
	while i < len(show):
		if show[i-1] == show[i]:		# Remove consequtive duplicate show
			show.pop(i)
			
		i += 1		
	
	return show




def parsePage(layout):
	global Show_Table, Channel_List
	y0set = set()
	table = dict()		# table = {} <key, value> = <y0Pos, Text List>
	y0x0 = dict()		# <y, x>
	L = []
	
	try:
		objstack = list(reversed(layout._objs))		# _objs contains set of object. It may be LTTextBox, LTTextLine, LTFigure, LTImage, LTTextLineHorizontal, LTTextBoxHorizontal, LTChar, LTRect, LTLine, LTAnon
	
		while objstack:
			b = objstack.pop()			
			if type(b) in [LTTextBoxHorizontal] and validText(b.get_text()):				
				key = b.y0				
				value = b.get_text().strip()			
				value = value.encode('ascii', 'ignore')		# convert unicode to ascii. without conversion "ashraf" is u"ashraf"
				value = formatText(value)		
				
				
				if key not in table:
					if value != "":
						L = []
						L.append(value)
						table[key] = L;				# Populate table with <y0Pos, Text List>					
				else:
					if value != "":
						L = []
						L = table[key]
						
						#if value not in L:			# Remove duplicates
						#if value != L[len(L)-1]:
						#	L.append(value)
						#	table[key] = L
							
						L.append(value)
						table[key] = L						
									
				y0set.add(b.y0)					# Also save y0Pos
								
				
				# Saving (y0, x0)
				if b.y0 not in y0x0:
					x = []
					x.append(b.x0)
					y0x0[b.y0] = x
				else:
					x = []
					x = y0x0[b.y0]
					x.append(b.x0)
					y0x0[b.y0] = x
										
		y0List = list(reversed(sorted(y0set)))		
					
		
		i = 0
		while i < len(y0List):							# For each y0Pos, find out the Channel and TV Show. 
			#ch = table[y0List[i]]			
			show = []
			start = float(y0List[i])			
			#i += 1			
			
			xl = []
			txt = []
			while i < len(y0List) and ( float(y0List[i]) > (start - 20) ):			# Diff between consequtive two upper and lower text box is more than 25 point
				xl.extend(y0x0[y0List[i]])						# So this block will catch up all the text box in a row
				#show.extend(table[y0List[i]])
				txt.extend(table[y0List[i]])
				i += 1
			
			if len(xl) == 0:
				i += 1
				continue
				
			#if len(show) > 1:
			elif len(xl) > 1:				
				#show = reArrangeList(xl, show)					# Sort Shows according to their x0 entry in a row, using Bubble Sort on x0				
				txt = reArrangeList(xl, txt)					# Sort TextBox according to their x0 entry in a row, using Bubble Sort on x0				
							
				ch = txt[0]					# 1st element in a row is a Channel
				show = txt[1:]					# And rest are the TV Shows
								
				if(ch not in Channel_List):
					Channel_List.append(ch)					# Populate Channel List
				
				if ch not in Show_Table:					# Populate TV Show table
					Show_Table[ch] = show
				else:
					L = Show_Table[ch]
					#L.extend(show)
					if L[len(L)-1] == show[0]:			# If previous program and current one is same then delete current
						show.pop(0)
					
					L.extend(show)					
					Show_Table[ch] = L								
		
	except Exception as err:
		print "error in parsePage(): " + str(err)
		 



def isSubstring(show1, show2):
	show1 = show1.strip().upper()
	show2 = show2.strip().upper()
	l1 = len(show1)
	l2 = len(show2)
	try:
		if l1 == 0 or l2 == 0:			
			return []
		if l1 == l2:
			return []
		elif (show1[0] == show2[0]) or (show1[l1-1] == show2[l2-1]):
			if (l1 > (l2+4)) and show1.startswith(show2 + " "):# or show1.endswith(" " + show2)):
				for w in ["NEW", "EXTRA", "PART"]:
					if show1.startswith(show2 + " " + w):						
						return []						
				
				if len(show1.split(" ")) >= ( len(show2.split(" ")) + 2 ):						
					return [0, len(show2)]
				else:						
					return []								
			
			elif (l1 > (l2+4)) and show1.endswith(" " + show2):
				if len(show1.split(" ")) >= ( len(show2.split(" ")) + 2 ):						
					return [show1.find(show2), len(show2)]
				else:						
					return []				
			
			elif (l2 > (l1+4)) and show2.startswith(show1 + " "):# or show2.endswith(" " + show1)):
				for w in ["NEW", "EXTRA", "PART"]:
					if show2.startswith(show1 + " " + w):					
						return []
					
				if len(show2.split(" ")) >= ( len(show1.split(" ")) + 2 ):						
					return [0, len(show1)]
				else:					
					return []
			
			elif (l2 > (l1+4)) and show2.endswith(" " + show1):
				if len(show2.split(" ")) >= ( len(show1.split(" ")) + 2 ):						
					return [show2.find(show1), len(show1)]
				else:					
					return []
							
		else:
			return 0
	except Exception as err:
		print "error in isSubstring(): " + show1 + ", " + show2 + ". " + str(err)



def fixAdjacent(show_list):
	try:		
		i = 1
		while i < len(show_list):
			j = i-1
			while j >= 0:				
				si_le = isSubstring(show_list[j], show_list[i])
				
				if si_le:
					if len(show_list[j]) > len(show_list[i]):						
						if si_le[0] == 0:
							s1 = show_list[j][0:si_le[1]]
							s2 = show_list[j][si_le[1]+1:]
						else:
							s1 = show_list[j][0:si_le[0]-1]
							s2 = show_list[j][si_le[0]:]
						
						show_list.pop(j)
						show_list.insert(j, s2)
						show_list.insert(j, s1)						
						
					elif len(show_list[i]) > len(show_list[j]):						
						if si_le[0] == 0:
							s1 = show_list[i][0:si_le[1]]
							s2 = show_list[i][si_le[1]+1:]
						else:
							s1 = show_list[i][0:si_le[0]-1]
							s2 = show_list[i][si_le[0]:]
						
						show_list.pop(i)
						show_list.insert(i, s2)
						show_list.insert(i, s1)																	
				j -= 1
			i += 1	
		
	except Exception as err:
		print "error in fixAdjacent(): " + str(err)
		
	return show_list




# Sometimes it happens for PDFMiner that it counts two consqutive boxes as a single one.
# So two tvshow names are merged into one. The following method seperate them all.

def fixAdjacentRowProblem():
	global Show_Table, Channel_List
	for channel in Channel_List:
		show_list = Show_Table[channel]		
		show_list = fixAdjacent(show_list)		
		
		i = 1
		while i < len(show_list):				# Remove duplicate
			if show_list[i-1] == show_list[i]:		
				show_list.pop(i)
				i -= 1				
			i += 1	
		
		Show_Table[channel] = show_list



def makeOutput():
	global Channel_List, Show_Table
	try:
		#file = open("/Asraf/D/Office_NU/WebPageCrawling/TVGuide.com/TV_Listings.txt", "w")
		file = open("TV_Listings.txt", "w")
		file.writelines("\'TV CHANNEL\' -> [\'TV SHOW LIST\']")
		
		for ch in Channel_List:
			line = "'" + ch + "'" + " -> " + str(Show_Table[ch])
			file.writelines("\n\n")
			file.writelines(line)
		
		file.close()
	except Exception as err:
		print "error in makeOutput(); " + str(err)
		

def makeCSV():
	global Channel_List, Show_Table
	maxColLen = 0	
	for ch in Channel_List:
		if len(Show_Table[ch]) > maxColLen:
			maxColLen = len(Show_Table[ch])			
	try:
		today = datetime.date.today()		
		#file = open("/Asraf/D/Office_NU/TVGuide.com/TV_Listings_"+today.isoformat()+".csv", "w")
		file = open("TV_Listings_"+today.isoformat()+".csv", "w")
		row = "\"CHANNEL\""
		for i in range(1, maxColLen+1):
			row += ","
			row += "\"" + "TV_SHOW_" + str(i) + "\""
		file.writelines(row + "\n")		
		
		for ch in Channel_List:
			row = "\"" + ch + "\""
			show_list = Show_Table[ch]
			i = 0
			while i < len(show_list):
				row += ","
				row += "\"" + show_list[i] + "\""
				i += 1
			
			while i < maxColLen:
				row += ","
				row += "\"" + "\""
				i += 1
				
			file.writelines(row + "\n")			
		
		file.close()
	except Exception as err:
		print "error in makeOutput(); " + str(err)

		
def main():			
	try:		
		removeFiles()				# Delete all files from Resources dir, which contains downloaded PDF files	
		
		downloadFiles()				# Download all PDFs, each containing 2hrs TVShow
		
		# Sort file names
		i = 0
		fileList = []
		files = os.listdir(res_dir)
		while i < len(files):			
			for f in files:			
				if(f.endswith(".pdf")):
					n = re.findall(r'\d+', f)					
					if(len(n)==0 and i==0):						
						fileList.append(f)						
						break
					else:
						if (len(n)>0 and int(n[0]) == i):														
							fileList.append(f)						
							break
				else:
					files.remove(f)
			i += 1			
		
		
		# Read and Parse each file
		for f in fileList:			
			if(f.endswith(".pdf")):
				readFiles(res_dir+f)
				#break
				
				
		fixAdjacentRowProblem()			# Sometimes it happens for pdfminer that it counts two consecutive boxes as single one. So two tvshow is merged into one.							
		
								
		makeCSV()		# csv file
		
		
	except Exception as err:
		print "Error in main(): " + str(err)
	
	
if __name__ == '__main__':
	main()
