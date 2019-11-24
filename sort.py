import os

# db_load -T -f emails.txt -t btree email.idx
Files = ['datesN.txt', 'emailsN.txt', 'recsN.txt', 'termsN.txt']
FilesS =  ['datesS.txt', 'emailsS.txt', 'recsS.txt', 'termsS.txt']
def makeNewFiles():

	global Files

	for i in Files:
		if os.path.exists(i):
			os.remove(i)

	os.system("sort -u dates.txt > datesN.txt")
	os.remove("dates.txt")
	os.system("sort -u emails.txt > emailsN.txt")
	os.remove("emails.txt")
	os.system("sort -u recs.txt > recsN.txt")
	os.remove("recs.txt")
	os.system("sort -u terms.txt > termsN.txt")
	os.remove("terms.txt")


def removeSlash(read, write):
	inf = open(read, 'r')
	out = open(write, 'w')
	
	

	for line in inf:
		line = line.replace('\\', '&92')
		k = True
		key = ''
		data = ''
		for char in line:
			if char == ':':
				k = False
			elif k:
				key = key + char
			elif not(k):
				data = data + char
		out.write(key + '\n')
		out.write(data)
			
	
if __name__ == "__main__":
	global FilesS
	global Files
	makeNewFiles()
	for i in range(len(FilesS)):
		removeSlash(Files[i], FilesS[i])
		os.remove(Files[i])
	
	
	
"""
def makeRecsDB():
	database = db.DB()
	DB_File = "recs.db"
	database.open(DB_Filedb_load, None, db.DB_HASH, db.DB_CREATE)
	

def makeEmailsDB():
	database = db.DB()
	DB_File = "emails.db"
	database.open(DB_File, None, db.DB_HASH, db.DB_CREATE)
		
def makeDatesDB():
	database = db.DB()
	DB_File = "dates.db"
	database.open(DB_File, None, db.DB_HASH, db.DB_CREATE)

def makeTermsDB():	
	database = db.DB()
	DB_File = "terms.db"
	database.open(DB_File, None, db.DB_HASH, db.DB_CREATE)	
"""


