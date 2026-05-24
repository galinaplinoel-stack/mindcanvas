"""Auto-layout algorithms for MindCanvas.

Provides multiple layout strategies: radial, tree, and force-directed.
"""

import math
from typing import Optional
from .models import MindMap


class AutoLayout:
    """Automatic layout engine for mind maps."""

    def __init__(self, algorithm: str = "radial", spacing: float = 200):
        self.algorithm = algorithm
        self.spacing = spacing

    def apply(self, mind_map: MindMap, algorithm: Optional[str] = None):
        """Apply layout algorithm to a mind map.

        Args:
            mind_map: The mind map to layout
            algorithm: Override default algorithm
        """
        algo = algorithm or self.algorithm
        if algo == "radial":
            self._radial_layout(mind_map)
        elif algo == "tree":
            self._tree_layout(mind_map)
        elif algo == "force":
            self._force_layout(mind_map)
        else:
            raise ValueError(f"Unknown algorithm: {algo}")

    def _radial_layout(self, mind_map: MindMap):
        """Radial layout — branches radiate from center."""
        center = mind_map.get_center()
        if not center:
            return

        center.x = 400
        center.y = 300

        branches = mind_map.get_children(center.id)
        if not branches:
            return

        angle_step = (2 * math.pi) / len(branches)
        for i, branch in enumerate(branches):
            angle = angle_step * i - math.pi / 2
            branch.x = center.x + self.spacing * math.cos(angle)
            branch.y = center.y + self.spacing * math.sin(angle)

            # Layout children of this branch
            children = mind_map.get_children(branch.id)
            if children:
                sub_angle_step = 0.4
                sub_radius = self.spacing * 0.65
                for j, child in enumerate(children):
                    sub_angle = angle + (j - len(children) / 2) * sub_angle_step
                    child.x = branch.x + sub_radius * math.cos(sub_angle)
                    child.y = branch.y + sub_radius * math.sin(sub_angle)

    def _tree_layout(self, mind_map: MindMap):
        """Tree layout — top-down hierarchical structure."""
        center = mind_map.get_center()
        if not center:
            return

        center.x = 400
        center.y = 80

        branches = mind_map.get_children(center.id)
        total_width = max(len(branches) * self.spacing, 800)
        start_x = center.x - total_width / 2

        for i, branch in enumerate(branches):
            branch.x = start_x + (i + 0.5) * (total_width / len(branches))
            branch.y = center.y + self.spacing

            children = mind_map.get_children(branch.id)
            if children:
                child_width = self.spacing * 0.8
                child_start = branch.x - (len(children) - 1) * child_width / 2
                for j, child in enumerate(children):
                    child.x = child_start + j * child_width
                    child.y = branch.y + self.spacing * 0.8

    def _force_layout(self, mind_map: MindMap):
        """Simple force-directed layout simulation."""
        # Initialize positions randomly if not set
        for node in mind_map.nodes:
            if node.x == 0 and node.y == 0:
                node.x = 400 + (hash(node.id) % 200 - 100)
                node.y = 300 + (hash(node.id) % 200 - 100)

        # Simple force simulation (10 iterations)
        for _ in range(10):
            for i, n1 in enumerate(mind_map.nodes):
                for j, n2 in enumerate(mind_map.nodes):
                    if i >= j:
                        continue
                    dx = n2.x - n1.x
                    dy = n2.y - n1.y
                    dist = max(math.sqrt(dx * dx + dy * dy), 1)

                    # Repulsion
                    if dist < self.spacing:
                        force = (self.spacing - dist) / dist * 0.5
                        n1.x -= dx * force
                        n1.y -= dy * force
                        n2.x += dx * force
                        n2.y += dy * force

            # Attraction along edges
            for edge in mind_map.edges:
                src = mind_map.get_node(edge.source_id)
                tgt = mind_map.get_node(edge.target_id)
                if not src or not tgt:
                    continue
                dx = tgt.x - src.x
                dy = tgt.y - src.y
                dist = max(math.sqrt(dx * dx + dy * dy), 1)
                ideal = self.spacing * 0.7
                if dist > ideal:
                    force = (dist - ideal) / dist * 0.1
                    src.x += dx * force
                    src.y += dy * force
                    tgt.x -= dx * force
                    tgt.y -= dy * force
