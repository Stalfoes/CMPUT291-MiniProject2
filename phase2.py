import os

Files = ['datesN.txt', 'emailsN.txt', 'recsN.txt', 'termsN.txt']
FilesS =  ['datesS.txt', 'emailsS.txt', 'recsS.txt', 'termsS.txt']
indexes = ['da.idx', 'em.idx', 're.idx', 'te.idx']
trees = ['btree', 'btree', 'hash', 'btree']

def checkMultipleCalls():
    if (os.path.exists("datesS.txt")):
        print("phase2 done already")
        return False
    else:
        return True


def makeNewFiles():

	for i in Files:
		if os.path.exists(i):
			os.remove(i)

	os.system("sort -u dates.txt > datesN.txt")
	if os.path.exists("dates.txt"):
			os.remove("dates.txt")
    
	os.system("sort -u emails.txt > emailsN.txt")
	if os.path.exists("emails.txt"):
			os.remove("emails.txt")
    
	os.system("sort -u recs.txt > recsN.txt")
	if os.path.exists("recs.txt"):
			os.remove("recs.txt")
    
	os.system("sort -u terms.txt > termsN.txt")
	if os.path.exists("terms.txt"):
			os.remove("terms.txt")
    


def removeSlash(read, write):
	inf = open(read, 'r')
	out = open(write, 'w')

	for line in inf:
		line = line.replace('\\', '&#92;')
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
			
def makeIndexes(File, index, tree):
    # db_load -T -f emails.txt -t btree email.idx
    os.system("db_load -T -c duplicates=1 -f " + File + " -t " + tree + " " + index)
	
if __name__ == "__main__":
    run = checkMultipleCalls()
    
    if run:
        makeNewFiles()    
        for i in range(len(FilesS)):
            removeSlash(Files[i], FilesS[i])
            makeIndexes(FilesS[i], indexes[i], trees[i])
            #print(Files[i])
            os.remove(Files[i])

