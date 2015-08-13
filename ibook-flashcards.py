import os
import sqlite3
import random
from DictionaryServices import *

bookDB = '/Users/gggg/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/'
notesDB = '/Users/gggg/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/'

connectB = sqlite3.connect(bookDB + [f for f in os.listdir(bookDB) if f.endswith('.sqlite')][0])
c = connectB.cursor()
c.execute('SELECT ZASSETID, ZTITLE AS Title, ZAUTHOR AS Author FROM ZBKLIBRARYASSET WHERE ZTITLE IS NOT NULL')
books = c.fetchall()

connectN = sqlite3.connect(notesDB + [f for f in os.listdir(notesDB) if f.endswith('.sqlite')][0])
cursor = connectN.cursor()
query = '''
			SELECT
				ZANNOTATIONREPRESENTATIVETEXT as BroaderText,
				ZANNOTATIONSELECTEDTEXT as SelectedText,
				ZANNOTATIONNOTE as Note,
				ZFUTUREPROOFING5 as Chapter,
				ZANNOTATIONCREATIONDATE as Created,
				ZANNOTATIONMODIFICATIONDATE as Modified,
				ZANNOTATIONASSETID
			FROM ZAEANNOTATION
			WHERE ZANNOTATIONSELECTEDTEXT IS NOT NULL
			ORDER BY ZANNOTATIONASSETID ASC,Created ASC
			'''
cursor.execute(query)
notes = cursor.fetchall() 

print 'Notes count: ' + str(len(notes))
rand = random.randint(0,len(notes))
word = notes[rand][1]
context = notes[rand][0]
print 'word: ' + word
wordrange = (0, len(word))
dictresult = DCSCopyTextDefinition(None, word, wordrange)
if not dictresult:
    errmsg = "'%s' not found in Dictionary." % (word)
    print errmsg.encode('utf-8')
else:
    print 'meaning: ' + dictresult.encode('utf-8')

print 'context: ' + context
book = [x for x in books if x[0]==notes[rand][-1]][0]
print 'book: ' + book[1] + ', ' + book[2]