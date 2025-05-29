from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pandas as pd # Potentially needed if models or route signatures depend on it indirectly
import json # Potentially needed
import ast # Potentially needed

# Attempt to import Pydantic models used in main.py routes
try:
    from source.schemas.matched_resume import ResumeMatchedModel
    from source.schemas.jobextracted import JobExtractedModel
    print("Successfully imported Pydantic models.")
except ImportError as e:
    print(f"Error importing Pydantic models: {e}")
    # If models can't be imported, there's a deeper issue or path problem
    # For now, proceed to see if FastAPI itself initializes
    ResumeMatchedModel = None
    JobExtractedModel = None

# Mock database object if it's used at the global scope or during import of other modules
class MockCollection:
    async def insert_one(self, data):
        print(f"MockCollection.insert_one called with {data}")
        return MockInsertOneResult()
    
    async def to_list(self, length):
        print(f"MockCollection.to_list called with length {length}")
        return []

    def find(self, *args, **kwargs):
        print(f"MockCollection.find called with {args} {kwargs}")
        return self # Return self to allow chaining .sort().limit()
    
    def sort(self, *args, **kwargs):
        print(f"MockCollection.sort called with {args} {kwargs}")
        return self # Return self for chaining
    
    def limit(self, *args, **kwargs):
        print(f"MockCollection.limit called with {args} {kwargs}")
        return self # Return self for chaining


class MockDatabase:
    def __init__(self):
        self.jobsextracted = MockCollection()
        self.matches = MockCollection()

    def get_collection(self, name):
        print(f"MockDatabase.get_collection called with {name}")
        if name == "jobsextracted":
            return self.jobsextracted
        elif name == "matches":
            return self.matches
        return MockCollection()

class MockInsertOneResult:
    def __init__(self):
        self.inserted_id = "mock_id"

# Replace actual database with mock
# This needs to be done carefully if 'source.db_helpers.db_connection.database' is imported elsewhere
# For now, we assume this direct import in main.py is what we need to bypass for initialization
# A more robust way would be to use monkeypatching if this script were a pytest test.

# Mocking the services that might be initialized globally or at import time
class MockJobInfoExtraction:
    def __init__(self, *args, **kwargs):
        print("MockJobInfoExtraction initialized")
    def extract_entities(self, jobs_df):
        print("MockJobInfoExtraction.extract_entities called")
        # Return a DataFrame with expected columns to avoid errors in route logic
        # if it's not fully commented out.
        return pd.DataFrame(columns=['Minimum degree level', 'Acceptable majors', 'Skills'])

class MockRules:
    def __init__(self, *args, **kwargs):
        print("MockRules initialized")
    def matching_score(self, resumes, jobs, job_index):
        print("MockRules.matching_score called")
        # Return a DataFrame with expected columns
        # Example columns, adjust based on actual usage in the route
        return pd.DataFrame(columns=['_id', f'Degree job {job_index} matching', 
                                     f'Major job {job_index} matching', 
                                     f'Skills job {job_index} semantic matching',
                                     f'matching score job {job_index}'])

# Monkey patch before app definition that might trigger imports
import sys
from unittest.mock import MagicMock

# Mock modules that interact with DB or read files at import time
sys.modules['source.db_helpers.db_connection'] = MagicMock()
sys.modules['source.db_helpers.db_connection'].database = MockDatabase()

# If JobInfoExtraction or Rules are instantiated globally in main or schemas, mock them too
sys.modules['services.JobInfoExtraction'] = MagicMock(JobInfoExtraction=MockJobInfoExtraction)
sys.modules['services.Rules'] = MagicMock(Rules=MockRules)


print("Attempting to initialize FastAPI app...")
app = FastAPI()
print("FastAPI app initialized.")

# Utility function from main.py, keep as is if it doesn't have external deps by itself
def transform_dataframe_to_json(dataframe):
    result = dataframe.to_json(orient="records")
    parsed = json.loads(result)
    json_data = json.dumps(parsed, indent=4)
    return json_data

def modifying_type_resume(resumes):
    # This function might fail if resumes is not a DataFrame with 'degrees' and 'skills' columns
    # For init test, it might not be called if route logic is skipped.
    print("modifying_type_resume called")
    if "degrees" in resumes and "skills" in resumes:
        for i in range(len(resumes["degrees"])):
            resumes["degrees"][i] = ast.literal_eval(resumes["degrees"][i])
        for i in range(len(resumes["skills"])):
            resumes["skills"][i] = ast.literal_eval(resumes["skills"][i])
    return resumes

