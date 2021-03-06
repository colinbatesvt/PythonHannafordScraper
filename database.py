import mysql.connector

def createInstance():
    mydb = mysql.connector.connect(
    host="localhost",
    user="hannafordApp",
    password="groceryListTestPassword",
    database="hannaford_products"
    )

    #print(mydb)
    return mydb


def printAll(mydb):
    cursor = mydb.cursor()
    query = ("SELECT * FROM products")
    cursor.execute(query)

    for (id, name, last_update) in cursor:
        print("{}, {}, {:%d %b %Y}".format(
        id, name, last_update))

    cursor.close()

def insertProduct(mydb, id, name, price, brand, category, variant, dataList):
    #sanitize inputs
    name = cleanString(name)
    brand = cleanString(brand)
    category = cleanString(category)
    variant = cleanString(variant)
    dataList = cleanString(dataList)

    #check for duplicate
    cursor = mydb.cursor(buffered=True)
    query = ("SELECT * FROM products where id={:d}".format(id))
    cursor.execute(query)

    #if duplicate update
    if(cursor.rowcount == 1):
        #first enter the historical price into the prices table
        row = cursor.fetchone()
        old_date = row[2]
        old_price = float(row[3])
        if(old_price != price):
            query = ("insert into prices (id, start_date, end_date, price) VALUES ('{}', '{}', NOW(), '{}')".format(id, old_date, old_price))
            cursor.execute(query)
        

        #now update the product table entry
        query = ("UPDATE products set name = '{}', price = {:f}, brand = '{}', category = '{}', variant = '{}', list = '{}' where id = {:d}".format(
            name, price, brand, category, variant, dataList, id
        ))
        cursor.execute(query)
    else:
        query = ("insert into products (id, name, last_update, price, brand, category, variant, list) VALUES ('{}', '{}', NOW(), '{}', '{}', '{}', '{}', '{}')".format(
            id, name, price, brand, category, variant, dataList
        ))
        cursor.execute(query)

    mydb.commit()
    cursor.close()

def cleanString(myString):
    myString = myString.replace('\"', '\\"')
    myString = myString.replace('\'', '\\\'')
    return myString