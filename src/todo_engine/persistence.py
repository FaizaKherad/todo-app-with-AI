"""
File-based persistence module for the Todo Engine.
Handles loading and saving tasks to/from a JSON file.
"""
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import tempfile


class FilePersistence:
    """
    Handles file-based persistence for tasks.
    """

    def __init__(self, file_path: str = None):
        # Use environment variable for storage path if available, otherwise default
        storage_path = os.getenv("STORAGE_PATH", "")
        if storage_path:
            # Use the storage path from environment with tasks.json
            self.file_path = os.path.join(storage_path, "tasks.json")
        else:
            # Default to current directory if no environment variable set
            self.file_path = "tasks.json" if file_path is None else file_path

        try:
            self.ensure_file_exists()
        except Exception as e:
            # If we can't create the file, that's an issue for the caller to handle
            # when they try to save
            pass
    
    def ensure_file_exists(self):
        """Ensure the persistence file exists, create if it doesn't."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """
        Load tasks from the persistence file.
        
        Returns:
            List of task dictionaries
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    # If file is empty, initialize with an empty list
                    tasks = []
                else:
                    tasks = json.loads(content)
                    
                # Validate that loaded data is a list
                if not isinstance(tasks, list):
                    raise ValueError(f"Invalid data format in {self.file_path}: expected list")
                
                return tasks
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.file_path}: {str(e)}")
        except FileNotFoundError:
            # If file doesn't exist, create it with an empty list
            self.ensure_file_exists()
            return []
        except Exception as e:
            raise Exception(f"Error loading tasks from {self.file_path}: {str(e)}")
    
    def save_tasks(self, tasks: List[Dict[str, Any]]) -> bool:
        """
        Save tasks to the persistence file atomically.
        
        Args:
            tasks: List of task dictionaries to save
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            # Write to a temporary file first
            temp_file = None
            try:
                # Create a temporary file in the same directory to ensure atomic move
                temp_dir = os.path.dirname(os.path.abspath(self.file_path)) or '.'
                with tempfile.NamedTemporaryFile(mode='w', dir=temp_dir, delete=False, suffix='.tmp') as f:
                    temp_file = f.name
                    json.dump(tasks, f, indent=2)
                
                # Atomically replace the original file
                os.replace(temp_file, self.file_path)
                return True
            except Exception:
                # Clean up temp file if something went wrong
                if temp_file and os.path.exists(temp_file):
                    os.remove(temp_file)
                raise
        except Exception as e:
            raise Exception(f"Error saving tasks to {self.file_path}: {str(e)}")
    
    def file_exists(self) -> bool:
        """
        Check if the persistence file exists.
        
        Returns:
            bool: True if file exists, False otherwise
        """
        return os.path.exists(self.file_path)


# Global persistence instance
persistence = FilePersistence()