def modifying_type_job(jobs):
    print("modifying_type_job called")
    if "Skills" in jobs:
        for i in range(len(jobs["Skills"])):
            jobs["Skills"][i] = ast.literal_eval(jobs["Skills"][i])
    return jobs

# Define routes with their logic commented out or replaced by pass
@app.get("/extraction")
async def extraction_route():
    print("Extraction route defined.")
    # Original logic commented out:
    # degrees_patterns_path = 'Resources/data/degrees.jsonl'
    # majors_patterns_path = 'Resources/data/majors.jsonl'
    # skills_patterns_path = 'Resources/data/skills.jsonl'
    # jobs = pd.read_csv('Resources/data/job descriptions.csv', index_col=0)
    # jobs = jobs[['Qualifications']]
    # job_extraction = JobInfoExtraction(skills_patterns_path, majors_patterns_path, degrees_patterns_path, jobs)
    # jobs_df = job_extraction.extract_entities(jobs)
    # for i, row in jobs_df.iterrows():
    #     minimum_degree_level = jobs_df['Minimum degree level'][i]
    #     acceptable_majors = jobs_df['Acceptable majors'][i]
    #     skills = jobs_df['Skills'][i]
    #     job_extracted = JobExtractedModel(minimum_degree_level=minimum_degree_level if minimum_degree_level else '',
    #                                       acceptable_majors=acceptable_majors if acceptable_majors else [],
    #                                       skills=skills if skills else [])
    #     job_extracted_encoded = jsonable_encoder(job_extracted)
    #     # new_job_extracted = await database.get_collection("jobsextracted").insert_one(job_extracted_encoded)
    # # jobs_json = transform_dataframe_to_json(jobs_df)
    # return {"message": "Extraction endpoint (mocked)"}
    pass

@app.get("/matching")
async def matching_route():
    print("Matching route defined.")
    # Original logic commented out:
    # with open('Resources/data/labels.json') as fp:
    #     labels = json.load(fp)
    # jobs_df = pd.read_csv('Resources/data/job_description_by_spacy.csv', index_col=0)
    # resumes_df = pd.read_csv('Resources/data/resumes_by_spacy.csv', index_col=0)
    # resumes_df = modifying_type_resume(resumes_df)
    # jobs_df = modifying_type_job(jobs_df)
    # rules = Rules(labels, resumes_df, jobs_df)
    # job_indexes = [0, 1, 2, 3, 4]
    # resumes_matched_jobs = pd.DataFrame()
    # for job_index in job_indexes:
    #     resumes_matched = rules.matching_score(resumes_df, jobs_df, job_index)
    #     resumes_matched_jobs = resumes_matched_jobs.append(resumes_matched)
    #     for i, row in resumes_matched.iterrows():
    #         id_resume = resumes_matched['_id'][i]
    #         degree_matching = float(resumes_matched['Degree job ' + str(job_index) + ' matching'][i])
    #         major_matching = float(resumes_matched['Major job ' + str(job_index) + ' matching'][i])
    #         skills_semantic_matching = float(resumes_matched['Skills job ' + str(job_index) + ' semantic matching'][i])
    #         matching_score = float(resumes_matched['matching score job ' + str(job_index)][i])
    #         matched_resume_model = ResumeMatchedModel(id_resume=id_resume if id_resume else '',
    #                                             job_index=job_index if job_index else 0,
    #                                             degree_matching=degree_matching if degree_matching else 0,
    #                                             major_matching=major_matching if major_matching else 0,
    #                                             skills_semantic_matching=skills_semantic_matching
    #                                             if skills_semantic_matching else 0,
    #                                             matching_score=matching_score if matching_score else 0)
    #         matched_resume_encoded = jsonable_encoder(matched_resume_model)
    #         # new_matched_resume = await database.get_collection("matches").insert_one(matched_resume_encoded)
    # # resumes_matched_json = transform_dataframe_to_json(resumes_matched_jobs)
    # return {"message": "Matching endpoint (mocked)"}
    pass

@app.get("/top_resumes")
async def top_resumes_route(): # Renamed from extraction to avoid conflict
    print("Top resumes route defined.")
    # Original logic commented out:
    # top_resumes_cursor = database.matches.find().sort("matching_score", -1).limit(5)
    # result = []
    # top_resumes_list = await top_resumes_cursor.to_list(None)
    # for x in top_resumes_list:
    #     result.append(x)
    # top_resumes_json = jsonable_encoder(result)
    # return {"message": "Top resumes endpoint (mocked)"}
    pass

print("Route definitions processed.")
print("Test script finished. If no ValueError occurred before this, initialization is likely fine.")
