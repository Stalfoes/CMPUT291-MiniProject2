import xml.etree.ElementTree
import sys
import re
import os


Files = ['datesN.txt', 'emailsN.txt', 'recsN.txt', 'termsN.txt']
FilesS =  ['datesS.txt', 'emailsS.txt', 'recsS.txt', 'termsS.txt']
indexes = ['da.idx', 'em.idx', 're.idx', 'te.idx']


startDocumentTag = "<emails type=\"array\">\n"
mailStartTag = "<mail>"
mailEndTag = "</mail>"
endDocumentTag = "</emails>\n"

termRegex = r"[0-9a-zA-Z_-]{3,}"
emailRegex = r"\b[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\b"

def parseDocument(document):
	global startDocumentTag
	global mailStartTag
	global mailEndTag
	global endDocumentTag
	# Going to parse it email by email
	xmlFile = open(document, 'r')
	emailsStart = xmlFile.readline()
	emailsStart = xmlFile.readline()	# Hope that this is the first mail tag
	if emailsStart != startDocumentTag:
		print("ERROR: EMAILS START TAG NOT FOUND.")
		sys.exit()
	# Clear and create the files
	clearAndCreateFile("terms.txt")
	clearAndCreateFile("emails.txt")
	clearAndCreateFile("dates.txt")
	clearAndCreateFile("recs.txt")
	# Parse until we reach the end of the emails array
	workingLine = emailsStart
	while workingLine != endDocumentTag:
		workingLine = xmlFile.readline()
		if workingLine == endDocumentTag:
			break
		parseMail(workingLine)
	# Close the file
	xmlFile.close()


def parseMail(mailString):
	mail = xml.etree.ElementTree.fromstring(mailString)
	makeTermsFile(mail)
	makeEmailsFile(mail)
	makeDatesFile(mail)
	makeRecsFile(mail, mailString)


def makeRecsFile(mail, mailString):
	row = mail.find('row').text
	key = [row + ":" + mailString]
	writeToFile("recs.txt", key)


def makeDatesFile(mail):
	row = mail.find('row').text
	date = mail.find('date').text
	key = [date + ":" + row + "\n"]
	writeToFile("dates.txt", key)


def makeEmailsFile(mail):
	row = mail.find('row').text
	fromText = mail.find('from').text
	to = mail.find('to').text
	cc = mail.find('cc').text
	bcc = mail.find('bcc').text
	# Extract the emails
	fromEmails = findEmails(fromText)
	toEmails = findEmails(to)
	ccEmails = findEmails(cc)
	bccEmails = findEmails(bcc)
	# Convert them to their respective keys
	fromKeys = ["from-" + e.lower() + ":" + row + "\n" for e in fromEmails]
	toKeys = ["to-" + e.lower() + ":" + row + "\n" for e in toEmails]
	ccKeys = ["cc-" + e.lower() + ":" + row + "\n" for e in ccEmails]
	bccKeys = ["bcc-" + e.lower() + ":" + row + "\n" for e in bccEmails]
	# Concatenate
	allKeys = fromKeys + toKeys + ccKeys + bccKeys
	writeToFile("emails.txt", allKeys)


def findEmails(line):
	if line is None:
		return []
	global emailRegex
	emails = re.findall(emailRegex, line)
	return emails


def makeTermsFile(mail):
	row = mail.find('row').text
	subject = mail.find('subj').text
	body = mail.find('body').text
	# parse the bodies of text (subject and body) for terms
	subjectTerms = findTerms(subject)
	bodyTerms = findTerms(body)
	# convert all of them to the key form of the terms
	subjectKeys = ["s-" + t.lower() + ":" + row + "\n" for t in subjectTerms]
	bodyKeys = ["b-" + t.lower() + ":" + row + "\n" for t in bodyTerms]
	allKeys = subjectKeys + bodyKeys
	# write all the keys to the file
	writeToFile("terms.txt", allKeys)


def findTerms(text):
	if text is None:
		return []
	global termRegex
	terms = re.findall(termRegex, text)
	return terms


def clearAndCreateFile(fileName):
	# Create the file or open it
	f = open(fileName, 'w+')
	f.close()
	# Clear the file
	f = open(fileName, 'w').close()


def writeToFile(fileName, lines):
	# Open the file again so that we can append to it
	f = open(fileName, 'a')
	for line in lines:
		f.write(line)
	f.close()



def restart():
	for i in range(len(Files)):
		if os.path.exists(Files[i]):
			os.remove(Files[i])
		if os.path.exists(FilesS[i]):
			os.remove(FilesS[i])
		if os.path.exists(indexes[i]):
			os.remove(indexes[i])


if __name__ == "__main__":
	restart()
	if len(sys.argv) < 2:
		print("Enter the document from which to parse as the argument.")
		sys.exit()
	parseDocument(sys.argv[1])