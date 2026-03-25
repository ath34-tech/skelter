from setuptools import setup, find_packages

setup(
    name="skelter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi[standard]>=0.135.2",
        "groq>=0.30.0,<1",
        "httpx>=0.28.1",
        "langchain>=1.2.13",
        "langchain-groq>=1.1.2",
        "pydantic>=2.12.5",
        "pyinstaller>=6.19.0",
        "python-dotenv>=1.2.2",
        "typer>=0.24.1",
        "uvicorn>=0.42.0",
    ],
    entry_points={
        "console_scripts": [
            "skelter=skelter.cli.main:app",
        ],
    },
)
