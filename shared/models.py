from pydantic import BaseModel, ConfigDict
from typing import Any, List, Optional
from enum import Enum

# data object for python test execution
class SingleTestRunResult(BaseModel):
    test_pass: bool
    error_message: Optional[str] = None
    input: Any
    actual_output: Any
    expected_output: Any

class TestRunnerState(str, Enum):
    UNKNOWN = 'UNKNOWN'
    INIT = 'INIT'
    LOAD = 'LOAD'
    COMPILE = 'COMPILE'
    BYTE_CODE = 'BYTE_CODE'
    READY = 'READY'
    RUN_TESTS = 'RUN_TESTS'
    LOAD_TESTCASE = 'LOAD_TESTCASE'
    COMPLETE = 'COMPLETE'

class TestRunnerResult(BaseModel):
    session_id: str
    test_outputs: List[SingleTestRunResult]
    num_total_tests: int
    num_tests_passed: int

# data class between autograder and testrunner
class JobError(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    error_type: str
    message: str
    testrunner_state: TestRunnerState

class JobResult(BaseModel):
    session_id: str
    error: Optional[JobError] = None
    test_results: Optional[TestRunnerResult] = None


# data class for the code grader
class GradeCodeError(BaseModel):
    error_type: str
    message: str

class GradeCodeResult(BaseModel):
    session_id: str
    error: Optional[GradeCodeError] = None
    test_results: Optional[TestRunnerResult] = None