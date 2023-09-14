import sqlite3

def create_db():
	db = sqlite3.connect('data.db') 
	cursor = db.cursor()
	
	cursor.execute("CREATE TABLE IF NOT EXISTS Users ( id integer unique, username text, refer integer, count_refer integer)")
	
	db.commit()
	
	cursor.execute("CREATE TABLE IF NOT EXISTS Recipes ( id integer, name text uniqe, recipe text)")
	
	db.commit()
	db.close()
	
def save_user(id, username, refer):    
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    
    exist_user = cursor.execute("SELECT id FROM Users WHERE id = ?", (id, )).fetchone()
    
    if exist_user is None:
        if refer != "":
            if int(refer) != int(id):    
                cursor.execute("INSERT INTO Users (id, username, refer, count_refer) VALUES (?,?,?, 0)",(id, username, refer))
                count_refer = cursor.execute("SELECT count_refer FROM Users WHERE id = ?",(refer,)).fetchone()[0]
                count_refer  += 1
                cursor.execute("UPDATE Users SET count_refer = ? WHERE id = ?", (count_refer,refer))
        else:
            cursor.execute("INSERT INTO Users (id, username, refer, count_refer) VALUES (?,?, null, 0)",(id, username))
        
    db.commit()
    db.close()
    
def count_referals(id):
	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	
	c = cursor.execute("SELECT count_refer FROM Users WHERE id = ?",(id,)).fetchone()[0]
	
	db.close()
	return c
	
def save_recipe(recipe, name, id):
	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	print(name)
	exist_name = cursor.execute("SELECT name FROM Recipes WHERE name = ?",(name,)).fetchone()
	#доделать, чтобы возвращалось сообщение о имеющимся рецепте
	if exist_name is None:
	    cursor.execute("INSERT INTO Recipes (id, name, recipe) VALUES (?,?,?)",(id, name, recipe))
	    db.commit()
	else:
	    print("такой уже есть")
	      
	db.close()
	
def all_recipes(id):
	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	
	c = cursor.execute("SELECT * FROM Recipes WHERE id =  ?",(id,)).fetchall()

	db.commit()
	db.close()
	return c
	
create_db()
