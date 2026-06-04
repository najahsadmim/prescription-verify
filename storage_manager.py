import json
from datetime import datetime

class PatientLedger:
    def __init__(self, log_file="patient_intake.json"):
        self.log_file=log_file
        
    def log_transaction(self, validated_payload: dict):
        new_entry={
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "medication": validated_payload["medication"],
            "dosage": validated_payload["dosage"],
            "status": "APPROVED_AND_LOGGED"
        }
        
        try:
            try:
                with open(self.log_file,"r") as file:
                    current_history=json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                current_history=[]
                
            current_history.append(new_entry)
            
            with open(self.log_file, "w") as file:
                json.dump(current_history, file, indent=4)
                
            print(f"[Storage] Transaction successfully recorded to: '{self.log_file}")
            return True
            
        except Exception as e:
            print(f"[Storage] TFailed writing transaction matrix to disk: '{e}")
            return False
    