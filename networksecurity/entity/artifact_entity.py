from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    trained_file_path:str
    test_file_path:str

    '''
    
    | Element                  | Purpose                                                          |
| ------------------------ | ---------------------------------------------------------------- |
| `@dataclass`             | Auto-generates init, repr, etc., for clean data holder classes   |
| `DataIngestionArtifacts` | Holds output paths (`train`, `test`) of the data ingestion stage |
| `artifact_entity.py`     | Organized location for all artifact-related data classes         |


In ML pipelines:

Artifacts are the outputs of each pipeline stage.

For data ingestion, the artifacts are the paths to the split files (train.csv, test.csv).

This DataIngestionArtifacts class is used to return and pass those output paths between different components.

✅ Automatic __init__() method
You don't need to manually write the constructor. Python auto-generates it like:

python
Copy
Edit
def __init__(self, trained_file_path: str, test_file_path: str):
    self.trained_file_path = trained_file_path
    self.test_file_path = test_file_path
    
    '''


@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_File_path:str
    invalid_test_file_path:str
    drift_report_file_path:str