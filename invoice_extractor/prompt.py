import importlib.resources
import json

from langchain_core.prompts import ChatPromptTemplate

with importlib.resources.open_text("invoice_extractor.resources", "shipments_genai.json") as file:
    shipment_data = json.load(file)

with importlib.resources.open_text("invoice_extractor.resources", "suppliers_genai.json") as file:
    supplier_data = json.load(file)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant skilled in extracting structured data from invoices and matching them with supplier and shipments databases.",
        ),
        (
            "user",
            "Extract the following details from the invoice text and match them with supplier and shipment data: \
        1. Invoice Number \
        2. Invoice Date. Convert to 'mm/dd/yyyy' format \
        3. Due Date. Convert to 'mm/dd/yyyy' format \
        4. Currency \
        5. Exchange Rate (if present) \
        6. Foresea Name. Must be matched with the shipment database. It consists of four letters, starting with D, E, or F. If not available, it may be replaced by another reference as follow. For air shipments: **Airway Bill Number**, always in the form 123-12345678 (the hyphen may be omitted). For sea shipments: **Bill of Lading Number** and/or **Container Number** (always in the form ABCD1234567). \
        7. Invoiced Office. Adress in France, USA, Spain or Italy. Name Should contain 'Ovrsea' or 'FORESEA'. JSON field is an object with fields 'name' and 'adress' \
        8. Supplier ID & Name. Must be matched with the supplier database. JSON field name is 'supplier' \
        9. Total Amount Without Tax (HT) \
        10. Total Amount With Tax \
        11. Line Items (description, quantity, unit price, line total, taxable, currency, and final amount). \
        **Important**: Some of these fields may be missing in the invoice text. In such cases, simply omit the missing field. \
        Your answer will be a JSON object. JSON field names should be snake_cased",
        ),
        (
            "user",
            f"Here is the supplier database in JSON format:\n\n{json.dumps(supplier_data, indent=2)}",
        ),
        (
            "user",
            f"Here is the shipment database in JSON format:\n\n{json.dumps(shipment_data, indent=2)}",
        ),
        ("user", "Here is the invoice text :\n\n{{invoice_text}}"),
    ],
    template_format="jinja2",
)
