# Invoice Information Extractor
Parse and extract information from pdf files as defined in invoice_extractor.prompt. Uses 2 internal databases (shipment and suppliers).

## **Main Information to Extract**

1. **Invoice Number**
2. **Invoice Date**
3. **Due Date**
4. **Currency**
5. **Exchange Rate** (may not be present)
6. **Foresea Name**
    - Internal reference of the shipment in our system. It consists of four letters, starting with D, E, or F. If not available, it may be replaced by another reference (see below).
        1. For air shipments: **Airway Bill Number**, always in the form 123-12345678 (the hyphen may be omitted).
        2. For sea shipments: **Bill of Lading Number** and/or **Container Number** (always in the form ABCD1234567).
7. **Invoiced Office**
    - Can be the French, US, Italian, or Spanish office.
8. **Supplier ID & Name**
    - Use the given list of suppliers from our database.
9. **Total Amount Without Tax**
10. **Total Amount With Tax**
11. **Line Items** (Description, Quantity, Unit Price, Line Total, Taxable, Currency, Final Amount)

## CLI
```
poetry install
poetry run invoice_extractor PATH
```

PATH can be a single pdf file or folder of PDF files. Will output result in json files in current working directory (can be modified using `--output-file` option).

## App
Project is packaged inside a simple app. Demo available [here](http://13.38.230.153/).
