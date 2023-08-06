import string as _string
import random

#### 0123456789
lettersAndDigits = _string.digits

#### Return random integer value
def integer(length=6, prefix=None):

    #### Prefix should be of type int
    if not isinstance(prefix, int):
        raise Exception('Prefix should be of type int')
    
    randomInteger = int(''.join(random.choice(lettersAndDigits) for i in range(length)))

    if not prefix == None:
        randomInteger = prefix + randomInteger

    return randomInteger

#### Return random string value
def string(length=6, prefix=None):
    randomString = int(''.join(random.choice(lettersAndDigits) for i in range(length)))

    if not prefix == None:
        randomString = prefix + str(randomString)

    return str(randomString)


### TODO create function to accept a database cursor
#### Function to create a unique ID for in the database....
# def uniqueID(table, column, stringLength=6, prefix=None):
#     idExists = True
#     while idExists:
#         randomID = self.randomStringDigits(stringLength, prefix=prefix)

#         with connections['FMM'].cursor() as cursor:
#             cursor.execute('SELECT * FROM {} WHERE {} = "{}"'.format(table, column, randomID))

#             if not len(cursor.fetchall()):
#                 idExists = False
    
#     return randomID