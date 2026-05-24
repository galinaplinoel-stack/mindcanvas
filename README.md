# MindCanvas — AI Mind Mapping

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-orange" alt="version">
  <img src="https://img.shields.io/badge/python-3.10+-blue" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
</p>

> 🧠 Interactive mind mapping powered by AI. Generate ideas, organize thoughts, and visualize connections on an infinite canvas.

## ✨ Features

- 🧠 **AI Generation** — Enter any topic, AI generates a complete mind map
- 🎨 **Infinite Canvas** — Unlimited workspace with drag, zoom, and pan
- 🔗 **Smart Connections** — Draw connections between any nodes
- 📐 **Auto Layout** — One-click smart arrangement
- 📷 **Export & Share** — Export as PNG, share links, embed in documents
- ⚡ **Templates** — Pre-built templates for common use cases

## 📁 Project Structure

```
mindcanvas/
├── mindcanvas/               # Core Python package
│   ├── __init__.py           # Package init + version
│   ├── canvas.py             # Canvas & node management
│   ├── generator.py          # AI mind map generation
│   ├── layout.py             # Auto-layout algorithms
│   ├── models.py             # Data models (Node, Edge, Map)
│   ├── templates.py          # Pre-built mind map templates
│   └── exporter.py           # Export to various formats
├── api/                      # REST API server
│   ├── __init__.py
│   └── main.py               # FastAPI application
├── web/                      # Frontend
│   └── index.html            # Interactive canvas UI
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_canvas.py        # Canvas tests
│   └── test_models.py        # Model tests
├── config.example.yaml       # Configuration template
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── vercel.json               # Vercel deployment config
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Quick Start

### Install
```bash
pip install -r requirements.txt
```

### Run API Server
```bash
cd api
uvicorn main:app --reload --port 8002
```

### Run Web Interface
```bash
cd web
python -m http.server 3002
# Open http://localhost:3002
```

### Use as Python Library
```python
from mindcanvas import MindMap, Generator, AutoLayout

# Create a mind map from a topic
gen = Generator()
mind_map = gen.generate("AI startup ideas", depth=3)

# Apply auto layout
layout = AutoLayout()
layout.apply(mind_map)

# Export
from mindcanvas import Exporter
exporter = Exporter()
exporter.to_json(mind_map, "output.json")
```

## 🔧 Configuration

```yaml
api:
  host: "0.0.0.0"
  port: 8002

generator:
  default_depth: 3
  max_branches: 6
  max_sub_branches: 3
  ai_enabled: false

layout:
  algorithm: "radial"     # radial, tree, force
  spacing: 200
  center_offset: 0

canvas:
  width: 2000
  height: 1500
  snap_to_grid: false
  grid_size: 20
```

## 🧪 Testing

```bash
python -m pytest tests/ -v
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

Organize your thoughts with AI ❤️
