from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['CECS-323-Spring-2024']

db.createCollection('department',
    validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'title': 'department',
            'required': ['name', 'abbreviation', 'chair_name', 'building', 'office', 'description'],
            'properties': {
                'name': {
                    'bsonType': 'string',
                    'maxLength': 50
                },
                'abbreviation': {
                    'bsonType': 'string',
                    'maxLength': 6
                },
                'chair_name': {
                    'bsonType': 'string',
                    'maxLength': 80
                },
                'building': {
                    'bsonType': 'string',
                    'maxLength': 10
                },
                'office': {
                    'bsonType': 'int'
                },
                'description': {
                    'bsonType': 'string',
                    'maxLength': 80
                }
            }
        }
    }
);


client.close()




