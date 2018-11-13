from textract import process
import PyPDF2
import re
from collections import OrderedDict


#replace the path of your book
file_path = '/home/vikam/rahul/sample/siddhartha.pdf'
text = process(file_path)
text = text.replace('\xe2\x80\x9c','"').replace('\xe2\x80\x9d','"').replace('\xe2\x80\x99s',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x99',"'").replace('Siddhartha: An Open-Source Reader','').replace('\xe2\x80\x94','-')

in_valid = ['A','An','The','He','She','It','At','Of','They','Could','I','Do','While','For','To','From','When','In','Those','Let','You','Me','Here','There','With','Why','Who','This','That','Also'
,'Is','As','Not','If','Else','Or','Be','Yes','No','My','On','Up','Down','By','Before','After','Which','Then','All','One','Two','Three','Four']

special_characters = ['~','#','$','%','^','&','*','-','+','=','_',';',':',"'"]
strict = ['$','#','%','=','*',';',',']

text_pypdf = PyPDF2.PdfFileReader(file_path)
total_number_of_pages = text_pypdf.getNumPages()
"""def extract_using_pdf(n):
	content = " "
	for i in range(0,total_number_of_pages):
		content += n.getPage(i).extractText() + "\n"
	return content	"""
def get_names(text):
	n = set([e for e in text.split() if e > 1 and not e.isupper() and e[0].isupper() and e not in in_valid if not any(c.isdigit() for c in e) ]);
	return n
print get_names(text)
	
#get dialogue 
def get_dialogue(text):
	speaker = {'speaker':[],'listener':[]}
	start_dialogue = text.find('"')
	if start_dialogue == -1:
		return None,0,[]
	end_dialogue = text.find('"', start_dialogue + 1)
	dialogue = text[start_dialogue+1:end_dialogue]

	conversation_start = text.rfind('.',0,start_dialogue)
	conversation_end = text.find('.',end_dialogue)
        find_speakers = text[conversation_start+1:start_dialogue]
        find_speakers1 = text[end_dialogue-1:conversation_end]
 
        if find_speakers:
		new_list = find_speakers.split()
                for li in new_list:
			if li[0].isupper() and li not in in_valid:
				speaker['speaker'].append(li)
	if find_speakers1:
		new_list = find_speakers1.split()
		for li in new_list:
			if li and li[0].isupper() and li not in in_valid:
				speaker['speaker'].append(li)
			
	return dialogue, end_dialogue,speaker


def get_all_dialogues(text):
    dialogues = {'dialog': {},'speaker':{},'listener':{}}
    i = 0
    listener = []		
    while True:
    	dialogue, end_pos,speaker = get_dialogue(text)
    	if dialogue:
    		dialogues['dialog'][i] = dialogue
		dialogues['speaker'][i]= speaker['speaker']
		#dialogues['listener'][i] = speaker['listener'] 
    		text = text[end_pos+1:]
		i += 1
    	else:
		i = 0
    		break
    return dialogues
#get page titles    
def get_title(file):
	outline = file.getOutlines()
	titles = []
	for title in outline:
		if type(title) == list:
			for sub_title in title:
				titles.append(sub_title['/Title'])
		elif title['/Title'] != '':
		    titles.append(title['/Title'])
	return titles
#find characters
"""def get_all_characters(text,titles_list):
	speakers = []
	words = re.findall(r'\w+', text)
	for e in words:
		if e[0].isupper() and e[0] != int and e[0] not in article and e[0]not in titles_list and len(e)>2:
			speakers.append(e)
	return speakers"""

#get pages of each chapter
def get_page_numbers_of_each_chapter(text):
	list_of_titles = get_title(text)
	nl = [e.replace(' ','') for e in list_of_titles]
	chapters_with_pages = {l.replace(' ','') : {'pages':[]} for l in list_of_titles}
	#chapter_with_pages= OrderedDict((l.replace(' ','') , []) for l in list_of_titles)
	for i in range(0,total_number_of_pages):
		pdf_read = text.getPage(i)
		pdf_extract_text = pdf_read.extractText()
		for e in nl:
			if pdf_extract_text.startswith(e):
				chapters_with_pages[e]['pages'].append(i)

	return chapters_with_pages;





def get_all_characters(text):
	characters = []
	for e in text:
		word = e.split()
		for w in word:
			if w[0].isupper() and len(w)>2 and w not in article and bool(re.search(r'\d',w)) == False:
				characters.append(w)
	return characters


#titles 

titles = get_title(text_pypdf)
#print titles
"""for t in titles:
	if t == "Why Open Source?":
		print """



#print text.find("Why Open Source?")
#total_dialogues = get_all_dialogues(text)
#print total_dialogues


"""n = []
for d in total_dialogues:
	if d[0].isupper():
		n.append(d)
#print n"""
#characters = get_all_characters(total_dialogues)
#print characters

#n =set(characters)
#print n
#new =list(n)
#print len(new)


#new = text.split()


def get_text_from_chapters(text_textract,titles):
	dialogues = {title:{} for title in titles}
	for i in range(len(titles)):
		start_title = text_textract.find(titles[i])
		if i != len(titles)-1: 
			end_title = text_textract.find(titles[i+1])
		else:
			end_title = len(text_textract)
		new_text = text_textract[start_title+1:end_title]
		find_dialogues = get_all_dialogues(new_text)
		dialogues[titles[i]] = find_dialogues

	return dialogues



title = get_title(text_pypdf)
titles = [title.encode('utf8') for title in titles]
#print titles

#print total_dialogues




#print get_all_dialogues(text)
#content = extract_using_pdf(text_pypdf);
chapters_with_page_numbers = get_page_numbers_of_each_chapter(text_pypdf)
chapters_with_pages = {k: v for k, v in chapters_with_page_numbers.iteritems() if v['pages']}
new_titles = []
for key in titles:
	if key.replace(' ','') in chapters_with_pages:
		new_titles.append(key)


total_dialogues = get_text_from_chapters(text,new_titles)

dialogue = []
for dialog in total_dialogues:
	for d in dialog:
		dialogue.append(d)
nlist = {}
for key, value in total_dialogues.iteritems():
	for i in range(len(value['speaker'])-1):
		nlist[i] = {}
		nlist[i]['speaker'] = value['speaker'][i]	
		nlist[i]['dialog'] = value['dialog'][i]


	
#print text.split();


#chapters_with_empty_pages =  OrderedDict(chapters_with_page_numbers.items)
#print get_all_dialogues(text)

