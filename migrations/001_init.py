"""Peewee migrations -- 001_init.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    @migrator.create_model
    class BaseModel(pw.Model):
        id = pw.AutoField()

        class Meta:
            table_name = "basemodel"

    @migrator.create_model
    class Sitting(pw.Model):
        id = pw.AutoField()
        number = pw.IntegerField()

        class Meta:
            table_name = "sitting"

    @migrator.create_model
    class Day(pw.Model):
        id = pw.AutoField()
        date = pw.DateField()
        sitting = pw.ForeignKeyField(column_name='sitting_id', field='id', model=migrator.orm['sitting'])

        class Meta:
            table_name = "day"

    @migrator.create_model
    class Deputy(pw.Model):
        id = pw.AutoField()
        first_name = pw.CharField(max_length=255)
        last_name = pw.CharField(max_length=255)
        party = pw.CharField(max_length=255)

        class Meta:
            table_name = "deputy"

    @migrator.create_model
    class Vote(pw.Model):
        id = pw.AutoField()
        number = pw.IntegerField()
        total_votes = pw.IntegerField()
        time = pw.TimeField()
        title = pw.CharField(max_length=2048)
        day = pw.ForeignKeyField(column_name='day_id', field='id', model=migrator.orm['day'])

        class Meta:
            table_name = "vote"

    @migrator.create_model
    class PartyResult(pw.Model):
        id = pw.AutoField()
        party = pw.CharField(max_length=255)
        result = pw.FloatField()
        vote = pw.ForeignKeyField(column_name='vote_id', field='id', model=migrator.orm['vote'])

        class Meta:
            table_name = "partyresult"

    @migrator.create_model
    class Result(pw.Model):
        id = pw.AutoField()
        result = pw.IntegerField()
        deputy = pw.ForeignKeyField(column_name='deputy_id', field='id', model=migrator.orm['deputy'])
        vote = pw.ForeignKeyField(column_name='vote_id', field='id', model=migrator.orm['vote'])

        class Meta:
            table_name = "result"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_model('result')

    migrator.remove_model('partyresult')

    migrator.remove_model('vote')

    migrator.remove_model('deputy')

    migrator.remove_model('day')

    migrator.remove_model('sitting')

    migrator.remove_model('basemodel')
