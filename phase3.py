from bsddb3 import db
import xml.etree.ElementTree

symbols = [':', '<', '>', '>=', '<=', '=']
keyDict = {
    'subj' : 'te.idx',
    'body' : 'te.idx',
    'cc' : 'em.idx',
    'bcc' : 'em.idx',
    'to' : 'em.idx',
    'from' : 'em.idx',
    'date' : 'da.idx',
}

briefOutput = "brief"
fullOutput = "full"

def getOutput(rowID, outputType):
	global briefOutput
	global fullOutput
	record = ""
	database = recsDatabase()
	curs = database.cursor()
	iter = curs.set(rowID.encode("utf-8"))
	if iter != None:
		record = iter[1].decode("utf-8")
	if outputType == briefOutput:
		mail = xml.etree.ElementTree.fromstring(record)
		return mail.find('subj').text
	elif outputType == fullOutput:
		return record

def termsDatabase(): 
    database = db.DB()
    #database.set_flags(db.DB_DUP)
    DB_File = 'te.idx'
    database.open(DB_File, None, db.DB_BTREE)
    #curs = database.cursor()
    #iter = curs.first()
    #while iter:
    #        print(iter)
    #        iter = curs.next()
    return database
    
    
def emailsDatabase():
    database = db.DB()
    #database.set_flags(db.DB_DUP)
    DB_File = 'em.idx'
    database.open(DB_File, None, db.DB_BTREE)    
    return database
    

def recsDatabase():
    database = db.DB()
    #database.set_flags(db.DB_DUP)
    DB_File = 're.idx'
    database.open(DB_File, None, db.DB_HASH)
    return database
    

def datesDatabase():
    database = db.DB()
    #database.set_flags(db.DB_DUP)
    DB_File = 'da.idx'
    database.open(DB_File, None, db.DB_BTREE)
    return database
    
def equality(key, values):
    results = []
    x = keyDict.get(key)
    
    for i in values:
        if x == 'te.idx':
            database = termsDatabase()
            curs = database.cursor()
            if key == 'subj':
                iter = curs.set(b's-'+i.encode("utf-8"))
            elif key == 'body':
                iter = curs.set(b'b-'+i.encode("utf-8"))
           
        elif x == 'em.idx':
            database = emailsDatabase()
            curs = database.cursor()
            if key == 'cc':
                iter = curs.set(b'cc-'+i.encode("utf-8"))
            elif key == 'bcc':
                iter = curs.set(b'bcc-'+i.encode("utf-8"))
            elif key == 'to':
                iter = curs.set(b'to-'+i.encode("utf-8"))
            elif key == 'from':
                iter = curs.set(b'from-'+i.encode("utf-8"))
                
        elif x == 'da.idx':
                database = datesDatabase()
                curs = database.cursor()
                iter = curs.set(i.encode("utf-8"))
                
        #print(result)
        #iter = curs.first()
        if iter!=None:
            results.append((iter[0].decode("utf-8"), iter[1].decode("utf-8")))
            for i in range(curs.count()-1):
                iter = curs.next_dup()
                results.append((iter[0].decode("utf-8"), iter[1].decode("utf-8")))
                
        #print(results)
        #return results

        #while iter:
        #    print(curs.count())
        #    print((iter[0].decode("utf-8"), iter[1].decode("utf-8")))
        #        
        #    dup = curs.next_dup()
        #    while(dup!=None):
        #        print(dup)
        #        dup = curs.next_dup()
        #    iter = curs.next()

    curs.close()
    database.close()
        
        
        #results.append(result)
        #results.append(i)
    
    return results
    
#def range():



def lookup(query):
    results = []
    k = True
    key = ''
    value = ''
    values = []
    operators = []
    for char in query:
        if char in symbols:
            k = False
            if char == ':' or char == '=':
                querytype = 'equality'
            elif char == '>' or char == '<' or char == '>=' or char == '<=':
                querytype = 'range'
                operators.append(char) 
        elif k:
            key = key + char.lower()
        elif not(k):
            if char == '-':
                values.append(value) 
                value = ''
            else:
                value = value + char.lower()
    values.append(value)
    print(values)
    #print(operators)
    if querytype == 'equality':
        #equality(key, values)
         results = equality(key, values)
    elif querytype == 'range':
        querytype = ''
    
    return results
    
	
def helpPage():
	print("Welcome to the query interface. Available commands are:")
	print("q\tQuits the program.")
	print("h\tDisplays this page.")
	print("output=brief\tChanges the output type to brief (Row ID + Subject).")
	print("output=full\tChanges the output type to full (Row ID + Record.")    


def getQueries():
	global briefOutput
	global fullOutput
	helpPage()
	outputType = briefOutput
	while (True):
		results = []
		query = input(" >> ")
		if query == 'q':
            break
		elif query == 'h':
			helpPage()
			continue
		elif query == "output=" + briefOutput:
			outputType = briefOutput
			continue
		elif query == "output=" + fullOutput:
			outputType = fullOutput
			continue
        query = query.split(' ')
        while '' in query:
            query.remove('')
        #print(query)
        formatted = []
        for i in range(len(query)):
            if query[i] in symbols:
                formatted.append(''.join([query[i-1],query[i],query[i+1]]))
            elif (query[i][0] in symbols and len(query[i]) > 1):
                formatted.append(''.join([query[i-1], query[i]]))
            elif (query[i][-1] in symbols and len(query[i]) > 1):
                formatted.append(''.join([query[i], query[i+1]]))
            elif (':' in query[i] and query[i][0] != ':' and query[i][-1] != ':'):
                formatted.append(query[i])
            elif ('<' in query[i] and query[i][0] != '<' and query[i][-1] != '<'):
                formatted.append(query[i])
            elif ('>' in query[i] and query[i][0] != '>' and query[i][-1] != '>'):
                formatted.append(query[i])
            elif ('>=' in query[i] and query[i][0] != '>=' and query[i][-1] != '>='):
                formatted.append(query[i])
            elif ('<=' in query[i] and query[i][0] != '<=' and query[i][-1] != '<='):
                formatted.append(query[i])
            elif ('=' in query[i] and query[i][0] != '=' and query[i][-1] != '='):
                formatted.append(query[i])
            elif ('%' == query[i][-1]):
                formatted.append(query[i])
            elif (':' not in query[i] and '>' not in query[i] and '<' not in query[i] and '<=' not in query[i] and '>=' not in query[i] and '=' not in query[i]):
                formatted[-1] = '-'.join([formatted[-1], query[i]])
            
        print(formatted)

        #for i in formatted:
        #    lookup(i)

        for i in formatted:
            results.append(lookup(i))
        
        #for i in results:
        #    print(str(i)+'\n')    
        
        op = set.intersection(*map(set,results))

        if op:
            for i in op:
                print(i)
        else:
            print('None')



if __name__ == "__main__":
    termsDatabase()
    emailsDatabase()
    recsDatabase()
    datesDatabase()
    getQueries()
    
