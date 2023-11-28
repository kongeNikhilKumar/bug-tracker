import json
import psycopg2
import random
import uuid
# Database connection parameters
db_params = {
    "database": "bug_tracker",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
}
from psycopg2.extensions import AsIs
# Read the JSON data from the file
with open('./data/pallets_issues.json', 'r') as file:
    json_data = json.load(file)
index = 0
# Iterate over the JSON objects in the array
for item in json_data:
    # Extract data from the JSON
    if(index > 150) : break
    username = []
    user_data = item["user"]
    # 523f5443-c9b7-4b3c-b604-b360fa56143a angular
    # f1a1678a-426e-4111-a76e-f68e2d24b83c flask
    member_data = {
        "project_id": "f1a1678a-426e-4111-a76e-f68e2d24b83c",  # Replace with the actual 
    }
    priorities = ["low", "high", "medium"]
    random_priority = random.choice(priorities)

    bug_data = {
        "title": item['title'],  # Replace with the actual bug title
        "description": item['body'],  # Replace with the actual bug description
        "priority": random_priority,  # Replace with the actual bug priority
        "project_id": 1,  # Replace with the actual project ID
        "created_by_id": user_data["id"],
        "state" : item['state']
    }

    # Establish a database connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    usersList = {}
    # Insert data into the tables using raw SQL queries
    try:
        # Insert data into the "users" table
        
        if user_data["login"] not in usersList.keys():
            user_id = str(uuid.uuid4())
            formatted_user_id = str(uuid.UUID(user_id))

            user_insert_query = 'INSERT INTO users (id, username, "passwordHash") VALUES (%s, %s, %s)'
            cursor.execute(user_insert_query, ( formatted_user_id, user_data["login"] , "password" ))

            # Insert data into the "members" table
            formatted_project_id = str(uuid.UUID(member_data['project_id']))
            print("****************")
            print(member_data['project_id'])
            print("****************")
            member_insert_query = 'INSERT INTO members ("projectId", "memberId") VALUES (%s, %s);'
            cursor.execute(member_insert_query, (member_data['project_id'],formatted_user_id))

            usersList[user_data['login']] = formatted_user_id
        else :
            formatted_user_id = usersList[user_data['login']]
        # Insert data into the "bugs" table
        bug_description = bug_data["description"]
        if  bug_description and bug_description.strip(): 

            bug_description = bug_description[0 : 300]
            bug_title = bug_data["title"][0:59]
            bug_insert_query = 'INSERT INTO bugs (id,title, description, priority, "projectId", "createdById", state) VALUES ( %s,%s, %s, %s, %s, %s , %s);'
            cursor.execute(bug_insert_query, (str(uuid.uuid4()),bug_title, bug_description.strip(), bug_data["priority"], formatted_project_id, formatted_user_id, bug_data['state']))

            # Commit the changes
            conn.commit()
            index +=1
    except Exception as e:
        print(len(usersList))
        conn.rollback()
        raise e
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
    
print(len(usersList.keys()))
