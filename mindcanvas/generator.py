"""AI mind map generator.

Generates mind maps from topics using rule-based expansion
and optional AI integration.
"""

import math
import random
from typing import Optional
from .models import Node, Edge, MindMap
from .templates import TemplateLibrary


class Generator:
    """Generate mind maps from topics."""

    # Knowledge base for topic expansion
    KNOWLEDGE = {
        "startup": {
            "branches": ["Product", "Market", "Team", "Funding", "Growth", "Revenue"],
            "subs": {
                "Product": ["MVP", "Features", "Tech Stack"],
                "Market": ["Target Users", "Competition", "Market Size"],
                "Team": ["Founders", "Engineers", "Advisors"],
                "Funding": ["Bootstrapping", "Angel", "VC"],
                "Growth": ["Marketing", "Sales", "Partnerships"],
                "Revenue": ["SaaS", "Freemium", "Enterprise"],
            },
        },
        "project": {
            "branches": ["Scope", "Timeline", "Team", "Risks", "Tools", "Goals"],
            "subs": {
                "Scope": ["Requirements", "Deliverables", "Constraints"],
                "Timeline": ["Sprint 1", "Sprint 2", "Launch"],
                "Team": ["Dev", "Design", "QA"],
                "Risks": ["Technical", "Resource", "Schedule"],
                "Tools": ["Git", "CI/CD", "Monitoring"],
                "Goals": ["KPIs", "Metrics", "Review"],
            },
        },
        "ai": {
            "branches": ["Models", "Data", "Training", "Deployment", "Ethics", "Use Cases"],
            "subs": {
                "Models": ["LLM", "Vision", "Audio"],
                "Data": ["Collection", "Cleaning", "Augmentation"],
                "Training": ["Fine-tuning", "RLHF", "Evaluation"],
                "Deployment": ["API", "Edge", "Cloud"],
                "Ethics": ["Bias", "Privacy", "Safety"],
                "Use Cases": ["Chatbot", "Analytics", "Automation"],
            },
        },
        "study": {
            "branches": ["Fundamentals", "Core Theory", "Practice", "Advanced", "Resources", "Review"],
            "subs": {
                "Fundamentals": ["Concepts", "Definitions", "History"],
                "Core Theory": ["Principles", "Models", "Frameworks"],
                "Practice": ["Exercises", "Projects", "Labs"],
                "Advanced": ["Research", "Trends", "Case Studies"],
                "Resources": ["Books", "Videos", "Papers"],
                "Review": ["Summary", "Quiz", "Flashcards"],
            },
        },
    }

    def __init__(self):
        self.templates = TemplateLibrary()

    def generate(
        self,
        topic: str,
        depth: int = 3,
        max_branches: int = 6,
        max_subs: int = 3,
        template: Optional[str] = None,
    ) -> MindMap:
        """Generate a mind map from a topic.

        Args:
            topic: Central topic for the mind map
            depth: How many levels deep to generate
            max_branches: Maximum number of main branches
            max_subs: Maximum sub-branches per branch
            template: Optional template name to use

        Returns:
            Complete MindMap object
        """
        if template:
            return self.templates.load(template)

        mind_map = MindMap(title=topic)

        # Create center node
        center = Node(
            text=topic, x=400, y=300, node_type="center"
        )
        mind_map.add_node(center)

        # Find matching knowledge base
        branches, subs = self._find_knowledge(topic, max_branches)

        # Generate branches
        angle_step = (2 * math.pi) / max(len(branches), 1)
        radius = 200

        for i, branch_text in enumerate(branches[:max_branches]):
            angle = angle_step * i - math.pi / 2
            bx = center.x + radius * math.cos(angle)
            by = center.y + radius * math.sin(angle)

            branch = Node(text=branch_text, x=bx, y=by, node_type="branch")
            mind_map.add_node(branch)
            mind_map.add_edge(Edge(source_id=center.id, target_id=branch.id))

            # Generate sub-branches
            if depth >= 2:
                sub_texts = subs.get(branch_text, self._generic_subs(branch_text))
                sub_angle_step = 0.4
                sub_radius = 130

                for j, sub_text in enumerate(sub_texts[:max_subs]):
                    sub_angle = angle + (j - 1) * sub_angle_step
                    sx = bx + sub_radius * math.cos(sub_angle)
                    sy = by + sub_radius * math.sin(sub_angle)

                    sub = Node(text=sub_text, x=sx, y=sy, node_type="leaf")
                    mind_map.add_node(sub)
                    mind_map.add_edge(Edge(source_id=branch.id, target_id=sub.id))

        return mind_map

    def _find_knowledge(
        self, topic: str, max_branches: int
    ) -> tuple[list[str], dict[str, list[str]]]:
        """Find matching knowledge base for a topic."""
        topic_lower = topic.lower()
        for key, data in self.KNOWLEDGE.items():
            if key in topic_lower:
                return data["branches"], data["subs"]

        # Generic branches
        generic = [
            "Ideas", "Research", "Planning",
            "Execution", "Review", "Next Steps",
        ]
        return generic, {}

    def _generic_subs(self, branch_text: str) -> list[str]:
        """Generate generic sub-branch names."""
        return [f"{branch_text} - Detail 1", f"{branch_text} - Detail 2", f"{branch_text} - Detail 3"]

    def expand_node(
        self, mind_map: MindMap, node_id: str, count: int = 3
    ) -> list[Node]:
        """Add sub-branches to an existing node."""
        node = mind_map.get_node(node_id)
        if not node:
            return []

        new_nodes = []
        angle_step = 0.5
        base_angle = random.uniform(0, 2 * math.pi)
        radius = 130

        for i in range(count):
            angle = base_angle + (i - 1) * angle_step
            nx = node.x + radius * math.cos(angle)
            ny = node.y + radius * math.sin(angle)

            child = Node(
                text=f"{node.text} - Branch {i+1}",
                x=nx, y=ny, node_type="leaf"
            )
            mind_map.add_node(child)
            mind_map.add_edge(Edge(source_id=node.id, target_id=child.id))
            new_nodes.append(child)

        return new_nodes
