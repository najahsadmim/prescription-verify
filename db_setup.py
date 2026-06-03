import sqlite3
def init_hospital_database():
    connection=sqlite3.connect("hospital.db")
    cursor=connection.cursor()
    
    with open("hospital_registry.sql","r") as sql_file:
        sql_script=sql_file.read()
        
    cursor.executescript(sql_script)
    connection.commit()
    connection.close()
    print("Database constructed and pre-seeded with 50 certified records successfully!")
    
if __name__=="__main__":
    init_hospital_database()
    

