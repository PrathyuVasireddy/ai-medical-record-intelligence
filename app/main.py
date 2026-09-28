import json
from pathlib import Path


def read_medical_record():
    file_path = Path(__file__).parent.parent / "sample-data" / "sample_record.txt"

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


def validate_patient_record(patient_data):
    errors = []

    if not patient_data["patient"]["name"]:
        errors.append("Patient name is missing")

    if not patient_data["patient"]["birthDate"]:
        errors.append("Date of birth is missing")

    if not patient_data["patient"]["gender"]:
        errors.append("Gender is missing")

    if not patient_data["conditions"][0]["name"]:
        errors.append("Diagnosis is missing")

    if not patient_data["medications"][0]["description"]:
        errors.append("Medication is missing")

    if not patient_data["allergies"][0]["name"]:
        errors.append("Allergy information is missing")

    return errors


def create_patient_record():
    record_text = read_medical_record()

    patient_name = extract_value(record_text, "Patient Name:")
    birth_date = extract_value(record_text, "Date of Birth:")
    gender = extract_value(record_text, "Gender:")

    diagnosis = extract_section_value(record_text, "Diagnosis:")
    medication = extract_section_value(record_text, "Medications:")
    allergy = extract_section_value(record_text, "Allergies:")

    patient_data = {
        "patient": {
            "name": patient_name,
            "birthDate": birth_date,
            "gender": gender
        },
        "conditions": [
            {
                "name": diagnosis
            }
        ],
        "medications": [
            {
                "description": medication
            }
        ],
        "allergies": [
            {
                "name": allergy
            }
        ],
        "source_text": record_text
    }

    validation_errors = validate_patient_record(patient_data)

    patient_data["validation"] = {
        "valid": len(validation_errors) == 0,
        "errors": validation_errors
    }

    return patient_data


if __name__ == "__main__":
    record = create_patient_record()

    print("AI Medical Record Intelligence")
    print("--------------------------------")

    print(json.dumps(record, indent=4))
