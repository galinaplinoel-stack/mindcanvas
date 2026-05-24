"""Export mind maps to various formats."""

import json
from pathlib import Path
from typing import Optional
from .models import MindMap


class Exporter:
    """Export mind maps to JSON, SVG, and other formats."""

    def to_json(self, mind_map: MindMap, path: Optional[str] = None) -> str:
        """Export as JSON string or file."""
        data = mind_map.to_json()
        if path:
            Path(path).write_text(data)
        return data

    def to_dict(self, mind_map: MindMap) -> dict:
        """Export as Python dictionary."""
        return mind_map.to_dict()

    def to_svg(self, mind_map: MindMap, width: int = 1000, height: int = 800) -> str:
        """Export as SVG string."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}">'
        ]

        # Draw edges
        for edge in mind_map.edges:
            src = mind_map.get_node(edge.source_id)
            tgt = mind_map.get_node(edge.target_id)
            if src and tgt:
                svg_parts.append(
                    f'<line x1="{src.x}" y1="{src.y}" '
                    f'x2="{tgt.x}" y2="{tgt.y}" '
                    f'stroke="#f97316" stroke-width="2" opacity="0.5"/>'
                )

        # Draw nodes
        for node in mind_map.nodes:
            if node.node_type == "center":
                fill = "#f97316"
                text_color = "white"
                rx = 16
            elif node.node_type == "branch":
                fill = "#1a1a25"
                text_color = "white"
                rx = 12
            else:
                fill = "#1a1a25"
                text_color = "#64748b"
                rx = 8

            svg_parts.append(
                f'<rect x="{node.x - 60}" y="{node.y - 20}" '
                f'width="120" height="40" rx="{rx}" '
                f'fill="{fill}" stroke="#f97316" stroke-width="1"/>'
            )
            svg_parts.append(
                f'<text x="{node.x}" y="{node.y + 5}" '
                f'text-anchor="middle" fill="{text_color}" '
                f'font-size="12" font-family="sans-serif">'
                f'{node.text}</text>'
            )

        svg_parts.append("</svg>")
        return "\n".join(svg_parts)

    def to_markdown(self, mind_map: MindMap) -> str:
        """Export as indented markdown list."""
        lines = [f"# {mind_map.title}", ""]
        center = mind_map.get_center()
        if not center:
            return "\n".join(lines)

        lines.append(f"- **{center.text}**")
        for branch in mind_map.get_children(center.id):
            lines.append(f"  - {branch.text}")
            for leaf in mind_map.get_children(branch.id):
                lines.append(f"    - {leaf.text}")

        return "\n".join(lines)
