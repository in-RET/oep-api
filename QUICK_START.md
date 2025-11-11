# OEP Data Uploader - Quick Start Guide

## Was wurde erstellt?

Ein vollständiges, eigenständiges Python-Programm zum Hochladen von Daten auf die Open Energy Platform (OEP).

### Dateien:
1. **`oep/uploader.py`** - Hauptprogramm (eigenständig, keine Abhängigkeiten von anderen Projektdateien)
2. **`OEP_UPLOADER_README.md`** - Vollständige Dokumentation
3. **`example_usage.py`** - Beispielskript für programmatische Nutzung

## Schnellstart

### 1. API Token setzen

```bash
# Linux/Mac
export OEP_API_TOKEN="your-token-here"

# Windows (CMD)
set OEP_API_TOKEN=your-token-here

# Windows (PowerShell)
$env:OEP_API_TOKEN="your-token-here"
```

Holen Sie sich ihren Token von: https://openenergy-platform.org/user/settings

### 2. Daten hochladen

```bash
# Einfachster Upload
python oep/uploader.py \
  --data data/parameter_photovoltaik_openfield.csv \
  --table my_test_table

# Mit Metadaten
python oep/uploader.py \
  --data data/parameter_photovoltaik_openfield.csv \
  --metadata data/parameter_photovoltaik_openfield.json \
  --table my_test_table
```

### 3. Hilfe anzeigen

```bash
python oep/uploader.py --help
```

## Features

- CSV und Excel Upload (.csv, .xlsx, .xls)
- Automatische Schema-Erkennung
- JSON Metadaten Upload
- Verschiedene Trennzeichen (`,`, `;`, Tab)
- Primary Key Unterstützung
- Überschreiben existierender Tabellen
- Vollständiges CLI und Python API

## Programmatische Verwendung

```python
from oep.uploader import OepUploader

uploader = OepUploader(token="your-token", topic="sandbox")

uploader.upload_complete(
    data_file="data.csv",
    table_name="my_table",
    metadata_file="metadata.json",  # optional
    primary_key="id",  # optional
    delete_existing=True  # optional
)
```

## Beispiele

Siehe `example_usage.py` für mehr Beispiele.

Für vollständige Dokumentation siehe `OEP_UPLOADER_README.md`.

