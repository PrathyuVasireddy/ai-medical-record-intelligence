import json


def create_patient_record():
    patient_data = {
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
