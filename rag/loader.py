# rag/loader.py
import json
from pathlib import Path


def load_hospital_data():
    data_path = Path("data/hospital_data.json")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    # Hospital info
    hospital = data["hospital_info"]
    documents.append(
        f"Creation Hospital is located at {hospital['location']}. "
        f"Contact number is {hospital['contact_number']}. "
        f"Emergency number is {hospital['emergency_number']}."
    )

    # OPD timings
    opd = data["opd_timings"]
    documents.append(
        f"General OPD timings are {opd['general_opd']}. "
        f"On Sunday: {opd['sunday']}. "
        f"Registration closes {opd['registration_closes']}."
    )

    # Doctors
    for doc in data["doctors"]:
        documents.append(
            f"{doc['name']} works in {doc['department']} department. "
            f"Available {doc['availability']}. "
            f"Consultation fee is {doc['consultation_fee']}. "
            f"Speaks {', '.join(doc['languages'])}."
        )

    # Diagnostic services
    for service in data["diagnostic_services"]:
        documents.append(
            f"{service['service']} costs {service['price']}. "
            f"Report available in {service['report_time']}."
        )

    # Policies
    for policy in data["policies"]:
        documents.append(policy)

    return documents
