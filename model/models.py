import psycopg2
import pandas as pd 

def connect_to_db():
  db_connection = psycopg2.connect(
    host="***.***.***.**",
    database="********",
    user="*********",
    password="********")
  db_connection.set_session(autocommit=True)
  cursor = db_connection.cursor()
  cursor.execute('SELECT version()')
  db_version = cursor.fetchone()
  print(db_version)
  return db_connection,cursor


conn,db=connect_to_db()
def create_table():
  try:
    table_creation="""
                    CREATE TABLE newscrawler (
                    id serial PRIMARY KEY,
                    title VARCHAR ( 500 ) ,
                    text VARCHAR ( 2000 ) ,
                    time TIMESTAMP ,
                    newsource VARCHAR ( 500 ) ,
                    image VARCHAR ( 500 ) ,
                    country VARCHAR ( 500 ) ,
                    countrycode VARCHAR ( 500 ) ,
                    newslet VARCHAR ( 500 ) ,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                  );
                """

    db.execute(table_creation)
    db.close()
    return True   
  except Exception as e :
    print("error:",e)
    return False
  
def insert_to_db(new_source,data=None):
  if data is None:
    data=[]
  try:
    record_to_insert=[]
    if len(data)>0:
      for d in data:
        checkrecord=record_exists(d['title'])
        print("checkrecord:",checkrecord)
        if not checkrecord:
          title=str(d['title']).replace("'","''") if 'title' in d else None
          text=d['text'] if 'text' in d else None
          time=d['time'] if 'time' in d else None
          newsource=new_source
          image=d['image'] if 'image' in d else None
          country=d['country'] if 'country' in d else None
          countrycode=d['countrycode'] if 'countrycode' in d else None
          newslet=d['newslet'] if 'newslet' in d else None
          db_data=(title,text,time,newsource,image,country,countrycode,newslet)
          record_to_insert.append(db_data)

    db_insert_query = """ INSERT INTO newscrawler (title, text, time,newsource,image,country,countrycode,newslet) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    for record in record_to_insert :
      db.execute(db_insert_query, record)
      conn.commit()
    return True
  except Exception as e :
    print("error:",e)
    return False


def record_exists(title):
  title=str(title).replace("'","''")
  query="""SELECT id FROM newscrawler WHERE title = '{title}'""".format(title=title)
  db.execute(query)
  return db.fetchone() is not None



if __name__ == '__main__':
  # print(create_table())
  df = pd.read_csv("news.csv") 
  data=df.to_dict(orient='records')
  print(insert_to_db('news247',data))
