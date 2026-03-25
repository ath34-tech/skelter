from pydantic import BaseModel
from typing import List, Optional



class StackRequest(BaseModel):
    stack: str
    usecase: str


class ArchitectureResponse(BaseModel):
    folders: List[str]
    files: List[str]

class WalkthroughRequest(BaseModel):
    stack: str
    usecase: str
    architecture: ArchitectureResponse

class DocsResponse(BaseModel):
    prd: str
    walkthrough: str
    hld: str