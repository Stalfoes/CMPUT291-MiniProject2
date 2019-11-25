from bsddb3 import db


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
                result = curs.set(b's-'+i.encode("utf-8"))
            elif key == 'body':
                result = curs.set(b'b-'+i.encode("utf-8"))
           
        elif x == 'em.idx':
            database = emailsDatabase()
            curs = database.cursor()
            if key == 'cc':
                result = curs.set(b'cc-'+i.encode("utf-8"))
            elif key == 'bcc':
                result = curs.set(b'bcc-'+i.encode("utf-8"))
            elif key == 'to':
                result = curs.set(b'to-'+i.encode("utf-8"))
            elif key == 'from':
                result = curs.set(b'from-'+i.encode("utf-8"))
                
        elif x == 'da.idx':
                database = datesDatabase()
                curs = database.cursor()
                result = curs.set(i.encode("utf-8"))
                
        print(result)
        iter = curs.first()
        while iter:
                print(iter)
                dup = curs.next_dup()
                while(dup!=None):
                    print(dup)
                    dup = curs.next_dup()
                iter = curs.next()

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
    #print(values)
    #print(operators)
    if querytype == 'equality':
        results = equality(key, values)
    elif querytype == 'range':
        querytype = ''
    
    #return results
    
    #curs = database.cursor()
    #iter = curs.first()
    #while iter:
    #        print(iter)
    #        iter = curs.next()


def getQueries():
    while (True):
        results = []
        query = input("enter the query below:\n")
        if query == 'q':
            break
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
            
        #print(formatted)

        #for i in formatted:
        #    results.append(lookup(i))
        #print(results)    
        #op = set.intersection(*map(set,results))

        #if op:
        #    print(op)
        #else:
        #    print('None')



if __name__ == "__main__":
    termsDatabase()
    emailsDatabase()
    recsDatabase()
    datesDatabase()
    getQueries()
    