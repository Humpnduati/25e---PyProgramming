from unittest import result
from pymongo import MongoClient
client = MongoClient('mongodb+srv://nduatihump:zOqKwMyCiuOXjX4K@cluster0.wcyfmwi.mongodb.net/')
db = client.School  
Students_collection = db.Students

student_document ={
    'firstName': 'John',
    'lastName': 'Doe',
    'age': 14,
    'grade': '9th',
    'courses': ['Mathematics', 'Science']
}
result = Students_collection.insert_one(student_document)
#print(f'Inserted document with ID: {result.inserted_id}')

student_documents = [
    {'firstName': 'Alice', 'lastName': 'Smith', 'age': 14, 'grade': '9th', 'courses': ['History', 'Math']},
    {'firstName': 'Bob', 'lastName': 'Kimani', 'age': 15, 'grade': '10th', 'courses': ['Chemistry', 'Physics']},
    {'firstName': 'Nduati', 'lastName': 'Githu', 'age': 9, 'grade': '4th', 'courses': ['Religion', 'English']},
    {'firstName': 'Mary', 'lastName': 'Wambui', 'age': 18, 'grade': '13th', 'courses': ['Biology', 'Business Studies']}
]
result = Students_collection.insert_many(student_documents)
#print(f'Inserted documents with ID: {result.inserted_ids}')

#query data #find  a single document
student = Students_collection.find_one({'firstName': 'John'})
#print(f'Found student: {student}')

#find multiple documents
students = Students_collection.find({'grade': '10th'})
for student in students:
    #print(student)
    pass  # Add a pass statement to provide an indented block

                    
#query specific fields
students = Students_collection.find({}, {'firstName': 1, 'grade': 1})
for student in students:
    #print(student)
    
  
    
                     

