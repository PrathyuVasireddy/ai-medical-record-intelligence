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
st.caption(
    "Transform synthetic medical notes into validated structured data "
    "and FHIR-style healthcare resources."
)

st.info(
    "Demo only — uses synthetic data and is not intended for clinical use."
)

sample_note = """Patient is Jane Doe, born April 20, 1986.

She has a history of type 2 diabetes mellitus and is currently taking
Metformin 500 mg twice daily.

She has a known allergy to Penicillin.
"""

st.subheader("1. Enter a Synthetic Medical Record")

record_text = st.text_area(
    "Medical record",
    value=sample_note,
    height=220,
    label_visibility="collapsed"
)

extract_button = st.button(
    "Extract Medical Data",
    type="primary",
    use_container_width=True
)

if extract_button:
    if not record_text.strip():
        st.warning("Please enter a medical record.")

    else:
        extracted_data = extract_with_rules(record_text)
        validation_errors = validate_patient_record(extracted_data)
        fhir_resources = create_fhir_resources(extracted_data)

        st.divider()

        st.subheader("2. Extracted Patient Information")

        row1_col1, row1_col2, row1_col3 = st.columns(3)

        with row1_col1:
            st.metric(
                label="Patient Name",
                value=extracted_data.get("name") or "Not found"
            )

        with row1_col2:
            st.metric(
                label="Date of Birth",
                value=extracted_data.get("birthDate") or "Not found"
            )

        with row1_col3:
            st.metric(
                label="Gender",
                value=extracted_data.get("gender") or "Not found"
            )

        row2_col1, row2_col2, row2_col3 = st.columns(3)

        with row2_col1:
            st.metric(
                label="Diagnosis",
                value=extracted_data.get("diagnosis") or "Not found"
            )

        with row2_col2:
            st.metric(
                label="Medication",
                value=extracted_data.get("medication") or "Not found"
            )

        with row2_col3:
            st.metric(
                label="Allergy",
                value=extracted_data.get("allergy") or "Not found"
            )

        st.divider()

        st.subheader("3. Validation")

        if len(validation_errors) == 0:
            st.success("Validation passed — all required fields were extracted.")
        else:
            st.error("Validation failed.")

            for error in validation_errors:
                st.write(f"- {error}")

        st.divider()

        st.subheader("4. Structured Output")

        structured_result = {
            "extractionMethod": "Rule-based",
            "extractedData": extracted_data,
            "validation": {
                "valid": len(validation_errors) == 0,
                "errors": validation_errors
            },
            "fhirResources": fhir_resources
        }

        json_tab, fhir_tab = st.tabs(
            ["Structured JSON", "FHIR-Style Resources"]
        )

        with json_tab:
            st.json(structured_result)

        with fhir_tab:
            resource_name = st.selectbox(
                "Choose a FHIR-style resource",
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

            st.json(resource_map[resource_name])

        st.divider()

        st.caption(
            "Pipeline: Medical Record → Extraction → Validation → "
            "Structured JSON → FHIR-Style Resources"
        )