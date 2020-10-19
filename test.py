## Secure login and storage of passwords using hashing and sqlite
import sqlite3
import hashlib
import json


conn = sqlite3.connect('DatabaseName.db')
c = conn.cursor()



##Once table is initially created, comment out this line
##Table has a completion marker set to = '0'/F as default
##Create Table
#c.execute(' ' 'CREATE TABLE TableName (SocialMediaSite text, HashedPassword text, completionMarker text) ' ' ')


def createNewRow():
    print('hi')
    
    c.execute('INSERT INTO TableName(SocialMediaSite, HashedPassword, completionMarker) values (0,0,0)')
    
    print('ENTER NAME OF WEBSITE PASSWORD BELONGS TO: ')
    oSocials = (input(),)
    c.execute('update TableName set SocialMediaSite = ? where SocialMediaSite = 0', oSocials)
    
    print('ENTER PASSWORD: ')
    oPassword = input()
    passwordAsBytes = str.encode(oPassword)
    ##Change to preference
    m = hashlib.sha256()
    m.update(passwordAsBytes)
    passToStore = str(m.hexdigest(),)
    c.execute('update TableName set HashedPassword = ? where HashedPassword = 0', [passToStore])
    
    # Completion marker
    c.execute('update TableName set completionMarker = 1 where completionMarker = 0')
    
    #Save new information added
    conn.commit()
    print('\n\nSaved.\n')

    
def viewData(connection):
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    curs.execute('select * from TableName order by SocialMediaSite')
    rows = curs.fetchall()
    print('HERE IS A LIST OF YOUR DATA:\n')
    for row in rows:
        print(tuple(row))
        print('\n')
    print('PRESS ENTER TO CONTINUE')
    wait = input(' ')
        
        
def databaseToJSON(connection):
#Template name for JSON file
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    curs.execute('select * from TableName')
    rows = curs.fetchall()
    with open("dataFile.json", "w") as write_file:
        for row in rows:
            ##Dump data
            json.dump(tuple(row), write_file)
    ##Close File
    write_file.close()



print('NOW CONNECTED TO DATABASE...\n')
createNewRow()
viewData(conn)





#Close File                     
conn.close()


