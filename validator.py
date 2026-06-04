import sqlite3
import string
from exception import MedicalValidationError

class ClinicalDataValidator:
    def __init__(self, db_path: str="hospital.db"):
        self.db_path=db_path
        self.TYPO_DICT-{
            "amoxcilin": "amoxicillin",
            "amoxacillin": "amoxicillin",
            "paracetamal": "paracetamol",
            "asprin": "aspirin"
        }
        
    def clean_and_split(self, raw_text: str) -> list:
        clean_text= raw_text.translate(str.maketrans("","", string.punctuation))
        return clean_text.lower().split()
    
    def query_db_drug(self, word: str) -> bool:
        connection=sqlite3.connect(self.db_path)
        cursor=connection.cursor()
        cursor.execute("SELECT generic_name FROM medication WHERE generic_name= ?;"(word,))
        result=cursor.fetchone()
        connection.close()
        return result is not None
    
    def query_db_dosage(self, word_list: list) -> dict:
        detected_drug=None
        detected_dosage=None
        
        for word in word_list:
            if word in self.TYPO_DICT:
                word=self.TYPO_DICT[word]
                
            if self.query_db_drug(word):
                detected_drug=word
                break
            
        if not detected_drug:
            raise MedicalValidationError("No recognized, validated medical compounds found in database.")
        
        for word in word_list:
            if self.query_db_dosage(detected_drug, word):
                detected_dosage=word
                break
        
        return{
            "status":"VALIDATED",
            "medication":detected_drug.capitalize(),
            "dosage":detected_dosage if detected_dosage else "dosage unspecified or non-standard"
        }