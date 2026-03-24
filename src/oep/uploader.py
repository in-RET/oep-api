"""
OEP data uploader library helpers.

Provides the `OepUploader` class to upload CSV/Excel data and JSON metadata
into an Open Energy Platform (OEP) topic. Can be used programmatically or via
the batch script in `main.py`.

Quick usage:
    from oep.uploader import OepUploader
    uploader = OepUploader(topic="sandbox")
    uploader.upload_complete(
        data_file="data.csv",
        metadata_file="data.json",
        table_name="my_table",
        primary_key="id",
        delete_existing=True,
    )

Environment Variables:
    OEP_API_TOKEN: Your OEP API token (required unless passed to OepUploader)
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, List, Any

import pandas as pd
from oep_client import OepClient


class OepUploader:
    """Standalone OEP data uploader"""

    def __init__(self, token: Optional[str] = None, topic: str = "sandbox"):
        """
        Initialize OEP uploader

        Args:
            token: OEP API token (defaults to OEP_API_TOKEN env variable)
            topic: OEP schema/topic (default: sandbox)
        """
        self.token = token or os.getenv("OEP_API_TOKEN")
        if not self.token:
            raise ValueError("OEP API token not found. Set OEP_API_TOKEN environment variable or pass token parameter.")

        self.topic = topic
        self.client = OepClient(token=self.token)

    def infer_sql_type(self, dtype: str, sample_value: Any = None) -> str:
        """
        Infer SQL data type from pandas dtype

        Args:
            dtype: Pandas dtype as string
            sample_value: Sample value to help with type inference

        Returns:
            SQL data type as string
        """
        dtype_str = str(dtype).lower()

        if 'int' in dtype_str:
            return 'bigint'
        elif 'float' in dtype_str or 'double' in dtype_str:
            return 'double precision'
        elif 'bool' in dtype_str:
            return 'boolean'
        elif 'datetime' in dtype_str or 'date' in dtype_str:
            return 'timestamp'
        else:
            return 'text'

    def create_table_schema(self, df: pd.DataFrame, primary_key: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Create table schema from pandas DataFrame

        Args:
            df: Pandas DataFrame
            primary_key: Name of primary key column (optional)

        Returns:
            Table schema dictionary for OEP
        """
        columns = []

        for col_name in df.columns:
            sample_value = df[col_name].iloc[0] if len(df) > 0 else None
            sql_type = self.infer_sql_type(str(df[col_name].dtype), sample_value)

            column_def: Dict[str, Any] = {
                "name": col_name,
                "data_type": sql_type,
            }

            if primary_key and col_name == primary_key:
                column_def["primary_key"] = True

            columns.append(column_def)

        return {"columns": columns}

    def read_data(self, file_path: str) -> pd.DataFrame:
        """
        Read data from CSV file

        Args:
            file_path: Path to CSV file

        Returns:
            Pandas DataFrame
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        if path.suffix.lower() == '.csv':
            # Try different separators
            for sep in [',', ';', '\t']:
                try:
                    df = pd.read_csv(file_path, sep=sep)
                    if len(df.columns) > 1:
                        return df
                except Exception:
                    continue
            # Fallback to default
            return pd.read_csv(file_path)
        elif path.suffix.lower() in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

    def read_metadata(self, file_path: str) -> Dict:
        """
        Read metadata from JSON file

        Args:
            file_path: Path to JSON metadata file

        Returns:
            Metadata dictionary
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Metadata file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def dataframe_to_records(self, df: pd.DataFrame) -> List[Dict]:
        """
        Convert DataFrame to list of records for OEP upload

        Args:
            df: Pandas DataFrame

        Returns:
            List of dictionaries (records)
        """
        # Replace NaN with None for JSON serialization
        df = df.where(pd.notna(df), None)
        return json.loads(df.to_json(orient='records'))

    def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists on OEP

        Args:
            table_name: Name of the table

        Returns:
            True if table exists, False otherwise
        """
        try:
            # Try to get table metadata - if it exists, this won't raise an exception
            self.client.get_metadata(table=table_name)
            return True
        except Exception:
            return False

    def create_table(self, table_name: str, schema: Dict) -> None:
        """
        Create table on OEP

        Args:
            table_name: Name of the table
            schema: Table schema dictionary
        """
        # print(f"Creating table '{table_name}' in schema '{self.topic}'...")
        try:
            self.client.create_table(table=table_name, definition=schema)
            print(f"Table '{table_name}' created successfully")
        except Exception as e:
            raise Exception(f"Failed to create table: {str(e)}")

    def upload_data(self, table_name: str, data: List[Dict]) -> None:
        """
        Upload data to OEP table

        Args:
            table_name: Name of the table
            data: List of records to upload
        """
        # print(f"Uploading {len(data)} records to table '{table_name}'...")
        try:
            self.client.insert_into_table(table=table_name, data=data)
            print(f"Data uploaded successfully ({len(data)} records)")
        except Exception as e:
            raise Exception(f"Failed to upload data: {str(e)}")

    def upload_metadata(self, table_name: str, metadata: Dict) -> None:
        """
        Upload metadata to OEP table

        Args:
            table_name: Name of the table
            metadata: Metadata dictionary
        """
        # print(f"Uploading metadata to table '{table_name}'...")
        try:
            self.client.set_metadata(table=table_name, metadata=metadata)
            # print(f"Metadata uploaded successfully")
        except Exception as e:
            raise Exception(f"Failed to upload metadata: {str(e)}")

    def delete_table(self, table_name: str) -> None:
        """
        Delete table from OEP

        Args:
            table_name: Name of the table
        """
        # print(f"Deleting table '{table_name}'...")
        try:
            self.client.drop_table(table=table_name)
            # print(f"Table '{table_name}' deleted successfully")
        except Exception as e:
            raise Exception(f"Failed to delete table: {str(e)}")

    def upload_complete(
        self,
        data_file: str,
        table_name: str,
        metadata_file: Optional[str] = None,
        primary_key: Optional[str] = None,
        delete_existing: bool = False
    ) -> None:
        """
        Complete upload workflow: create table, upload data and metadata

        Args:
            data_file: Path to CSV data file
            table_name: Name of the table on OEP
            metadata_file: Path to JSON metadata file (optional)
            primary_key: Name of primary key column (optional)
            delete_existing: Delete existing table before upload (default: False)
        """
        # Check if table exists
        if self.table_exists(table_name):
            if delete_existing:
                self.delete_table(table_name)
            else:
                print(f"Warning: Table '{table_name}' already exists in schema '{self.topic}'")
                response = input("Delete existing table and recreate? (yes/no): ")
                if response.lower() in ['yes', 'y']:
                    self.delete_table(table_name)
                else:
                    print("Upload cancelled.")
                    return

        # Read data
        df = self.read_data(data_file)

        # Create table schema
        schema = self.create_table_schema(df, primary_key=primary_key)

        # Create table
        self.create_table(table_name, schema)

        # Upload data
        records = self.dataframe_to_records(df)
        self.upload_data(table_name, records)

        # Upload metadata if provided
        if metadata_file:
            metadata = self.read_metadata(metadata_file)
            self.upload_metadata(table_name, metadata)