AI Medical Record Intelligence

A healthcare engineering prototype that transforms synthetic structured and unstructured medical records into validated healthcare data and FHIR-style resources.

Why This Project?

Healthcare information is often stored or exchanged through unstructured documents such as clinical notes, discharge summaries, scanned forms, and medical reports.

Turning that information into structured data is useful for:

- Healthcare interoperability
- Automation
- Analytics
- AI-assisted workflows
- Data validation
- Structured downstream processing

This project explores that transformation pipeline using only synthetic medical data.

Architecture

Medical Record
      |
      v
Text Extraction
      |
      v
Information Extraction
      |
      v
Validation
      |
      v
Structured JSON
      |
      v
FHIR-Style Resources


Current Features

- Reads synthetic medical records
- Supports structured and unstructured text
- Extracts patient name
- Extracts date of birth
- Extracts gender
- Extracts diagnosis
- Extracts medication
- Extracts allergy information
- Normalizes date formats
- Validates required healthcare fields
- Produces structured JSON
- Generates FHIR-style resources
- Supports command-line file selection
- Supports optional AI extraction with rule-based fallback
- Uses environment-based configuration for AI mode

Technologies

- Python
- Regular Expressions
- JSON
- FHIR-style healthcare data modeling
- OpenAI API integration
- Python dotenv
- Environment-based configuration
- Information extraction
- Data validation
- Git and GitHub

How to Run

1. Clone the Repository

git clone https://github.com/PrathyuVasireddy/ai-medical-record-intelligence.git
cd ai-medical-record-intelligence


2. Create a Virtual Environment

python3 -m venv .venv


3. Activate the Virtual Environment

On macOS or Linux:

source .venv/bin/activate


4. Install Dependencies

pip install -r requirements.txt


5. Run the Structured Sample

python3 app/main.py sample_record.txt


6. Run the Unstructured Sample

python3 app/main.py unstructured_record.txt


Example Structured Input

Patient Name: Jane Doe
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


Example Unstructured Input

Patient is Jane Doe, born April 20, 1986.

She has a history of type 2 diabetes mellitus and is currently taking Metformin 500 mg twice daily.

The patient reports that her glucose control has improved after making dietary changes.

She has a known allergy to Penicillin.

Plan:
Continue current medication and monitor blood glucose regularly.


Example Output

{
  "extractionMethod": "Rule-based",
  "extractedData": {
    "name": "Jane Doe",
    "birthDate": "1986-04-20",
    "gender": "Female",
    "diagnosis": "type 2 diabetes mellitus",
    "medication": "Metformin 500 mg twice daily",
    "allergy": "Penicillin"
  },
  "validation": {
    "valid": true,
    "errors": []
  }
}


FHIR-Style Resources

The extracted information is transformed into simplified healthcare resources modeled after common FHIR resource types.

Current resource types include:

- Patient
- Condition
- MedicationStatement
- AllergyIntolerance

Example Patient resource:

{
  "resourceType": "Patient",
  "id": "patient-001",
  "name": [
    {
      "text": "Jane Doe"
    }
  ],
  "gender": "female",
  "birthDate": "1986-04-20"
}


Example Condition resource:

{
  "resourceType": "Condition",
  "id": "condition-001",
  "subject": {
    "reference": "Patient/patient-001"
  },
  "code": {
    "text": "type 2 diabetes mellitus"
  }
}


Validation

The application validates required extracted fields before generating the final structured result.

Current validation checks include:

- Patient name
- Date of birth
- Gender
- Diagnosis
- Medication
- Allergy information

Example successful validation:

{
  "valid": true,
  "errors": []
}


Example failed validation:

{
  "valid": false,
  "errors": [
    "Medication is missing"
  ]
}


Extraction Modes

The application currently supports two extraction modes.

Rule-Based Extraction

The default mode uses deterministic parsing and regular expressions.

It can process:

- Label-based structured records
- Simple natural-language medical notes

Optional AI Extraction

The project also includes an optional AI extraction layer.

Create a local .env file in the project root:

USE_AI=false
OPENAI_API_KEY=your_api_key_here


With:

USE_AI=false


the application uses the local rule-based extraction engine.

With:

USE_AI=true


the application attempts AI extraction first.

If AI extraction fails, the application automatically falls back to rule-based extraction.

The .env file is excluded from Git and should never be committed to the repository.

Repository Structure

ai-medical-record-intelligence/
│
├── app/
│   ├── main.py
│   └── ai_extractor.py
│
├── docs/
│   └── architecture.md
│
├── sample-data/
│   ├── sample_record.txt
│   ├── unstructured_record.txt
│   └── sample_output.json
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt


Privacy

This repository uses only synthetic sample data.

It does not contain:

- Real patient information
- Protected health information
- Production data
- Employer-owned source code
- Production credentials
- Private API keys

Limitations

The current rule-based extraction engine uses deterministic parsing and regular expressions.

Natural-language extraction is therefore limited to patterns that the parser recognizes.

The generated healthcare resources are simplified FHIR-style representations and are not claimed to be fully FHIR-compliant.

The project is intended for software engineering, interoperability, and AI experimentation only.

It is not intended for clinical use.

Roadmap

- [x] Structured medical record parsing
- [x] Unstructured medical record parsing
- [x] Date normalization
- [x] Validation layer
- [x] Structured JSON output
- [x] FHIR-style resource generation
- [x] Command-line file selection
- [x] Optional AI extraction mode
- [x] Rule-based fallback
- [ ] PDF document support
- [ ] OCR support
- [ ] Confidence scoring
- [ ] Formal FHIR validation
- [ ] Medical terminology coding
- [ ] Human review interface
- [ ] Web application demo
- [ ] Automated tests
- [ ] CI/CD workflow

Disclaimer

This project is a technical prototype using synthetic data.

It is not a medical device and should not be used for diagnosis, treatment, or clinical decision-making.

Status

Active development.