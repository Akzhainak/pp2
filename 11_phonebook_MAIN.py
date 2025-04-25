import psycopg2
import csv

def get_conn():
    return psycopg2.connect(
        dbname="phonebook",
        user="postgres",
        password="2121",
        host="localhost",
        port="5432"
    )

def create_table():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS phonebook(
                    id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone BIGINT NOT NULL
                )
            ''')
            conn.commit()

def insert_csv():
    with get_conn() as conn:
        with conn.cursor() as cur:
            with open('phonfile.csv', 'r') as f:
                reader = csv.reader(f, delimiter=';')
                next(reader)
                for row in reader:
                    if len(row) >= 4 and row[1] and row[2] and row[3]:
                        cur.execute(
                            '''INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s)''',
                            (row[1], row[2], row[3])
                        )
            conn.commit()

def console():
    first_name = input("write the first name: ")
    last_name = input("write the last name: ")
    phone = input("write the phone: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s)", (first_name, last_name, phone))
            conn.commit()

def up_all():
    old_fname = input("write the old name: ")
    new_fname = input("write the new name: ")
    new_lname = input("write the new last name: ")
    nphone = input("write the new phone: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET first_name=%s, last_name=%s, phone=%s WHERE first_name=%s", (new_fname, new_lname, nphone, old_fname))
            conn.commit()

def up_fname():
    old_fname = input("write the old name: ")
    new_fname = input("write the new first name: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET first_name=%s WHERE first_name=%s", (new_fname, old_fname))
            conn.commit()

def up_lname():
    old_lname = input("write the old name: ")
    new_lname = input("write the new last name: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET last_name=%s WHERE last_name=%s", (new_lname, old_lname))
            conn.commit()

def up_ph():
    old_phone = input("write the old phone: ")
    nphone = input("write the new phone: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET phone=%s WHERE phone=%s", (nphone, old_phone))
            conn.commit()

def q_fname():
    first_name = input("Enter first name to search: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{first_name}%",))
            for row in cur.fetchall():
                print(row)

def q_lname():
    last_name = input("Enter last name to search: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE last_name ILIKE %s", (f"%{last_name}%",))
            for row in cur.fetchall():
                print(row)

def q_ph():
    phone = input("Enter phone to search: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE phone::text ILIKE %s", (f"%{phone}%",))
            for row in cur.fetchall():
                print(row)

def mul_del_id():
    ids = input("Enter id-s to delete (comma separated): ")
    id_list = [id_str.strip() for id_str in ids.split(',') if id_str.strip().isdigit()]
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
    fname = input("Enter first name to delete: ")
    lname = input("Or enter last name to delete: ")
    phone = input("Or enter phone to delete: ")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE first_name = %s OR last_name = %s OR phone = %s", (fname, lname, phone))
            conn.commit()

def pattern_fun():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE OR REPLACE FUNCTION find_pattern(pattern TEXT)
                RETURNS TABLE (id INT, first_name TEXT, last_name TEXT, phone BIGINT)
                AS $$
                BEGIN
                    RETURN QUERY
                    SELECT * FROM phonebook
                    WHERE first_name ILIKE '%' || pattern || '%'
                    OR last_name ILIKE '%' || pattern || '%'
                    OR phone::TEXT ILIKE '%' || pattern || '%';
                END;
                $$ LANGUAGE plpgsql;
            """)
            conn.commit()

def insert_or_up():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE OR REPLACE PROCEDURE insert_or_up(
                    in_fname TEXT,
                    in_lname TEXT,
                    in_phone BIGINT
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM phonebook WHERE first_name = in_fname AND last_name = in_lname
                    ) THEN
                        UPDATE phonebook SET phone = in_phone WHERE first_name = in_fname AND last_name = in_lname;
                    ELSE
                        INSERT INTO phonebook(first_name, last_name, phone)
                        VALUES (in_fname, in_lname, in_phone);
                    END IF;
                END;
                $$;
            """)
            conn.commit()

def create_insert_mul_users():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE OR REPLACE PROCEDURE insert_mul_users(
                    names TEXT[],
                    phones TEXT[],
                    OUT invalid_entries TEXT[]
                )
                LANGUAGE plpgsql
                AS $$
                DECLARE
                    i INT;
                BEGIN
                    invalid_entries := '{}';
                    FOR i IN 1..array_length(names, 1) LOOP
                        IF phones[i] ~ '^[0-9]{6,15}$' THEN
                            CALL insert_or_up(
                                split_part(names[i], ' ', 1),
                                split_part(names[i], ' ', 2),
                                phones[i]::BIGINT
                            );
                        ELSE
                            invalid_entries := array_append(invalid_entries, names[i] || ' - ' || phones[i]);
                        END IF;
                    END LOOP;
                END;
                $$;
            """)
            conn.commit()

def get_users_fun():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE OR REPLACE FUNCTION get_users(limit_num INT, offset_num INT)
                RETURNS TABLE (id INT, first_name TEXT, last_name TEXT, phone BIGINT)
                AS $$
                BEGIN
                    RETURN QUERY
                    SELECT * FROM phonebook
                    ORDER BY id
                    LIMIT limit_num OFFSET offset_num;
                END;
                $$ LANGUAGE plpgsql;
            """)
            conn.commit()

def create_delete_by_name_or_phone():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(
                    in_first TEXT,
                    in_last TEXT,
                    in_phone TEXT
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    DELETE FROM phonebook
                    WHERE first_name = in_first
                       OR last_name = in_last
                       OR phone::TEXT = in_phone;
                END;
                $$;
            """)
            conn.commit()

def create_all_sql_objects():
    pattern_fun()
    insert_or_up()
    create_insert_mul_users()
    get_users_fun()
    create_delete_by_name_or_phone()

if __name__ == "__main__":
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
            print('''update:
                1. all
                2. first name
                3. last name
                4. phone
            ''')
            up = input("choose: ")
            if up == '1':
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
            qc = input("choose: ")
            if qc == '1':
                q_fname()
            elif qc == '2':
                q_lname()
            elif qc == '3':
                q_ph()
            else:
                print("Invalid choice. Try again.")
        elif choice == '5':
            print("""deleting:
                1. one user
                2. with id multiple users""")
            d = input("choose: ")
            if d == '1':
                delt()
            elif d == '2':
                mul_del_id()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Try again.")
