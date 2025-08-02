from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    trained_file_path:str
    test_file_path:str