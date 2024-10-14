import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceKeyv2.json')
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

class CareerCategory:
    def __init__(self, career_category, career_description, career_expert_email, career_expert_id, career_expert_name,
                 dscd, possible_careers, related_pathway):
        self.career_category = career_category
        self.career_description = career_description
        self.career_expert_email = career_expert_email
        self.career_expert_id = career_expert_id
        self.career_expert_name = career_expert_name
        self.dscd = dscd
        self.possible_careers = possible_careers
        self.related_pathway = related_pathway

    def to_dict(self):
        return {
            'careerCategory': self.career_category,
            'careerDescription': self.career_description,
            'careerExpertEmail': self.career_expert_email,
            'careerExpertId': self.career_expert_id,
            'careerExpertName': self.career_expert_name,
            'dscd': self.dscd,
            'possibleCareers': self.possible_careers,
            'relatedPathway': self.related_pathway
        }

# Function to input career details from user
def input_career_details(index):
    career_category = input(f"Enter career category for Career {index}: ")
    career_description = input(f"Enter career description for Career {index}: ")
    career_expert_email = input(f"Enter career expert email for Career {index}: ")
    career_expert_id = input(f"Enter career expert ID for Career {index}: ")
    career_expert_name = input(f"Enter career expert name for Career {index}: ")
    possible_careers_count = int(input(f"Enter number of possible careers for Career {index}: "))
    possible_careers = [input(f"Enter possible career {i+1}: ") for i in range(possible_careers_count)]
    related_pathway_count = int(input(f"Enter number of related pathways for Career {index}: "))
    related_pathway = [input(f"Enter related pathway {i+1}: ") for i in range(related_pathway_count)]
    return CareerCategory(career_category, career_description, career_expert_email, career_expert_id, career_expert_name,
                          datetime.now(), possible_careers, related_pathway)

# Loop to add career categories to Firestore
for i in range(1, 7):
    career_category = input_career_details(i)
    data = career_category.to_dict()
    db.collection('Career').document(str(i)).set(data)
    print(f"Career {i} data added successfully to Firestore!")