import json
from pathlib import Path


def read_medical_record():
    file_path = Path(__file__).parent.parent / "sample-data" / "sample_record.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def create_patient_record():
    record_text = read_medical_record()

    patient_data = {
        "source_text": record_text,
        "patient": {
            "name": "Jane Doe",
            "birthDate": "1986-04-20",
            "gender": "female"
        },
        "conditions": [
            {
                "name": "Type 2 Diabetes Mellitus"
            }
        ],
        "medications": [
            {
                "name": "Metformin",
                "dose": "500 mg",
                "frequency": "twice daily"
            }
        ],
        "allergies": [
            {
                "name": "Penicillin"
            }
        ]
    }

    return patient_data


if __name__ == "__main__":
    record = create_patient_record()

    print("AI Medical Record Intelligence")
    print("--------------------------------")

    print(json.dumps(record, indent=4))
