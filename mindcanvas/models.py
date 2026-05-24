"""Data models for MindCanvas.

Defines the core structures: Node, Edge, and MindMap.
"""

from dataclasses import dataclass, field
from typing import Optional
import uuid
import json


@dataclass
class Node:
    """A single node in the mind map."""

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    text: str = ""
    x: float = 0.0
    y: float = 0.0
    node_type: str = "branch"  # center, branch, leaf
    color: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "x": self.x,
            "y": self.y,
            "type": self.node_type,
            "color": self.color,
            "metadata": self.metadata,
        }


@dataclass
class Edge:
    """A connection between two nodes."""

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    source_id: str = ""
    target_id: str = ""
    label: Optional[str] = None
    style: str = "solid"  # solid, dashed, dotted

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source_id,
            "target": self.target_id,
            "label": self.label,
            "style": self.style,
        }


@dataclass
class MindMap:
    """Complete mind map containing nodes and edges."""

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = "Untitled"
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_node(self, node: Node) -> Node:
        """Add a node to the mind map."""
        self.nodes.append(node)
        return node

    def add_edge(self, edge: Edge) -> Edge:
        """Add an edge to the mind map."""
        self.edges.append(edge)
        return edge

    def remove_node(self, node_id: str):
        """Remove a node and its connected edges."""
        self.nodes = [n for n in self.nodes if n.id != node_id]
        self.edges = [
            e for e in self.edges
            if e.source_id != node_id and e.target_id != node_id
        ]

    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def get_children(self, node_id: str) -> list[Node]:
        """Get all child nodes of a given node."""
        child_ids = [
            e.target_id for e in self.edges if e.source_id == node_id
        ]
        return [n for n in self.nodes if n.id in child_ids]

    def get_parent(self, node_id: str) -> Optional[Node]:
        """Get the parent node of a given node."""
        for e in self.edges:
            if e.target_id == node_id:
                return self.get_node(e.source_id)
        return None

    def get_center(self) -> Optional[Node]:
        """Get the center (root) node."""
        for n in self.nodes:
            if n.node_type == "center":
                return n
        return self.nodes[0] if self.nodes else None

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "metadata": self.metadata,
        }

    def to_json(self, indent: int = 2) -> str:
        """Export mind map as JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> "MindMap":
        """Create a MindMap from a dictionary."""
        mm = cls(id=data.get("id", ""), title=data.get("title", ""))
        mm.nodes = [
            Node(
                id=n["id"], text=n["text"],
                x=n.get("x", 0), y=n.get("y", 0),
                node_type=n.get("type", "branch"),
                color=n.get("color"),
            )
            for n in data.get("nodes", [])
        ]
        mm.edges = [
            Edge(
                id=e["id"], source_id=e["source"],
                target_id=e["target"], label=e.get("label"),
            )
            for e in data.get("edges", [])
        ]
        return mm
