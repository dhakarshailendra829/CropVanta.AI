import pandas as pd
import base64
import os
from pathlib import Path
from typing import List, Dict, Optional
from modules.core.logger import get_logger

logger = get_logger(__name__)

class PaperManager:
    def __init__(self, upload_dir: str = "uploaded_papers", metadata_file: str = "data/research_papers.csv"):
        self.upload_dir = Path(upload_dir)
        self.metadata_file = Path(metadata_file)
        self._init_storage()

    def _init_storage(self):
        """Ensures directories and metadata files exist."""
        if not self.upload_dir.exists():
            self.upload_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {self.upload_dir}")
            
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.metadata_file.exists():
            pd.DataFrame(columns=["Title", "Topic", "Uploader", "Filename", "Date"]).to_csv(self.metadata_file, index=False)

    def save_paper(self, uploaded_file, title: str, topic: str, uploader: str) -> bool:
        """Saves file to 'uploaded_papers' and logs metadata."""
        try:
            file_path = self.upload_dir / uploaded_file.name
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            df = pd.read_csv(self.metadata_file)
            new_entry = {
                "Title": title,
                "Topic": topic,
                "Uploader": uploader,
                "Filename": uploaded_file.name,
                "Date": pd.Timestamp.now().strftime("%Y-%m-%d")
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(self.metadata_file, index=False)
            
            logger.info(f"Paper saved successfully: {uploaded_file.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to save paper: {e}")
            return False

    def get_papers(self, query: Optional[str] = None) -> List[Dict]:
        """Retrieves papers from CSV metadata."""
        try:
            df = pd.read_csv(self.metadata_file)
            if query:
                df = df[df['Title'].str.contains(query, case=False) | df['Topic'].str.contains(query, case=False)]
            return df.to_dict(orient="records")
        except Exception as e:
            logger.error(f"Error reading papers: {e}")
            return []

    def get_paper_path(self, filename: str) -> str:
        """Returns the full string path for the PDF viewer."""
        path = self.upload_dir / filename
        return str(path) if path.exists() else None

    @staticmethod
    def get_pdf_base64(file_path: str) -> str:
        """Encodes PDF for embedding in Iframe."""
        try:
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Base64 Encoding failed: {e}")
            return ""