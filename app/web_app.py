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

# -----------------------------
# Header
# -----------------------------

st.title("AI Medical Record Intelligence")

st.caption(
    "Transform synthetic medical notes into structured, validated "
    "healthcare data and FHIR-style resources."
)

badge_col1, badge_col2, badge_col3 = st.columns([1.2, 1.2, 5])

with badge_col1:
    st.info("Synthetic Demo")

with badge_col2:
    st.info("Rule-Based Mode")

st.warning(
    "For demonstration only. This application uses synthetic data "
    "and is not intended for clinical use."
)

# -----------------------------
# Sample records
# -----------------------------

structured_sample = """Patient Name: Jane Doe
Date of Birth: 1986-04-20
Gender: Female

Diagnosis:
Type 2 Diabetes Mellitus

Medications:
Metformin 500 mg twice daily

Allergies:
Penicillin

Clinical Notes:
Patient reports improved glucose control after dietary changes.
Continue current medication and monitor blood glucose regularly.
"""

unstructured_sample = """Patient is Jane Doe, born April 20, 1986.

She has a history of type 2 diabetes mellitus and is currently taking
Metformin 500 mg twice daily.

The patient reports improved glucose control after dietary changes.

She has a known allergy to Penicillin.

Plan:
Continue current medication and monitor blood glucose regularly.
"""

st.subheader("1. Choose a Sample")

sample_type = st.radio(
    "Select input format",
    ["Structured Record", "Unstructured Record"],
    horizontal=True
)

if sample_type == "Structured Record":
    default_text = structured_sample
else:
    default_text = unstructured_sample

# -----------------------------
# Input
# -----------------------------

st.subheader("2. Enter a Synthetic Medical Record")

record_text = st.text_area(
    "Medical record",
    value=default_text,
    height=260,
    label_visibility="collapsed"
)

extract_button = st.button(
    "Extract Medical Data",
    type="primary",
    use_container_width=True
)

# -----------------------------
# Processing
# -----------------------------

if extract_button:

    if not record_text.strip():
        st.warning("Please enter a medical record.")

    else:
        extracted_data = extract_with_rules(record_text)

        validation_errors = validate_patient_record(extracted_data)

        fhir_resources = create_fhir_resources(extracted_data)

        result = {
            "extractionMethod": "Rule-based",
            "extractedData": extracted_data,
            "validation": {
                "valid": len(validation_errors) == 0,
                "errors": validation_errors
            },
            "fhirResources": fhir_resources
        }

        st.divider()

        # -----------------------------
        # Extracted fields
        # -----------------------------

        st.subheader("3. Extracted Patient Information")

        row1_col1, row1_col2, row1_col3 = st.columns(3)

        with row1_col1:
            st.metric(
                "Patient Name",
                extracted_data.get("name") or "Not found"
            )

        with row1_col2:
            st.metric(
                "Date of Birth",
                extracted_data.get("birthDate") or "Not found"
            )

        with row1_col3:
            st.metric(
                "Gender",
                extracted_data.get("gender") or "Not found"
            )

        row2_col1, row2_col2, row2_col3 = st.columns(3)

        with row2_col1:
            st.metric(
                "Diagnosis",
                extracted_data.get("diagnosis") or "Not found"
            )

        with row2_col2:
            st.metric(
                "Medication",
                extracted_data.get("medication") or "Not found"
            )

        with row2_col3:
            st.metric(
                "Allergy",
                extracted_data.get("allergy") or "Not found"
            )

        # -----------------------------
        # Validation
        # -----------------------------

        st.divider()

        st.subheader("4. Validation")

        if not validation_errors:
            st.success(
                "Validation passed — all required fields were extracted."
            )
        else:
            st.error("Validation failed.")

            for error in validation_errors:
                st.write(f"- {error}")

        # -----------------------------
        # Output tabs
        # -----------------------------

        st.divider()

        st.subheader("5. Structured Output")

        json_tab, fhir_tab = st.tabs(
            ["Structured JSON", "FHIR-Style Resources"]
        )

        with json_tab:
            st.json(result)

            json_download = json.dumps(
                result,
                indent=2
            )

            st.download_button(
                label="Download JSON",
                data=json_download,
                file_name="medical_record_output.json",
                mime="application/json"
            )

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

        # -----------------------------
        # Architecture
        # -----------------------------

        st.divider()

        st.subheader("6. Processing Pipeline")

        st.code(
            """
Medical Record
      ↓
Information Extraction
      ↓
Validation
      ↓
Structured JSON
      ↓
FHIR-Style Resources
            """,
            language="text"
        )

        st.caption(
            "Current extraction mode: rule-based. "
            "Optional AI extraction is supported through configuration."
        )