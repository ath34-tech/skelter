from skelter.server.agent.prompts import ARCH_PROMPT, WALKTHROUGH_PROMPT, PRD_PROMPT, HLD_PROMPT
from skelter.server.core.client import invoke_client

def plan_architecture(stack: str, usecase: str):
    prompts = ARCH_PROMPT.format(stack=stack, usecase=usecase)
    response = invoke_client(prompts)
    return response

def generate_prd(stack: str, usecase: str):
    prompts = PRD_PROMPT.format(stack=stack, usecase=usecase)
    response = invoke_client(prompts)
    return response

def generate_walkthrough(stack: str, usecase: str, folders: list, files: list):
    prompts = WALKTHROUGH_PROMPT.format(stack=stack, usecase=usecase, folders=folders, files=files)
    response = invoke_client(prompts)
    return response

def generate_hld(stack: str, usecase: str, folders: list, files: list):
    prompts = HLD_PROMPT.format(stack=stack, usecase=usecase, folders=folders, files=files)
    response = invoke_client(prompts)
    return response


