import psycopg2

#  День 4: Python ↔ PostgreSQL (psycopg2)
def main (object):
    # Замените на свои данные из Neon/Supabase
    conn = psycopg2.connect(
        dbname="postgres", user="postgres.eaqvvnzcjdesmqghmphk", password="ZacrqkY5SvzJHlVv",
        host="aws-1-eu-central-1.pooler.supabase.com", port=5432
    )
    cur = conn.cursor()
    
    print("username: ")
    username = input()
    print("email: ")
    email = input()
    cur.execute("INSERT INTO users (username, email) VALUES (%s, %s);", (username, email))
    conn.commit()

    cur.execute("SELECT username FROM users LIMIT 100;")
    print(cur.fetchall())    
    cur.close(); conn.close()
# end match

if __name__ == "__main__":
    main(None)
# end main