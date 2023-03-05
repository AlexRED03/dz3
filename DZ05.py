import psycopg2
     

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            surname VARCHAR(40) NOT NULL,
            email VARCHAR(40) NOT NULL
        );
        """)
        conn.commit()
    # with conn.cursor() as cur:  
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id SERIAL PRIMARY KEY,
            client_tell VARCHAR(40) ,
            client_id INTEGER NOT NULL REFERENCES client(id)
        );
        """)
        conn.commit()
    


def add_client(conn, name, surname, email, tell=None):
    with conn.cursor() as cur:
        cur.execute ("""
        INSERT INTO client (name, surname, email) VALUES(%s, %s, %s);
        """, (name, surname, email))
        conn.commit()

        cur.execute("""
            SELECT id FROM client WHERE name=%s;
            """, (name,))
        c = cur.fetchone()[0]

        if tell != None:
            cur.execute ("""
            INSERT INTO phone (client_tell, client_id) VALUES (%s, %s);
            se
            """, (tell, c))
            conn.commit()
            
        # else:
            # cur.execute ("""
            # INSERT INTO phone (client_tell, client_id) VALUES (%s, %s);
            # """, (0, c))
            # conn.commit()
            

def add_tell(conn, client_id, tell):
    with conn.cursor() as cur:
        cur.execute ("""
        INSERT INTO phone (client_tell, client_id) VALUES(%s, %s);
        """, (tell, client_id))
        conn.commit()

def change_client(conn, id, name=None, surname=None, email=None, tell=None):
    with conn.cursor() as cur:
        cur.execute ("""
        UPDATE client SET name=%s, surname=%s, email=%s WHERE id=%s;
        """, (name, surname, email, id))
        conn.commit()
        cur.execute ("""
        UPDATE phone SET client_tell=%s WHERE client_id=%s;
        """, (tell, id))
        conn.commit()

def delete_tell(conn, client_id, tell):
    with conn.cursor() as cur:
        cur.execute ("""
        DELETE FROM phone WHERE client_id=%s and client_tell=%s;
        """, (client_id, tell))
        conn.commit()

def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute ("""
        DELETE FROM client WHERE id=%s;
        """, (id))
        conn.commit()

def find_client(conn, name=None, surname=None, email=None, tell=None):
    name=(name)
    surname = (surname)
    email = (email)
    with conn.cursor() as cur:
        cur.execute ("""
        SELECT * FROM client
        join phone on phone.client_id = client.id
        WHERE name=%s or surname=%s or email=%s or client_tell=%s;
        """, (name, surname, email, tell))
        return cur.fetchone()



"""" Тесты """

with psycopg2.connect(database="test_db", user="postgres", password="1234") as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)

    create_db(conn)
    add_client(conn, 'Alex', 'RRRRRR', 'kkkkkkkk', tell=None)
    add_client(conn, 'Alex2', 'RRRRRR2', 'kkkkkkkk2', tell=None)
    add_client(conn, 'Alex3', 'RRRRRR3', 'kkkkkkkk3', tell=None)

    add_tell(conn, 1, 45675674676)
    add_tell(conn, 2, 334543534534)
    add_tell(conn, 3, 456777643443)
   

    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM client;
            """)
        print('fetchall', cur.fetchall()) 
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM phone;
            """)
        print('fetchall', cur.fetchall()) 


    # change_client(conn, 1, name='dfggg', surname='dfgdfgdfg', email='sdfdfdff', tell='12323232133')

    # with conn.cursor() as cur:
    #     cur.execute("""
    #         SELECT * FROM client;
    #         """)
    #     print('fetchall', cur.fetchall()) 
    # with conn.cursor() as cur:
    #     cur.execute("""
    #         SELECT * FROM phone;
    #         """)
    #     print('fetchall', cur.fetchall()) 

    # delete_tell(conn, 1, '12323232133')
    # with conn.cursor() as cur:
    #     cur.execute("""
    #         SELECT * FROM phone;
    #         """)
    #     print('fetchall', cur.fetchall()) 

    # delete_client(conn, '1')
    # with conn.cursor() as cur:
    #     cur.execute("""
    #         SELECT * FROM client;
    #         """)
    #     print('fetchall', cur.fetchall())

    z =find_client(conn, name=None, surname=None, email=None, tell='45675674676')
    print(z)


conn.close()