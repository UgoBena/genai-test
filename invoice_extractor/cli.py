import json
from pathlib import Path

import typer

from invoice_extractor.extractor import InvoiceExtractor

app = typer.Typer()

extractor = InvoiceExtractor()


def process_pdf(file_path: Path, output_path: Path):
    """
    Process a single PDF file.
    """
    typer.echo(f"Processing file {file_path}...")
    res = extractor.process(file_path.read_bytes())
    with open(output_path / f"{file_path.stem}.json", "w") as f:
        json.dump(res, f)


@app.command()
def process(
    path: Path = typer.Argument(..., help="Path to a PDF file or a folder containing PDF files."),
    output_path: Path = typer.Option(Path.cwd(), "--output-path", help="Directory to save output JSON files."),
):
    """
    Extract main information from a single PDF file or all PDF files in a folder.
    """
    # Ensure the output directory exists
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    if path.is_file() and path.suffix.lower() == ".pdf":
        process_pdf(path, output_path)
    elif path.is_dir():
        pdf_files = list(path.glob("*.pdf"))
        if not pdf_files:
            typer.echo("No PDF files found in the specified directory.")
            raise typer.Exit()
        for pdf_file in pdf_files:
            process_pdf(pdf_file, output_path)
    else:
        typer.echo("The specified path is neither a PDF file nor a directory.")
        raise typer.Exit()
