# Prescription Verify
Prescription Verify is a full stack clinical AI Pipeline designed to help patients scan their prescriptions and verify their medications. 

**Objective:**
On a larger scale, Prescription Verify automates and protects the bridge between physical medical paper and digital hospital records. 
By using local AI to instantly read prescriptions and validating them against a strict SQL database, it eliminates dangerous human transcription and typos before they reach a patient's file. 
It preserves patient privacy by deleting raw images immediately after processing, avoiding the risks of cloud storage.
Ultimately, it cuts down on hospital administrative workloads, allowing medical staff to focus on critical care while ensuring data entry is fast, accurate, and completely private.

**Features:**
This project is split into 5 separate files:
- exception.py : custom error handling file that prevents the program from crashing if an image is blurry or a drug is unrecognised.
- db_setup.py : builds a local SQLite database (hospital.db) pre-loaded with official drug names and corresponding dosages.
- validator.py : cleans up extracted text, fixes typos or spelling errors from extracted text, and runs SQL queries to verify drug is real.
- engine.py : uses PyTorch and Hugging Face model (BLIP) to extract information from given prescription images.
- web_interface.py : a simple, clean website built for patients using Streamlit to upload their prescription images and see their results (this is an optional step as every hospital will have their own website and this program can be integrated into the website accordingly. web_interface will simply act as a dummy website for us to verify whether our program runs properly)

**Tech Stack:**
- Language: Python
- Framework: Hugging Face Transformer
- Model: Salesforce BLIP
- Libraries: PIL (Pillow), PyTorch, Streamlit, SQLite3, pyttsx3

**Future Improvements:**
- integrate 'RapidFuzz' from the library to match handwritten drug spelling anomalies instead of relying on dictionary spellings
- for enterprise level data tracking, hospital.db could be migrated to PostgreSQL (an enterprise-grade database engine) to allow simultaneous connections on the hospital network, and to prevent crashes or delays in the system.
- Add an authentication layer to autheticate registered patients and hospital staff
- replace BLIP with an open-source vision transformer fine-tuned specifically on handwritten health records to allow more accurate text extraction

