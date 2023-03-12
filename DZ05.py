import psycopg2
     

def create_db(cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            surname VARCHAR(40) NOT NULL,
            email VARCHAR(40) NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id SERIAL PRIMARY KEY,
            client_tell VARCHAR(40) ,
            client_id INTEGER NOT NULL REFERENCES client(id)
        );
        """)
       
    


def add_client(cur, name, surname, email, tell=None):
        cur.execute ("""
            INSERT INTO client (name, surname, email) VALUES(%s, %s, %s);
        """, (name, surname, email))
        
        cur.execute("""
            SELECT id FROM client WHERE name=%s;
            """, (name,))
        c = cur.fetchone()[0]

        if tell != None:
            cur.execute ("""
            INSERT INTO phone (client_tell, client_id) VALUES (%s, %s);
            """, (tell, c))
            
            
                    

def add_tell(cur, client_id, tell):
        cur.execute ("""
        INSERT INTO phone (client_tell, client_id) VALUES(%s, %s);
        """, (tell, client_id))
        

def change_client(cur, id, name=None, surname=None, email=None, tell=None):
    if name != None:
        cur.execute ("""
        UPDATE client SET name=%s WHERE id=%s;
        """, (name, id))
    if surname != None:
        cur.execute ("""
        UPDATE client SET surname=%s WHERE id=%s;
        """, (surname, id))
    if email != None:
        cur.execute ("""
        UPDATE client SET email=%s WHERE id=%s;
        """, (email, id))
    if tell != None:    
        cur.execute ("""
        UPDATE phone SET client_tell=%s WHERE client_id=%s;
        """, (tell, id))
        

def delete_tell(cur, client_id, tell):
        cur.execute ("""
        DELETE FROM phone WHERE client_id=%s and client_tell=%s;
        """, (client_id, tell))
        

def delete_client(cur, id):
        cur.execute ("""
        DELETE FROM client WHERE id=%s;
        """, (id))
        conn.commit()

def find_client(cur, name=None, surname=None, email=None, tell=None):
    name=(name)
    surname = (surname)
    email = (email)
    cur.execute ("""
        SELECT * FROM client
        join phone on phone.client_id = client.id
        WHERE name=%s and surname=%s and email=%s and client_tell=%s;
        """, (name, surname, email, tell))
    return cur.fetchall()




if __name__ == "__main__":

    with psycopg2.connect(database="test_db", user="postgres", password="1234") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE phone;
            DROP TABLE client;
            """)

            create_db(cur)
            add_client(cur,'Alex', 'RRRRRR', 'kkkkkkkk', tell=None)
            add_client(cur,'Alex2', 'RRRRRR2', 'kkkkkkkk2', tell=None)
            add_client(cur,'Alex2', 'RRRRRR3', 'kkkkkkkk3', tell=None)

            add_tell(cur,1, 45675674676)
            add_tell(cur,2, 45675456674676)
            add_tell(cur,3, 456777643443)
    

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


            # change_client(cur, 1, name='dfggg', surname='dfgdfgdfg', email='sdfdfdff', tell='12323232133')

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

            z =find_client(cur, name='Alex2', surname='RRRRRR3', email='kkkkkkkk3', tell="456777643443")
            print(z)


    conn.close()