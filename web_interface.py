import streamlit as st
import os
import sys

try:
    from app import MedicalIntake
    from exception import MedicalAppException
    
except ImportError as e:
    st.error(f"Fatal Interface Binding Error: Could not locate app.py system files.({e})")
    sys.exit(1)
    
st.set_page_config(page_title="Prescription Intake", layout="centered")
st.title("Prescription Intake Dashboard")
st.write("Upload or take a clear prescription scan below")

@st.cache_resource
def load_core_app():
    return MedicalIntake()

app_processor=load_core_app()

uploaded_file=st.file_uploader("Upload prescription file image", type=['jpg','png','jpeg'])

if uploaded_file:
    temp_path=f"web_temp{uploaded_file.name}"
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    with st.spinner("Executing extraction and verification..."):
        try:
            record=app_processor.run_audit(temp_path)
            st.success("Prescription Verified and Logged Successfully!")
            
            with st.container(border=True):
                st.subheader("Database Mapping Result")
                st.write(f"**Medication Target:**{record['medication']}")
                st.write(f"**Dosage Calculated:**{record['dosage']}")
                st.caption("Verified transaction recorded parmanently")
                
        except MedicalAppException as medical_err:
            st.error(f"Safety Exception Triggered:{str(medical_err)}")
            st.warning("An audio voice warning alert was broadcasted regarding this safety vilation.")
            
        except Exception as system_err:
            st.error(f"Engine System INterruption Error: {system_err}")
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
                