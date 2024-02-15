import os
import psycopg2
from schemas import court_schema, user_schemas, court_headings


def build():
  ''' Builds the database '''
  try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cursor = conn.cursor()

    for table in user_schemas:
      cursor.execute(table)

    for heading in court_headings:
      cursor.execute(court_schema.format(table_name=heading))

    conn.commit()
    conn.close()
    return{"message":"Database Created Sucessfully"}
  except Exception as e:
    return {"error":e}

