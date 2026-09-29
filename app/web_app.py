import json
import streamlit as st

from main import (
    extract_with_rules,
    validate_patient_record,
    create_fhir_resources
)


st.set_page_config(
    page_title="AI Medical Record Intelligence",
    page_icon="🩺",
    layout="wide"
)


st.title("AI Medical Record Intelligence")

st.write(
    "Transform synthetic medical notes into structured healthcare data "
    "and FHIR-style resources."
)

st.info(
    "This demo uses synthetic data only and is not intended for clinical use."
)


sample_note = """Patient is Jane Doe, born April 20, 1986.

She has a history of type 2 diabetes mellitus and is currently taking
Metformin 500 mg twice daily.

She has a known allergy to Penicillin.
"""


record_text = st.text_area(
    "Enter a synthetic medical record",
    value=sample_note,
    height=220
)


if st.button("Extract Medical Data"):
    if not record_text.strip():
        st.warning("Please enter a medical record.")

    else:
        extracted_data = extract_with_rules(record_text)

        validation_errors = validate_patient_record(extracted_data)

        fhir_resources = create_fhir_resources(extracted_data)

        st.subheader("Extracted Data")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Patient Name:**", extracted_data.get("name"))
            st.write("**Date of Birth:**", extracted_data.get("birthDate"))
            st.write("**Gender:**", extracted_data.get("gender"))

        with col2:
            st.write("**Diagnosis:**", extracted_data.get("diagnosis"))
            st.write("**Medication:**", extracted_data.get("medication"))
            st.write("**Allergy:**", extracted_data.get("allergy"))

        st.subheader("Validation")

        if len(validation_errors) == 0:
            st.success("Validation passed")
        else:
            st.error("Validation failed")

            for error in validation_errors:
                st.write(f"- {error}")

        st.subheader("Structured JSON")

        result = {
            "extractionMethod": "Rule-based",
            "extractedData": extracted_data,
            "validation": {
                "valid": len(validation_errors) == 0,
                "errors": validation_errors
            },
            "fhirResources": fhir_resources
        }

        st.json(result)

        st.subheader("FHIR-Style Resources")

        resource_type = st.selectbox(
            "Select resource",
            [
                "Patient",
                "Condition",
                "MedicationStatement",
                "AllergyIntolerance"
            ]
        )

        resource_map = {
            "Patient": fhir_resources["patient"],
            "Condition": fhir_resources["condition"],
            "MedicationStatement": fhir_resources["medication"],
            "AllergyIntolerance": fhir_resources["allergy"]
        }

        st.json(resource_map[resource_type])