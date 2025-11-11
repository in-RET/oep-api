# OEP API - Open Energy Platform Data Uploader

A comprehensive Python toolkit for uploading data and metadata to the [Open Energy Platform (OEP)](https://openenergyplatform.org).

This project provides both a **standalone command-line tool** and a **FastAPI web interface** for easy data upload to the OEP.

## Features

- **Standalone CLI Tool** - Upload data directly from the command line
- **FastAPI Web Interface** - User-friendly web UI for data upload
- **Flexible Data Formats** - Support for CSV, Excel (.xlsx, .xls)
- **Automatic Schema Generation** - Infers table structure from your data
- **Metadata Upload** - Full support for OEP metadata format (JSON)
- **Smart CSV Detection** - Automatically detects separators (`,`, `;`, Tab)
- **Type Inference** - Automatic SQL type detection (bigint, text, double precision, etc.)
- **Table Management** - Create, delete, and update tables
- **Multiple Schemas** - Support for sandbox, model_draft, and other OEP schemas
- **Programmatic API** - Use as a Python library in your own scripts

## Requirements

- Python 3.8+
- OEP API Token ([Get one here](https://openenergy-platform.org/user/settings))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/oep-api.git
cd oep-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OEP API token:
```bash
# Linux/Mac
export OEP_API_TOKEN="your-token-here"

# Windows (CMD)
set OEP_API_TOKEN=your-token-here

# Windows (PowerShell)
$env:OEP_API_TOKEN="your-token-here"
```

## 📖 Usage

### Command Line Interface (CLI)

#### Basic Upload
```bash
python oep/main.py --data data/parameter_photovoltaik_openfield.csv --table my_test_table
```

#### Upload with Metadata
```bash
python oep/main.py \
  --data data/parameter_photovoltaik_openfield.csv \
  --metadata data/parameter_photovoltaik_openfield.json \
  --table my_test_table
```

#### Advanced Options
```bash
# Upload to specific schema
python oep/main.py \
  --data data.csv \
  --table my_table \
  --topic model_draft

# With primary key
python oep/main.py \
  --data data.csv \
  --table my_table \
  --primary-key id

# Auto-delete existing table
python oep/main.py \
  --data data.csv \
  --table my_table \
  --delete-existing
```

### Programmatic Usage

Use the OEP Uploader in your Python scripts:

```python
from oep.main import OepUploader
import pandas as pd

# Initialize uploader
uploader = OepUploader(topic="sandbox")

# Read and upload data
df = uploader.read_data("data/parameter_photovoltaik_openfield.csv")
schema = uploader.create_table_schema(df, primary_key="year")

# Upload complete workflow
uploader.upload_complete(
    data_file="data/parameter_photovoltaik_openfield.csv",
    metadata_file="data/parameter_photovoltaik_openfield.json",
    table_name="my_table",
    primary_key="year"
)
```

See `example_usage.py` for more examples.

## Project Structure

```
oep-api/
├── oep/                    # Core uploader module
│   ├── __init__.py
│   └── main.py            # Standalone OEP uploader
├── data/                   # Sample data files
│   ├── parameter_photovoltaik_openfield.csv
│   ├── parameter_photovoltaik_openfield.json
│   └── ...
├── examples/               # Example data
│   ├── scalars/
│   └── sequences/
├── static/                 # Web UI assets
│   ├── main.js
│   ├── style.css
│   └── templates/
├── docs/                   # Documentation
├── example_usage.py        # Usage examples
├── requirements.txt        # Python dependencies
├── QUICK_START.md         # Quick start guide
└── OEP_UPLOADER_README.md # Detailed uploader docs
```

## Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[OEP Uploader Documentation](OEP_UPLOADER_README.md)** - Complete CLI reference
- **[Example Usage](example_usage.py)** - Python API examples
- **[MkDocs Documentation](docs/)** - Full documentation site

Build documentation:
```bash
mkdocs serve
```

## Example Data

The project includes example data in the `data/` and `examples/` directories:

- **Parameter data**: Photovoltaic and wind power plant parameters
- **Sequences data**: Feed-in profiles for wind power plants
- Both CSV and JSON metadata formats

## Getting an OEP API Token

1. Register at [openenergy-platform.org](https://openenergy-platform.org)
2. Navigate to your user profile
3. Go to Settings → API Token
4. Copy your token and set it as an environment variable

## OEP Schemas/Topics

- **sandbox** - For testing (default, recommended for first uploads)
- **model_draft** - For model drafts
- **scenario** - For scenario data
- And more... (see OEP documentation)

## Important Notes

- Always test in the **sandbox** schema first
- The sandbox schema may be periodically cleaned
- For production data, use appropriate schemas
- Follow OEP metadata standards

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See [LICENSE](LICENSE) file for details.

## Links

- [Open Energy Platform](https://openenergyplatform.org)
- [OEP Documentation](https://openenergy-platform.org/tutorials/)
- [OEP Client Library](https://github.com/OpenEnergyPlatform/oep-client)

## 💡 Troubleshooting

### "OEP API token not found"
Make sure you've set the `OEP_API_TOKEN` environment variable.

### "Table already exists"
Either delete the table manually on OEP or use the `--delete-existing` flag.

### "Failed to create table"
Check your table name (no special characters except underscore) and verify your API token has the correct permissions.

### CSV parsing issues
The tool automatically tries different separators. If issues persist, ensure your CSV file is properly formatted.

## Support

For issues related to:
- **This tool**: Open an issue on GitHub
- **OEP platform**: Contact the OEP team at [openenergy-platform.org](https://openenergy-platform.org)
