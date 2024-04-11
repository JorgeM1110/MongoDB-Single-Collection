import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu

def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(db):

    # Create a "pointer" to the students collection within the db database.
    collection = db["department"]
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building_office: bool = False
    unique_description: bool = False
    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = -1
    description: str = ''
    while not unique_name or not unique_abbreviation or not unique_chair_name or not unique_building_office or not unique_description:

        name = input("Department name--> ")
        abbreviation = input("Department abbreviation--> ")
        chair_name = input("Chair name--> ")
        building = input("Building--> ")
        office = int(input("Office--> "))
        description = input("Description--> ")
        name_count: int = collection.count_documents({"name": name})
        unique_name = name_count == 0
        if not unique_name:
            print("Department with that name already exists.  Try again.")
        if unique_name:
            abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("Department with that abbreviation already exists.  Try again.")
            if unique_abbreviation:
                chair_name_count: int = collection.count_documents({"chair_name": chair_name})
                unique_chair_name = chair_name_count == 0
                if not unique_chair_name:
                    print("Department with that chair name already exists.  Try again.")
                if unique_chair_name:
                    unique_building_office_count: int = collection.count_documents({"building": building, "office": office})
                    unique_building_office = unique_building_office_count == 0
                    if not unique_building_office:
                        print("Department with that building and office already exists.  Try again.")
                    if unique_building_office:
                        unique_description_count: int = collection.count_documents({"description": description})
                        unique_description = unique_description_count == 0
                        if not unique_description:
                            print("Department with that description already exists.  Try again.")
    # Build a new department document preparatory to storing it
    department = {
        "name": name,
        "abbreviation": abbreviation,
        "chair_name": chair_name,
        "building": building,
        "office": office,
        "description": description,
    }
    results = collection.insert_one(department)


def select_department(db):

    # Create a connection to the students collection from this database
    collection = db["department"]
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    found_department = collection.find_one({"abbreviation": abbreviation})
    return found_department


def delete_department(db):
    department = select_department(db)
    # Create a "pointer" to the students collection within the db database.
    departments = db["department"]

    deleted = departments.delete_one({"name": department["name"]})

    print(f"We just deleted: {deleted.deleted_count} department.")


def list_department(db):

    departments = db["department"].find({}).sort([("name", pymongo.ASCENDING),
                                             ("abbreviation", pymongo.ASCENDING),
                                             ("chair_name", pymongo.ASCENDING),
                                             ("building", pymongo.ASCENDING),
                                             ("office", pymongo.ASCENDING),
                                             ("description", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)



if __name__ == '__main__':

    password: str = getpass.getpass('Mongo DB password -->')
    username: str = input('Database username [CECS-323-Spring-2023-user] -->') or \
                    "CECS-323-Spring-2023-user"
    project: str = input('Mongo project name [cecs-323-spring-2023] -->') or \
                   "CECS-323-Spring-2023"
    hash_name: str = input('7-character database hash [puxnikb] -->') or "puxnikb"
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())
    # department is our departments collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.
    # Connect to MongoDB Atlas

    departments = db["department"]
    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")

    # ************************** Set up the students collection
    departments_indexes = departments.index_information()
    if 'name' in departments_indexes.keys():
        print("name and abbr index present.")
    else:
        # Create a single UNIQUE index
        departments.create_index([('name', pymongo.ASCENDING)], unique=True, name='name')

    if 'abbreviation' in departments_indexes.keys():
        print("chair_name index present.")
    else:
        # Create a UNIQUE index on just the abbreviation
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name='abbreviation')

    if 'chair_name' in departments_indexes.keys():
        print("chair_name index present.")
    else:
        # Create a UNIQUE index on just the chair_name
        departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='chair_name')

    if 'building_office' in departments_indexes.keys():
        print("building and office index present.")
    else:
        # Create a UNIQUE index on both the building and office
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)], unique=True, name='building_office')
    pprint(departments.index_information())
    main_action: str = ''

    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)