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


def create_patient_record():
    record_text = read_medical_record()

    patient_name = extract_value(record_text, "Patient Name:")
    birth_date = extract_value(record_text, "Date of Birth:")
    gender = extract_value(record_text, "Gender:")

    patient_data = {
        "patient": {
            "name": patient_name,
            "birthDate": birth_date,
            "gender": gender
        },
        "source_text": record_text
    }

    return patient_data


if __name__ == "__main__":
    record = create_patient_record()

    print("AI Medical Record Intelligence")
    print("--------------------------------")

    print(json.dumps(record, indent=4))
