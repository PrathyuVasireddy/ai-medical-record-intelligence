import json
from pathlib import Path

from ai_extractor import extract_medical_data_with_ai


def read_medical_record(filename="sample_record.txt"):
    file_path = Path(__file__).parent.parent / "sample-data" / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_value(text, label):
    for line in text.splitlines():
        if line.startswith(label):
            return line.replace(label, "").strip()

    return None


def extract_section_value(text, section_name):
    lines = text.splitlines()

    for index, line in enumerate(lines):
        if line.strip() == section_name:
            for next_line in lines[index + 1:]:
                if next_line.strip():
                    return next_line.strip()

    return None


def extract_with_rules(record_text):
    return {
        "name": extract_value(record_text, "Patient Name:"),
        "birthDate": extract_value(record_text, "Date of Birth:"),
        "gender": extract_value(record_text, "Gender:"),
        "diagnosis": extract_section_value(record_text, "Diagnosis:"),
        "medication": extract_section_value(record_text, "Medications:"),
        "allergy": extract_section_value(record_text, "Allergies:")
    }


def validate_patient_record(data):
    errors = []

    if not data.get("name"):
        errors.append("Patient name is missing")

    if not data.get("birthDate"):
        errors.append("Date of birth is missing")

    if not data.get("gender"):
        errors.append("Gender is missing")

    if not data.get("diagnosis"):
        errors.append("Diagnosis is missing")

    if not data.get("medication"):
        errors.append("Medication is missing")

    if not data.get("allergy"):
        errors.append("Allergy information is missing")

    return errors


def create_fhir_resources(data):
    patient = {
        "resourceType": "Patient",
        "id": "patient-001",
        "name": [
            {
                "text": data.get("name")
            }
        ],
        "gender": data.get("gender", "").lower() if data.get("gender") else None,
        "birthDate": data.get("birthDate")
    }

    condition = {
        "resourceType": "Condition",
        "id": "condition-001",
        "subject": {
            "reference": "Patient/patient-001"
        },
        "code": {
            "text": data.get("diagnosis")
        }
    }

    medication = {
        "resourceType": "MedicationStatement",
        "id": "medication-001",
        "subject": {
            "reference": "Patient/patient-001"
        },
        "medicationCodeableConcept": {
            "text": data.get("medication")
        }
    }

    allergy = {
        "resourceType": "AllergyIntolerance",
        "id": "allergy-001",
        "patient": {
            "reference": "Patient/patient-001"
        },
        "code": {
            "text": data.get("allergy")
        }
    }

    return {
        "patient": patient,
        "condition": condition,
        "medication": medication,
        "allergy": allergy
    }


def create_patient_record():
    record_text = read_medical_record()


    try:
        extracted_data = extract_medical_data_with_ai(record_text)

    except Exception as error:
        print(f"AI extraction failed: {error}")
        print("Using rule-based extraction instead.")

        extracted_data = extract_with_rules(record_text)
        extraction_method = "Rule-based fallback"

    validation_errors = validate_patient_record(extracted_data)

    fhir_resources = create_fhir_resources(extracted_data)

    return {
        "extractionMethod": extraction_method,
        "extractedData": extracted_data,
        "validation": {
            "valid": len(validation_errors) == 0,
            "errors": validation_errors
        },
        "fhirResources": fhir_resources
    }


if __name__ == "__main__":
    record = create_patient_record("sample_record.txt")

    print("AI Medical Record Intelligence")
    print("--------------------------------")

    print(json.dumps(record, indent=4))
