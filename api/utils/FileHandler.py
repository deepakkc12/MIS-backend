from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.conf import settings
from typing import Optional, Dict, Any
import os
import uuid
from datetime import datetime
import logging
from pathlib import Path

class FileHandler:

    
    ALLOWED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png'],
        'document': ['.pdf', '.txt', '.csv'],

    }

    IMAGE_STORAGE = "images/"

    MAX_FILE_SIZE = 10 * 1024 * 1024  
    
    def __init__(self):
        self.storage = default_storage
        self.logger = logging.getLogger(__name__)
        self.saved_path = None
        # self.base_upload_path = getattr(settings, 'UPLOAD_ROOT')
        # os.makedirs(self.base_upload_path, exist_ok=True)
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename using UUID and timestamp."""
        ext = os.path.splitext(original_filename)[1].lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        return f"{timestamp}_{unique_id}{ext}"
    
    def validate_file(self, file_obj) -> None:
        """Validate file size and extension."""
        # Size validation
        if file_obj.size > self.MAX_FILE_SIZE:
            raise ValidationError("File size exceeds the maximum limit.")
        
        # Extension validation
        ext = os.path.splitext(file_obj.name)[1].lower()
        if ext not in [e for exts in self.ALLOWED_EXTENSIONS.values() for e in exts]:
            raise ValidationError("Invalid file type.")
    
    def save(self, file_obj, subdirectory: str = '') -> Optional[Dict[str, Any]]:
        """Save file and return file details."""
        try:
            # Validate file
            self.validate_file(file_obj)
            
            # Generate unique filename and path
            unique_filename = self.generate_unique_filename(file_obj.name)
            relative_path = os.path.join( subdirectory, unique_filename)
            
            # Save file
            saved_path = self.storage.save(relative_path, file_obj)
            
            self.saved_path = saved_path
            
            return {
                'original_name': file_obj.name,
                'saved_name': unique_filename,
                'path': saved_path,
                'size': file_obj.size,
                'uploaded_at': datetime.now().isoformat(),
            }
        except ValidationError as ve:
            self.logger.warning(f"Validation error: {ve}")
            raise
        except Exception as e:
            self.logger.error(f"Error saving file: {e}")
            return None
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file if it exists."""
        try:
            if self.storage.exists(file_path):
                self.storage.delete(file_path)
                self.logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting file: {e}")
            return False
    
    def list_files(self, directory: str = '') -> Optional[list]:
        """List files in the specified directory."""
        try:
            full_path = Path(self.storage, directory)
            if full_path.exists() and full_path.is_dir():
                return [str(file) for file in full_path.iterdir() if file.is_file()]
            return []
        except Exception as e:
            self.logger.error(f"Error listing files: {e}")
            return None
