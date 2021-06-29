import peewee

database = peewee.PostgresqlDatabase("postgres", user="postgres", password="admin")

def split_name(name):
  name = name.split(" ")
  if ("vel" in name):
    #👀 at you Szymon Szynkowski vel Sęk
    first_name = " ".join(name[-1:])
    last_name = " ".join(name[0:3])
  else:
    first_name = " ".join(name[1:])
    last_name = name[0]

  return first_name, last_name

class BaseModel(peewee.Model):
  class Meta:
    database = database

class Sitting(BaseModel):
  number = peewee.IntegerField()

class Day(BaseModel):
  date = peewee.DateField()
  sitting = peewee.ForeignKeyField(Sitting)

class Vote(BaseModel):
  number = peewee.IntegerField()
  title = peewee.CharField(max_length=1024)
  day = peewee.ForeignKeyField(Day)

class Deputy(BaseModel):
  first_name = peewee.CharField()
  last_name = peewee.CharField()
  party = peewee.CharField()

class Result(BaseModel):
  result = peewee.IntegerField()
  deputy = peewee.ForeignKeyField(Deputy)
  vote = peewee.ForeignKeyField(Vote)

if __name__ == "__main__":
  #DANGER ZONE
  if ("sitting" not in database.get_tables()):
    print("Dropping all tables...")
    database.drop_tables(models=[Sitting, Day, Vote, Deputy, Result])
    print("Done.")
    print("Creating new tables...")
    try:
      Sitting.create_table()
      Day.create_table()
      Deputy.create_table()
      Vote.create_table()
      Result.create_table()
    except Exception as e:
      print(e)
    print("Done.")