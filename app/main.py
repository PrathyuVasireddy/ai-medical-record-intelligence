import json
import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from ai_extractor import extract_medical_data_with_ai


load_dotenv()


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
    name = extract_value(record_text, "Patient Name:")
    birth_date = extract_value(record_text, "Date of Birth:")
    gender = extract_value(record_text, "Gender:")
    diagnosis = extract_section_value(record_text, "Diagnosis:")
    medication = extract_section_value(record_text, "Medications:")
    allergy = extract_section_value(record_text, "Allergies:")

    # Natural-language patient name extraction
    if not name:
        match = re.search(
            r"Patient is ([A-Z][a-z]+ [A-Z][a-z]+)",
            record_text,
            re.IGNORECASE
        )

        if match:
            name = match.group(1)

    # Natural-language DOB extraction and normalization
    if not birth_date:
        match = re.search(
            r"born ([A-Za-z]+ \d{1,2}, \d{4})",
            record_text,
            re.IGNORECASE
        )

        if match:
            raw_date = match.group(1)

            try:
                parsed_date = datetime.strptime(raw_date, "%B %d, %Y")
                birth_date = parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                birth_date = raw_date

    # Natural-language diagnosis extraction
    if not diagnosis:
        match = re.search(
            r"history of (.+?)(?: and is currently taking|\.|\n)",
            record_text,
            re.IGNORECASE
        )

        if match:
            diagnosis = match.group(1).strip()

    # Natural-language medication extraction
    if not medication:
        match = re.search(
            r"taking ([^.]+)",
            record_text,
            re.IGNORECASE
        )

        if match:
            medication = match.group(1).strip()

    # Natural-language allergy extraction
    if not allergy:
        match = re.search(
            r"allergy to ([^.]+)",
            record_text,
            re.IGNORECASE
        )

        if match:
            allergy = match.group(1).strip()

    # Infer gender from pronouns when explicit gender is unavailable
    if not gender:
        if re.search(r"\bshe\b", record_text, re.IGNORECASE):
            gender = "Female"

        elif re.search(r"\bhe\b", record_text, re.IGNORECASE):
            gender = "Male"

    return {
        "name": name,
        "birthDate": birth_date,
        "gender": gender,
        "diagnosis": diagnosis,
        "medication": medication,
        "allergy": allergy
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
        "gender": (
            data.get("gender", "").lower()
            if data.get("gender")
            else None
        ),
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


def create_patient_record(filename="sample_record.txt"):
    record_text = read_medical_record(filename)

    use_ai = os.getenv("USE_AI", "false").lower() == "true"

    if use_ai:
        extraction_method = "AI"

        try:
            extracted_data = extract_medical_data_with_ai(record_text)

        except Exception as error:
            print(f"AI extraction failed: {error}")
            print("Using rule-based extraction instead.")

            extracted_data = extract_with_rules(record_text)
            extraction_method = "Rule-based fallback"

    else:
        extracted_data = extract_with_rules(record_text)
        extraction_method = "Rule-based"

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
    import sys

    filename = "sample_record.txt"

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    record = create_patient_record(filename)

    print("AI Medical Record Intelligence")
    print("--------------------------------")
    print(f"Input file: {filename}")
    print()

    print(json.dumps(record, indent=4))