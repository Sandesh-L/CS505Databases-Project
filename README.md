
You need to install flask, jinja3, and pymongo to get started on the project. Use venv if you can

Contorllers has the logic, models has the database schemas and other databse stuff, and templates has the html

to start orient db run `sudo docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=root orientdb:2.2`

All routes are currently in app.py