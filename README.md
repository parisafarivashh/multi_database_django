
## Migrations for multi database
The migrate management command operates on one database at a time. 
By default, it operates on the default database, 
but by providing the --database option, 
you can tell it to synchronize a different database. 
So, to synchronize all models onto all databases in the first example above, 
you would need to call:

```
./manage.py migrate --database=default
./manage.py migrate --database=customers
```

## Automatic database routing
The easiest way to use multiple databases is to set up a database routing scheme. 
The default routing scheme ensures that objects remain ‘sticky’ 
to their original database (i.e., an object retrieved from the foo database will be saved on the same database).
The default routing scheme ensures that if a database isn’t specified, 
all queries fall back to the default database.

## Database routers
A database Router is a class that provides up to four methods:

1) db_for_read(model, **hints):
 ```
   Suggest the database that should be used for read operations for objects 
   of type model.

   If a database operation is able to provide any additional information that 
   might assist in selecting a database, it will be provided in the hints dictionary.
   
   Returns None if there is no suggestion.

   Hints:
     The hints received by the database router can be used to decide which
     database should receive a given request.
   ```
2) db_for_write(model, **hints)
                                                                                    
```
  Suggest the database that should be used for writes of objects of type Model.
```
3) allow_relation(obj1, obj2, **hints)¶
   
```
  Return True if a relation between obj1 and obj2 should be allowed, False 
  if the relation should be prevented, or None if the router has no opinion.
  This is purely a validation operation, used by foreign key and many to 
  many operations to determine if a relation should be allowed between two objects.
  If no router has an opinion (i.e. all routers return None), only relations 
  within the same database are allowed.
```
4) allow_migrate(db, app_label, model_name=None, **hints) 
    
```
   makemigrations always creates migrations for model changes, 
   but if allow_migrate() returns False, any migration operations for the
   model_name will be silently skipped when running migrate on the db. 
   Changing the behavior of allow_migrate() for models 
   that already have migrations may result in broken foreign keys, 
   extra tables, or missing tables. 
   When makemigrations verifies the migration history, 
   it skips databases where no app is allowed to migrate.
``` 
 
 A router doesn’t have to provide all these methods – it may omit one or 
 more of them.  
 If one of the methods is omitted, Django will skip that router when performing the relevant check.
-----------------------------------
Database routers are installed using the DATABASE_ROUTERS setting.  
This setting defines a list of class names, 
each specifying a router that should be used by the base router (django.db.router).
  
## Manually selecting a database for a QuerySet

You can select the database for a QuerySet at any point in the QuerySet “chain.”

Call using() on the QuerySet to get another QuerySet that uses the 
specified database.
#### using() : 
#### takes a single argument: the alias of the database on which you want to run the query.
```
>>> # This will run on the 'default' database.
>>> Author.objects.all()

>>> # So will this.
>>> Author.objects.using('default')

>>> # This will run on the 'other' database.
>>> Author.objects.using('other')
```
### Selecting a database for save()
Use the using keyword to Model.save() to specify to which database the data should be saved.

```
>>> my_object.save(using='other')
```

#### Moving an object from one database to another

```
>>> p = Person(name='Fred')
>>> p.save(using='default')  # (statement 1)
>>> p.save(using='other') # (statement 2)
```

in statement 1, a new Person object is saved to the first database. At this 
time, p doesn’t have a primary key, so Django issues an SQL INSERT statement. This creates a primary key, and Django assigns that primary key to p.

When the save occurs in statement 2, p already has a primary key value, and Django will attempt to use that primary key on the new database. If the primary key value isn’t in use in the second database, then you won’t have any problems – the object will be copied to the new database.

However, if the primary key of p is already in use on the second database, the existing object in the second database will be overridden when p is saved.

You can avoid this in two ways. First, you can clear the primary key of the instance. If an object has no primary key, Django will treat it as a new object, avoiding any loss of data on the second database:


```
>>> p = Person(name='Fred')
>>> p.save(using='first')
>>> p.pk = None # Clear the primary key.
>>> p.save(using='second') # Write a completely new object.
```
The second option is to use the force_insert option to save() to ensure 
that Django does an SQL INSERT:

```
>>> p = Person(name='Fred')
>>> p.save(using='first')
>>> p.save(using='second', force_insert=True)
```

### Selecting a database to delete from
```
>>> u = User.objects.using('legacy_users').get(username='fred')
>>> u.delete() # will delete from the `legacy_users` database
```

### Using managers with multiple databases¶
Use the db_manager() method on managers to give managers access to a non-default database.
For example, say you have a custom manager method that touches the database – User.objects.create_user().
##### Because create_user() is a manager method, not a QuerySet method, 
##### you can’t do User.objects.using('new_users').create_user(). 
##### (The create_user() method is only available on User.objects, 
the manager, not on QuerySet objects derived from the manager) 
The solution is to use db_manager(), like this:
```
User.objects.db_manager('new_users').create_user(...)
```
#### db_manager() returns a copy of the manager bound to the database you specify.

---------------------------------------------------------
Django doesn’t currently provide any support for foreign key or many-to-many relationships spanning multiple databases. If you have used a router to partition models to different databases, any foreign key and many-to-many relationships defined by those models must be internal to a single database.

```
This is because of referential integrity. 
In order to maintain a relationship between two objects, 
Django needs to know that the primary key of the related object is valid. 
If the primary key is stored on a separate database, 
it’s not possible to easily evaluate the validity of a primary key.
```





