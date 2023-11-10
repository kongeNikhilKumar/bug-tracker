import json
import psycopg2

# Database connection parameters
db_params = {
    "database": "bug_tracker",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
}

# Read the JSON data from the file
with open('test_data.json', 'r') as file:
    json_data = json.load(file)

# Iterate over the JSON objects in the array
for item in json_data:
    # Extract data from the JSON
    user_data = item["user"]
    issue_data = {
        "title": item["title"],
        "user_id": user_data["id"],
        "state": item["state"],
        "created_at": item["created_at"],
        "updated_at": item["updated_at"],
        # Add other relevant fields
    }
    project_data = {
        "name": "Your project name",  # Replace with the actual project name
        "created_by_id": user_data["id"],
        # Add other relevant fields
    }
    member_data = {
        "project_id": "Your project ID",  # Replace with the actual project ID
        "member_id": user_data["id"],
        # Add other relevant fields
    }
    bug_data = {
        "title": "Your bug title",  # Replace with the actual bug title
        "description": "Your bug description",  # Replace with the actual bug description
        "priority": "low",  # Replace with the actual bug priority
        "project_id": "Your project ID",  # Replace with the actual project ID
        "created_by_id": user_data["id"],
        # Add other relevant fields
    }

    # Establish a database connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Insert data into the tables using raw SQL queries
    try:
        # Insert data into the "users" table
        user_insert_query = "INSERT INTO users (id, username, avatar_url) VALUES (%s, %s, %s);"
        cursor.execute(user_insert_query, (user_data["id"], user_data["login"], user_data["avatar_url"]))

        # Insert data into the "issues" table
        issue_insert_query = "INSERT INTO issues (title, user_id, state, created_at, updated_at) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(issue_insert_query, (issue_data["title"], issue_data["user_id"], issue_data["state"], issue_data["created_at"], issue_data["updated_at"]))

        # Insert data into the "projects" table
        project_insert_query = "INSERT INTO projects (name, created_by_id) VALUES (%s, %s);"
        cursor.execute(project_insert_query, (project_data["name"], project_data["created_by_id"]))

        # Insert data into the "members" table
        member_insert_query = "INSERT INTO members (project_id, member_id) VALUES (%s, %s);"
        cursor.execute(member_insert_query, (member_data["project_id"], member_data["member_id"]))

        # Insert data into the "bugs" table
        bug_insert_query = "INSERT INTO bugs (title, description, priority, project_id, created_by_id) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(bug_insert_query, (bug_data["title"], bug_data["description"], bug_data["priority"], bug_data["project_id"], bug_data["created_by_id"]))

        # Commit the changes
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
