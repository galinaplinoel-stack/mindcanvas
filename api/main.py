"""MindCanvas REST API server."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

import sys
sys.path.insert(0, "..")
from mindcanvas import Generator, AutoLayout, Canvas, Exporter, __version__

app = FastAPI(
    title="MindCanvas API",
    description="AI Mind Mapping API",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = Generator()
layout = AutoLayout()
exporter = Exporter()


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    depth: int = Field(default=3, ge=1, le=5)
    max_branches: int = Field(default=6, ge=2, le=10)
    template: Optional[str] = None


class LayoutRequest(BaseModel):
    mind_map: dict
    algorithm: str = Field(default="radial")


@app.get("/")
def root():
    return {"name": "MindCanvas API", "version": __version__, "status": "running"}


@app.post("/generate")
def generate_map(req: GenerateRequest):
    try:
        mind_map = generator.generate(
            topic=req.topic,
            depth=req.depth,
            max_branches=req.max_branches,
            template=req.template,
        )
        return mind_map.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/templates")
def list_templates():
    return {"templates": generator.templates.list_templates()}


@app.post("/layout")
def apply_layout(req: LayoutRequest):
    try:
        from mindcanvas.models import MindMap
        mind_map = MindMap.from_dict(req.mind_map)
        layout.apply(mind_map, req.algorithm)
        return mind_map.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/export/json")
def export_json(mind_map_data: dict):
    from mindcanvas.models import MindMap
    mm = MindMap.from_dict(mind_map_data)
    return {"json": exporter.to_json(mm)}


@app.post("/export/markdown")
def export_markdown(mind_map_data: dict):
    from mindcanvas.models import MindMap
    mm = MindMap.from_dict(mind_map_data)
    return {"markdown": exporter.to_markdown(mm)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
