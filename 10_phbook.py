import psycopg2
import csv

def get_conn():
    
    conn = psycopg2.connect(
        dbname="phonebook", #dadtabase name
        user="postgres", #replace with your postgresql username
        password ="2121", #replace with your postgresql password
        host="localhost", #local host
        port="5432" #default postgre port
    )
    return conn


#cur = get_conn().cursor()   # cursor is a database object used to retrieve and manipulate rows from a query result one at a time.
     

def create_table():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS phonebook(
                id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name  TEXT NOT NUll,
                phone  BIGINT NOT NULL
                )
                ''')
            conn.commit()

def insert_csv():
    with get_conn() as conn:
        with conn.cursor() as cur:
            with open('phonfile.csv', 'r') as f:
                reader = csv.reader(f, delimiter=';')  
                next(reader)  # skip header
                for row in reader:
                    if len(row) >= 4:  # lenght of row
                        cur.execute(
                            '''
                            INSERT INTO phonebook (first_name, last_name, phone)
                            VALUES (%s, %s, %s)
                            ''',
                            (row[1], row[2], row[3])  # skip id
                        )
            conn.commit()


#inserting feom console
def console():
    first_name=input("write the first name: ")
    last_name=input("write the last name: ")
    phone=input("write the phone: ")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (first_name,last_name,phone) VALUES (%s,%s,%s)",(first_name,last_name,phone))
            conn.commit()

        

#upating user info
def up_all():
    old_fname=input("write the old name: ")
    new_fname=input("write the new name: ")
    new_lname=input("write tne new last name: ")
    nphone=input("write the new phone: ")
    with get_conn() as conn:
        with conn.cursor() as cur :
            cur.execute("UPDATE phonebook SET first_name=%s, last_name=%s, phone=%s WHERE first_name=%s",(new_fname,new_lname,nphone,old_fname))
            conn.commit()


#change only fname
def up_fname():
    old_fname=input("write the old name: ")
    new_fname=input("write the new first name: ")
    with get_conn() as conn:
        with conn.cursor() as cur :
            cur.execute("UPDATE phonebook SET first_name=%s  WHERE first_name=%s",(new_fname,old_fname))
            conn.commit()



#change only last name
def up_lname():
    old_lname=input("write the old name: ")
    new_lname=input("write tne last name: ")
    with get_conn() as conn:
        with conn.cursor() as cur :
            cur.execute("UPDATE phonebook SET  last_name=%s WHERE last_name=%s",(new_lname,old_lname))
            conn.commit()



#change phone
def up_ph():
    old_phone=input("write the old name: ")
    nphone=input("write the new phone: ")
    with get_conn() as conn:
        with conn.cursor() as cur :
            cur.execute("UPDATE phonebook SET phone=%s WHERE phone=%s",(nphone,old_phone))
            conn.commit()



#quering fst name
def q_fname():
    first_name= input("Enter first name to search: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{first_name}%",))
            rows = cur.fetchall()
            for row in rows:
                print(row)
            



#quering lst name
def q_lname():
    last_name=input("enter last name to search: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE last_name ILIKE %s",(f"%{last_name}%",))
            rows=cur.fetchall()
            for row in rows:
                print(row)

            



#quering phones 
def q_ph():
    phone=input("enter phone to search: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE phone :: text ILIKE %s",(f"%{phone}%",))
            rows=cur.fetchall()
            for row in rows:
                print(row)

            

def mul_del_id():
    ids=input("enter id-s to delete (comma seperated): ")
    id_list = []
    for id_str in ids.split(','):
        id_str = id_str.strip()  # del space front back
        if id_str.isdigit():     # only digit?
            id_list.append(id_str) 

    if not id_list:
        print("No valid IDs provided.")
        return

    placeholders = ','.join(['%s'] * len(id_list))

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM phonebook WHERE id IN ({placeholders})", id_list)
            conn.commit()
            print(f"{cur.rowcount} record(s) deleted.")


def delt():
    fname = input("enter first name to delete: ")
    lname = input("or enter last name to delete: ")
    phone = input("or enter phone to delete: ")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE first_name = %s OR last_name=%s OR phone = %s", (fname,lname, phone))
            conn.commit()




create_table()
while True:
    print("""
    1. insert from csv
    2. insert from console
    3. update 
    4. query 
    5. delete user
    6. exit
        """)
    choice = input("choose: ")
    if choice == '1':
        insert_csv()
    elif choice == '2':
        console()
    elif choice == '3':
        print('''upadte:
              1. all
              2. first name
              3. last name
              4. phone
              ''')
        up=input("choose:")
        if up =='1':
            up_all()
        elif up == '2':
            up_fname()
        elif up == '3':
            up_lname()
        elif up == '4':
            up_ph()
        else:
            print("Invalid choice. Try again.")
    elif choice == '4':
        print('''query:
              1. first name
              2. last name
              3. phone
              ''')
        q=input("choose:")
        if q =='1':
            q_fname()
        elif q == '2':
            q_lname()
        elif q == '3':
            q_ph()
        else:
            print("Invalid choice. Try again.")
    elif choice == '5':
        print("""deleting:
              1. one user
              2. with id mul users""")
        d=input("chooose: ")
        if d == '1':
            delt()
        elif d =='2':
            mul_del_id()
    elif choice == '6':
        break
    else:
        print("Invalid choice. Try again.")