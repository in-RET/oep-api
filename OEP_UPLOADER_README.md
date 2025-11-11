# OEP Data Uploader

Ein vollständiges, eigenständiges Python-Programm zum Hochladen von Daten auf die Open Energy Platform (OEP).

## Features

- Upload von CSV-Daten zur OEP
- Automatische Erstellung von Tabellenschemas aus CSV-Struktur
- Upload von JSON-Metadaten (OEP Metadata Format)
- Unterstützung verschiedener CSV-Trennzeichen (`,`, `;`, Tab)
- Unterstützung von Excel-Dateien (.xlsx, .xls)
- Automatische Typ-Inferenz (bigint, text, double precision, etc.)
- Verwaltung existierender Tabellen (Löschen/Überschreiben)
- Vollständiges CLI-Interface
- Keine Abhängigkeiten von anderen Projektdateien

## Installation

### Voraussetzungen

```bash
pip install pandas oep-client
```

Optional für Excel-Support:
```bash
pip install openpyxl
```

### OEP API Token

Sie benötigen einen API-Token von der Open Energy Platform:

1. Registrieren Sie sich auf [openenergy-platform.org](https://openenergy-platform.org)
2. Gehen Sie zu Ihrem Profil → API Token
3. Kopieren Sie Ihren Token
4. Setzen Sie die Umgebungsvariable:

```bash
# Linux/Mac
export OEP_API_TOKEN="your-token-here"

# Windows (CMD)
set OEP_API_TOKEN=your-token-here

# Windows (PowerShell)
$env:OEP_API_TOKEN="your-token-here"
```

## Verwendung

### Grundlegende Verwendung

```bash
# Nur Daten hochladen (CSV)
python oep/uploader.py --data data/parameter_photovoltaik_openfield.csv --table my_test_table

# Daten mit Metadaten hochladen
python oep/uploader.py \
  --data data/parameter_photovoltaik_openfield.csv \
  --metadata data/parameter_photovoltaik_openfield.json \
  --table my_test_table
```

### Erweiterte Optionen

```bash
# In ein anderes Schema hochladen (nicht sandbox)
python oep/uploader.py \
  --data data.csv \
  --table my_table \
  --topic model_draft

# Mit Primary Key
python oep/uploader.py \
  --data data.csv \
  --table my_table \
  --primary-key id

# Existierende Tabelle automatisch löschen (keine Nachfrage)
python oep/uploader.py \
  --data data.csv \
  --table my_table \
  --delete-existing

# Token direkt übergeben (statt Umgebungsvariable)
python oep/uploader.py \
  --data data.csv \
  --table my_table \
  --token "your-token-here"
```

### Vollständiges Beispiel

```bash
python oep/uploader.py \
  --data data/parameter_photovoltaik_openfield.csv \
  --metadata data/parameter_photovoltaik_openfield.json \
  --table parameter_pv_openfield_test \
  --topic sandbox \
  --primary-key year \
  --delete-existing
```

## Kommandozeilen-Argumente

| Argument | Erforderlich | Beschreibung |
|----------|---------|--------------|
| `--data` | Ja | Pfad zur CSV-Datendatei |
| `--table` | Ja | Name der Tabelle auf OEP |
| `--metadata` | Nein | Pfad zur JSON-Metadatendatei |
| `--topic` | Nein | OEP Schema/Topic (Standard: `sandbox`) |
| `--primary-key` | Nein | Name der Primary-Key-Spalte |
| `--delete-existing` | Nein | Existierende Tabelle ohne Nachfrage löschen |
| `--token` | Nein | OEP API Token (alternativ zu Umgebungsvariable) |

## Unterstützte Datentypen

Das Programm erkennt automatisch folgende Datentypen:

| Pandas Dtype | SQL Type |
|--------------|----------|
| int64, int32, etc. | bigint |
| float64, float32 | double precision |
| bool | boolean |
| datetime64 | timestamp |
| object (Standard) | text |

## Beispiel-Ausgabe

```
============================================================
OEP Data Upload
============================================================
Topic/Schema: sandbox
Table: parameter_pv_test
Data file: data/parameter_photovoltaik_openfield.csv
Metadata file: data/parameter_photovoltaik_openfield.json
============================================================

Reading data from 'data/parameter_photovoltaik_openfield.csv'...
✓ Data loaded: 6 rows, 5 columns
  Columns: year, investment_costs, operating_costs, lifetime, interest_rate

Creating table schema...
✓ Schema created with 5 columns
Creating table 'parameter_pv_test' in schema 'sandbox'...
✓ Table 'parameter_pv_test' created successfully
Uploading 6 records to table 'parameter_pv_test'...
✓ Data uploaded successfully (6 records)

Reading metadata from 'data/parameter_photovoltaik_openfield.json'...
✓ Metadata loaded
Uploading metadata to table 'parameter_pv_test'...
✓ Metadata uploaded successfully

============================================================
✓ Upload completed successfully!
============================================================

View your table at:
https://openenergy-platform.org/dataedit/view/sandbox/parameter_pv_test
```

## Fehlerbehandlung

### Häufige Fehler

**1. Token nicht gefunden**
```
Error: OEP API token not found. Set OEP_API_TOKEN environment variable or pass token parameter.
```
→ Lösung: Setzen Sie die Umgebungsvariable `OEP_API_TOKEN` oder verwenden Sie `--token`

**2. Datei nicht gefunden**
```
Error: Data file not found: data.csv
```
→ Lösung: Überprüfen Sie den Dateipfad

**3. Tabelle existiert bereits**
```
Warning: Table 'my_table' already exists in schema 'sandbox'
Delete existing table and recreate? (yes/no):
```
→ Lösung: Antworten Sie mit `yes` oder verwenden Sie `--delete-existing`

## Programmierbare Verwendung

Sie können den Uploader auch direkt in Python verwenden:

```python
from oep.uploader import OepUploader

# Uploader initialisieren
uploader = OepUploader(
    token="your-token-here",  # oder None für Umgebungsvariable
    topic="sandbox"
)

# Daten hochladen
uploader.upload_complete(
    data_file="data/my_data.csv",
    table_name="my_table",
    metadata_file="data/my_metadata.json",  # optional
    primary_key="id",  # optional
    delete_existing=True  # optional
)
```

### Einzelne Funktionen verwenden

```python
from oep.uploader import OepUploader

uploader = OepUploader()

# Prüfen ob Tabelle existiert
exists = uploader.table_exists("my_table")

# Tabelle löschen
uploader.delete_table("my_table")

# Daten lesen
df = uploader.read_data("data.csv")

# Schema erstellen
schema = uploader.create_table_schema(df, primary_key="id")

# Tabelle erstellen
uploader.create_table("my_table", schema)

# Daten hochladen
records = uploader.dataframe_to_records(df)
uploader.upload_data("my_table", records)

# Metadaten hochladen
metadata = uploader.read_metadata("metadata.json")
uploader.upload_metadata("my_table", metadata)
```

## Verfügbare OEP Topics/Schemas

- `sandbox` - Für Tests und Experimente (Standard)
- `model_draft` - Für Modellentwürfe
- `scenario` - Für Szenarien
- `supply` - Für Versorgungsdaten
- `demand` - Für Bedarfsdaten
- `climate` - Für Klimadaten
- Weitere: Siehe [OEP Dokumentation](https://openenergy-platform.org/dataedit/schemas)

## CSV-Format

Das Programm unterstützt verschiedene CSV-Formate:

### Beispiel 1: Komma-getrennt
```csv
year,investment_costs,operating_costs
2025,600000,2
2030,550000,2
```

### Beispiel 2: Semikolon-getrennt
```csv
year;investment_costs;operating_costs
2025;600000;2
2030;550000;2
```

### Beispiel 3: Tab-getrennt
```csv
year	investment_costs	operating_costs
2025	600000	2
2030	550000	2
```

Das Programm erkennt automatisch das verwendete Trennzeichen.

## Metadata-Format

Metadaten müssen im [OEP Metadata Format](https://github.com/OpenEnergyPlatform/oemetadata) vorliegen. Siehe Beispieldateien im `data/` Ordner.

## Lizenz

Siehe LICENSE-Datei im Projektverzeichnis.

## Support

Bei Fragen oder Problemen:
- OEP Forum: [forum.openmod-initiative.org](https://forum.openmod-initiative.org/)
- OEP GitHub: [github.com/OpenEnergyPlatform](https://github.com/OpenEnergyPlatform)
- OEP Client Dokumentation: [oep-client.readthedocs.io](https://oep-client.readthedocs.io/)

