from fastapi import APIRouter
from skelter.server.core.models import StackRequest, ArchitectureResponse, DocsResponse, WalkthroughRequest
from skelter.server.agent.planner import plan_architecture, generate_walkthrough, generate_prd, generate_hld
from skelter.server.core.utils import clean_json_response
import json

router = APIRouter()

@router.post("/generate-architecture", response_model=ArchitectureResponse)
def generate_architecture(req: StackRequest):
    response = plan_architecture(req.stack, req.usecase)
    plan = clean_json_response(response.content)
    return ArchitectureResponse(
        folders=plan["folders"],
        files=plan["files"],
    )

@router.post("/generate-docs", response_model=DocsResponse)
def generate_docs_api(req: WalkthroughRequest):
    prd_resp = generate_prd(req.stack, req.usecase)
    walk_resp = generate_walkthrough(req.stack, req.usecase, req.architecture.folders, req.architecture.files)
    hld_resp = generate_hld(req.stack, req.usecase, req.architecture.folders, req.architecture.files)
    
    return DocsResponse(
        prd=prd_resp.content,
        walkthrough=walk_resp.content,
        hld=hld_resp.content
    )