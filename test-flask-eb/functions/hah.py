import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firestore():
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("serviceKeyv2.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

def extract_schema(db):
    # Fetch Firestore collections and documents
    collections = db.collections()
    schema = {}

    # Extract schema from Firestore database
    for collection in collections:
        collection_schema = {}
        docs = collection.stream()
        for doc in docs:
            doc_schema = {}
            for field, value in doc.to_dict().items():
                doc_schema[field] = type(value).__name__
            collection_schema[doc.id] = doc_schema
        schema[collection.id] = collection_schema
    return schema

def print_schema(schema):
    # Print schema in a text format
    for collection, collection_schema in schema.items():
        print(f"Collection: {collection}")
        for document, document_schema in collection_schema.items():
            print(f"  Document: {document}")
            for field, field_type in document_schema.items():
                print(f"    {field}: {field_type}")
            print()

def main():
    try:
        # Initialize Firestore
        db = initialize_firestore()
        
        # Extract schema from Firestore
        schema = extract_schema(db)
        
        # Print schema
        print_schema(schema)
        
        print("Schema extracted successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
