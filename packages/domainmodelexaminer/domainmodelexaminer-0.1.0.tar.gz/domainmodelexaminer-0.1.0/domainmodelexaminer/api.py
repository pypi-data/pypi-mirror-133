"""
DMX API

This is copied to main.py by the Dockerfile.
"""

from fastapi import FastAPI
from domainmodelexaminer.dmx import examine as dmxexamine

tags_metadata = [
  {
    "name": "examine",
    "description": "Takes Git URL and returns YAML (default) or JSON",
    "returns": "Returns YAML or JSON as a string."
  },
  {
    "name": "root",
    "description": "Confirms the beast is alive.",
  },
]

app = FastAPI(
  title="Domain Model eXaminer",
  description="Performs machine reading over the model codebase in order to automatically extract key metadata.",
  version="0.0.1",
  openapi_tags = tags_metadata
  )


@app.get("/", tags=["root"])
def read_root():
  return {"status": "running"}

@app.get("/examine/", tags=["examine"])
async def examine(url, return_json: bool = False):
  return dmxexamine(url, return_json=return_json)






