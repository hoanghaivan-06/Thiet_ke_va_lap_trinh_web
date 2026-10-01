Lab Answers

Part 1: SQL Warm-up and Constraints

1. What error did each of the four failing queries produce, and which constraint caused each error?

Query 1: Inserting a team with a duplicate name

The query returned a duplicate key value violates unique constraint error. This happened because the name column in the team table has a UNIQUE constraint. The name Avengers already existed in the database.

Query 2: Inserting a hero with an invalid team_id

The query returned a foreign key constraint error. The team_id column references the id column in the team table. Since team_id 99 does not exist, the database rejected the query.

Query 3: Inserting a hero without a name

The query returned a NOT NULL constraint error because the name column cannot be empty. Every new hero must have a name.

Query 4: Deleting a team with id 1

The query returned a foreign key constraint error because some heroes were still associated with the team with id 1. PostgreSQL did not allow the team to be deleted because doing so would affect the relationships between the tables.

Part 2: Project Setup and DATABASE_URL

2. Why read DATABASE_URL from an environment variable rather than hardcoding it into the Python files?

Using an environment variable helps protect sensitive information such as database usernames and passwords. It also prevents this information from being exposed when uploading code to GitHub.

Another reason is that the application may use different databases in development, testing, and production. Using an environment variable makes it easier to change the database connection without modifying the source code.

Part 3: Model Architecture

3. Why define multiple schemas instead of a single Hero class?

Using different schemas helps separate the data used for different purposes. For example, HeroPublic does not include secret_name, so sensitive information is not returned to the client.

HeroCreate is used when creating a new hero. The client does not need to provide an ID because the database generates it automatically.

HeroUpdate allows clients to update only the fields they want to change. This is useful for PATCH requests because the client does not have to send all the information every time.

Part 4: Database Engine and Sessions

4. Why should echo=True be disabled in production environments?

When echo=True is enabled, SQLAlchemy prints SQL statements to the logs. This can make the application slower because too many logs are generated.

It can also expose sensitive information in database queries. Therefore, it is better to disable echo=True in production to improve performance and protect user data.
![Screenshot 1](screenshot/screenshot1.png)

Part 5: Persistence and In-memory Comparison

5. Why did data persist after restarting the FastAPI server, unlike earlier lab exercises?

In earlier exercises, data was stored in Python lists or dictionaries in memory. When the application stopped, the data was lost.

In this lab, data is stored in PostgreSQL, which is a separate database service. Restarting the FastAPI server does not delete the data because it is stored in the database and not in the application's memory.
![Screenshot 2](screenshot/screenshot2.png)

Part 6: HTTP Status Codes and Database Filtering

6. Why return 409 Conflict instead of allowing PostgreSQL to raise a 500 Internal Server Error when a duplicate team is added?

A duplicate team name is a conflict with the existing data, so returning 409 Conflict is more appropriate than returning a 500 Internal Server Error.

By catching the IntegrityError, the application can return a clear error message to the client. This helps the client understand what went wrong and prevents the error from being treated as an unexpected server failure.

Part 9: Database Migrations

7. Why is SQLModel.metadata.create_all() insufficient for evolving production databases?

SQLModel.metadata.create_all() is useful for creating tables that do not already exist. However, it does not automatically update existing tables when the database structure changes.

For example, if we add a new column or change a data type, create_all() will not apply those changes to existing tables.

Alembic helps manage these changes by keeping track of database versions. It allows developers to upgrade or downgrade the database structure when needed, making it easier to maintain the database as the application grows.

![Screenshot 3](screenshot/screenshot3.png)

