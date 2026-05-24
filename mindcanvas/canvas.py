"""Canvas management for MindCanvas.

Handles the interactive canvas state including nodes, edges,
view transforms, and undo/redo.
"""

from .models import Node, Edge, MindMap


class Canvas:
    """Interactive mind map canvas with state management."""

    def __init__(self, width: int = 2000, height: int = 1500):
        self.width = width
        self.height = height
        self.mind_map = MindMap()
        self._undo_stack: list[dict] = []
        self._redo_stack: list[dict] = []
        self._zoom: float = 1.0
        self._pan_x: float = 0.0
        self._pan_y: float = 0.0

    def set_map(self, mind_map: MindMap):
        """Load a mind map into the canvas."""
        self._save_state()
        self.mind_map = mind_map

    def add_node(
        self, text: str, x: float, y: float, node_type: str = "branch"
    ) -> Node:
        """Add a new node to the canvas."""
        self._save_state()
        node = Node(text=text, x=x, y=y, node_type=node_type)
        self.mind_map.add_node(node)
        return node

    def remove_node(self, node_id: str):
        """Remove a node and its connections."""
        self._save_state()
        self.mind_map.remove_node(node_id)

    def move_node(self, node_id: str, x: float, y: float):
        """Move a node to a new position."""
        node = self.mind_map.get_node(node_id)
        if node:
            self._save_state()
            node.x = x
            node.y = y

    def edit_node(self, node_id: str, text: str):
        """Edit a node's text."""
        node = self.mind_map.get_node(node_id)
        if node:
            self._save_state()
            node.text = text

    def connect_nodes(self, source_id: str, target_id: str) -> Edge:
        """Create an edge between two nodes."""
        self._save_state()
        edge = Edge(source_id=source_id, target_id=target_id)
        self.mind_map.add_edge(edge)
        return edge

    def disconnect_nodes(self, source_id: str, target_id: str):
        """Remove edge between two nodes."""
        self._save_state()
        self.mind_map.edges = [
            e for e in self.mind_map.edges
            if not (e.source_id == source_id and e.target_id == target_id)
        ]

    def undo(self) -> bool:
        """Undo the last action."""
        if not self._undo_stack:
            return False
        self._redo_stack.append(self.mind_map.to_dict())
        state = self._undo_stack.pop()
        self.mind_map = MindMap.from_dict(state)
        return True

    def redo(self) -> bool:
        """Redo the last undone action."""
        if not self._redo_stack:
            return False
        self._undo_stack.append(self.mind_map.to_dict())
        state = self._redo_stack.pop()
        self.mind_map = MindMap.from_dict(state)
        return True

    def clear(self):
        """Clear the entire canvas."""
        self._save_state()
        self.mind_map = MindMap()

    def set_zoom(self, zoom: float):
        """Set canvas zoom level."""
        self._zoom = max(0.1, min(5.0, zoom))

    def pan(self, dx: float, dy: float):
        """Pan the canvas view."""
        self._pan_x += dx
        self._pan_y += dy

    @property
    def zoom(self) -> float:
        return self._zoom

    @property
    def pan_offset(self) -> tuple[float, float]:
        return (self._pan_x, self._pan_y)

    def get_state(self) -> dict:
        """Get current canvas state."""
        return {
            "mind_map": self.mind_map.to_dict(),
            "zoom": self._zoom,
            "pan": {"x": self._pan_x, "y": self._pan_y},
            "size": {"width": self.width, "height": self.height},
        }

    def _save_state(self):
        """Save current state for undo."""
        self._undo_stack.append(self.mind_map.to_dict())
        self._redo_stack.clear()
        if len(self._undo_stack) > 50:
            self._undo_stack.pop(0)
