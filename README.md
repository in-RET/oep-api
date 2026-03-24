# OEP Data Uploader (library)

Lightweight Python library and helper script to upload CSV/Excel data and JSON metadata to the [Open Energy Platform (OEP)](https://openenergyplatform.org). No FastAPI frontend; no maintained CLI argument interface—use the batch script or the programmatic API.

## Features

- Programmatic uploader via `OepUploader`; batch helper script `main.py`
- Automatic schema creation with primary-key support and type inference
- CSV separator detection (`,`, `;`, tab) and Excel support (.xlsx/.xls)
- Table handling: optional delete/overwrite of existing tables
- Sample datasets under `data/` and `examples/` for quick testing

## Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

- Set OEP API token ([get a token](https://openenergyplatform.org/user/settings)):

```bash
# macOS/Linux
export OEP_API_TOKEN="your-token-here"

# Windows (CMD)
set OEP_API_TOKEN=your-token-here

# Windows (PowerShell)
$env:OEP_API_TOKEN="your-token-here"
```

## Usage (batch script)

Run from the repo root; the script scans `data/` for `.json` metadata files and uploads the matching `.csv` files to the configured topic (defaults to `sandbox`).

```bash
pip install -r requirements.txt
export OEP_API_TOKEN="your-token-here"
python main.py
```

Adjust `TOPIC`, `AUTOMATIC_SCAN`, and `delete_existing` directly in `main.py` as needed.

## Programmatic use

```python
from src.oep.uploader import OepUploader

# Ensure PYTHONPATH=src if the package is not installed
uploader = OepUploader(topic="sandbox")

df = uploader.read_data("data/demand/ghd_east.csv")


uploader.upload_complete(
    data_file="data/demand/ghd_east.csv",
    metadata_file="data/demand/ghd_east.json",
    table_name="my_table",
    primary_key="id",
    delete_existing=True,
)
```

## Project layout

```
oep-api/
├── src/oep/uploader.py     # OepUploader class
├── main.py                 # Helper script for batch upload from data/
├── data/                   # Sample data (CSV + JSON)
├── examples/               # Additional sample files
├── OEP_UPLOADER_README.md  # Detailed CLI docs (DE)
├── requirements.txt        # Dependencies
└── README.md
```

## More docs

- `OEP_UPLOADER_README.md` – detailed CLI reference with argument table (DE)

## Troubleshooting

- "OEP API token not found": set `OEP_API_TOKEN` or provide via `--token`.
- "Table already exists": use `delete_existing=True` in code or remove the table first.
- "Data/Metadata file not found": verify paths; CSV/JSON must exist.
- CSV parsing off: check separator; the tool tries `,`, `;`, tab in order.

## Notes

- Test first in the `sandbox` topic; use productive schemas carefully.
- For Excel uploads install `openpyxl`.
- For scripts, ensure `oep-client` is installed and `PYTHONPATH=src` is set if the package is not installed.
