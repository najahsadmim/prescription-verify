import pyttsx3
import os
import sys
import sqlite3

try:
    
    from engine import TextExtractionEngine
    from validator import ClinicalDataValidator
    from exception import MedicalAppException
    from storage_manager import PatientLedger

except ImportError as e:
    print(f"[Fatal Integeration Error] Missing Pipeline module dependencies: {e}")
    sys.exit(1)
    

class MedicalIntake:
    def __init__(self):
        self.engine=TextExtractionEngine()
        self.validator=ClinicalDataValidator()
        self.voice_engine=pyttsx3.init()
        self.voice_engine.setProperty('rate', 155)
        
    def speak(self, text_payload: str):
        print(f"[Audio System] Broadcasting: '{text_payload}")
        self.voice_engine.say(text_payload)
        self.voice_engine.runAndWait()
        
    def run_audit(self, image_path: str):
        print(f"\n==========================================")
        print(f"Commencing Ingestion Loop for Target: {image_path}")
        print(f"==========================================")
        
        try:
            raw_text= self.engine.extract_text(image_path)
            print(f"[Log] AI Extracted Text Result: \"{raw_text}\"")
            
            tokens=self.validator.clean_and_split(raw_text)
            validated_payload=self.validator.verify_and_correct(tokens)
            
            ledger_success=self.ledger.log_transaction(validated_payload)
            if not ledger_success:
                raise IOError("Persistent storage manager failed to write transaction array to disk.")
            
            connection=sqlite3.connect("hospital_registry.db",timeout=30.0)
            cursor=connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prescription(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    medication TEXT NOT NULL,
                    dosage TEXT NOT NULL,
                    status TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CUREENT_TIMESTAMP
                    )
                """)
            
            cursor.execute("""
                INSERT INTO prescription(medication, dosage, status)
                VALUES (?,?, 'APPROVED_AND_LOGGED')
                """, (validated_payload["medication"], validated_payload["dosage"]))
            
            connection.commit()
            connection.close()
            
            print(f"[Success] Intake completed safetly for {validated_payload['medication']}({validated_payload['dosage']})")
            return validated_payload 
                           
            
        except MedicalAppException as mae:
            error_msg=f"Intake Blocked! Safety Exception Detected: {str(mae)}"
            self.speak(error_msg)
            raise mae 
        
        except Exception as unhandled_err:
            print(f"Fatal Operating System Anomaly identified: {unhandled_err}")
            raise unhandled_err
        
if __name__=="__main__":
    app=MedicalIntake()
    
    app.run_audit("x.jpg")
            
                  
            
        