import os
from bsddb3 import db

# db_load -T -f emails.txt -t btree email.idx
	

def makeNewFiles():

	Files = ['datesN.txt', 'emailsN.txt', 'recsN.txt', 'termsN.txt']

	for i in Files:
		if os.path.exists(i):
			os.remove(i)

	os.system("sort -u dates.txt > datesN.txt")
	os.system("sort -u emails.txt > emailsN.txt")
	os.system("sort -u recs.txt > recsN.txt")
	os.system("sort -u terms.txt > termsN.txt")



if __name__ == "__main__":
	makeNewFiles()
	
	
"""
def makeRecsDB():
	database = db.DB()
	DB_File = "recs.db"
	database.open(DB_File, None, db.DB_HASH, db.DB_CREATE)
	

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


