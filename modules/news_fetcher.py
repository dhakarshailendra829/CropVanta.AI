import pandas as pd
import base64
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
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.metadata_file.exists():
            pd.DataFrame(columns=["Title", "Topic", "Uploader", "Filename", "Date"]).to_csv(self.metadata_file, index=False)

    def save_paper(self, uploaded_file, title: str, topic: str, uploader: str) -> bool:
        """Handles file saving and metadata entry."""
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
            return True
        except Exception as e:
            logger.error(f"Failed to save paper: {e}")
            return False

    def get_papers(self, query: Optional[str] = None) -> List[Dict]:
        """Retrieves and optionally filters papers."""
        df = pd.read_csv(self.metadata_file)
        if query:
            df = df[df['Title'].str.contains(query, case=False) | df['Topic'].str.contains(query, case=False)]
        return df.to_dict(orient="records")

    @staticmethod
    def get_pdf_base64(file_path: Path) -> str:
        """Encodes PDF for embedding."""
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')