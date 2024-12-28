from dotenv import load_dotenv
from os import environ as env
import peewee
import playhouse.postgres_ext as psql

load_dotenv()

database = psql.PostgresqlExtDatabase(env.get("POSTGRES_DB"), user=env.get("POSTGRES_USER"), password=env.get("POSTGRES_PASSWORD"), host="localhost", port="5432")

class BaseModel(peewee.Model):
  class Meta:
    database = database

class Term(BaseModel):
  start = peewee.DateField()
  end = peewee.DateField(null=True)

class Club(BaseModel):
  full_name = peewee.CharField()
  sejm_id = peewee.CharField()
  term = peewee.ForeignKeyField(Term, backref="clubs")

class Sitting(BaseModel):
  number = peewee.IntegerField()
  days = psql.ArrayField(peewee.DateField)
  term = peewee.ForeignKeyField(Term, backref="sittings")

class Vote(BaseModel):
  number = peewee.IntegerField()
  total_votes = peewee.IntegerField()
  time = peewee.TimeField()
  title = peewee.CharField(max_length=2048)
  sitting = peewee.ForeignKeyField(Sitting, backref="votes")

class Deputy(BaseModel):
  first_name = peewee.CharField()
  last_name = peewee.CharField()
  birthday = peewee.DateField()
  district_num = peewee.IntegerField()
  sejm_id = peewee.IntegerField()
  term = peewee.ForeignKeyField(Term, backref="mps")
  club = peewee.ForeignKeyField(Club, backref="mps")

class Result(BaseModel):
  result = peewee.IntegerField()
  deputy = peewee.ForeignKeyField(Deputy)
  vote = peewee.ForeignKeyField(Vote, backref="results")

class PartyResult(BaseModel):
  party = peewee.CharField()
  result = peewee.FloatField()
  vote = peewee.ForeignKeyField(Vote, backref="votes")

if __name__ == "__main__":
  #DANGER ZONE
  if ("sitting" not in database.get_tables()):
    print("Dropping all tables...")
    database.drop_tables(models=[Term, Club, Sitting, Vote, Deputy, Result, PartyResult])
    print("Done.")
    print("Creating new tables...")
    try:
      Term.create_table()
      Club.create_table()
      Sitting.create_table()
      Deputy.create_table()
      Vote.create_table()
      Result.create_table()
      PartyResult.create_table()
    except Exception as e:
      print(e)
    print("Done.")
