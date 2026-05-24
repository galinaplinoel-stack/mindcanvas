"""Pre-built mind map templates."""

from .models import Node, Edge, MindMap


class TemplateLibrary:
    """Library of pre-built mind map templates."""

    TEMPLATES = {
        "startup": {
            "title": "AI Startup Brainstorm",
            "center": "AI Startup",
            "branches": [
                {"text": "Product", "subs": ["MVP", "Features", "Tech Stack"]},
                {"text": "Market", "subs": ["Target Users", "Competition", "Size"]},
                {"text": "Team", "subs": ["Founders", "Engineers", "Advisors"]},
                {"text": "Funding", "subs": ["Bootstrapping", "Angel", "VC"]},
                {"text": "Growth", "subs": ["Marketing", "Sales", "Partnerships"]},
                {"text": "Revenue", "subs": ["SaaS", "Freemium", "Enterprise"]},
            ],
        },
        "project": {
            "title": "Project Planning",
            "center": "Project Plan",
            "branches": [
                {"text": "Scope", "subs": ["Requirements", "Deliverables", "Constraints"]},
                {"text": "Timeline", "subs": ["Sprint 1", "Sprint 2", "Launch"]},
                {"text": "Team", "subs": ["Dev", "Design", "QA"]},
                {"text": "Risks", "subs": ["Technical", "Resource", "Schedule"]},
                {"text": "Tools", "subs": ["Git", "CI/CD", "Monitoring"]},
                {"text": "Goals", "subs": ["KPIs", "Metrics", "Review"]},
            ],
        },
        "swot": {
            "title": "SWOT Analysis",
            "center": "SWOT",
            "branches": [
                {"text": "💪 Strengths", "subs": ["Advantage 1", "Advantage 2", "Advantage 3"]},
                {"text": "⚠️ Weaknesses", "subs": ["Gap 1", "Gap 2", "Gap 3"]},
                {"text": "🌟 Opportunities", "subs": ["Trend 1", "Trend 2", "Trend 3"]},
                {"text": "🔴 Threats", "subs": ["Risk 1", "Risk 2", "Risk 3"]},
            ],
        },
        "study": {
            "title": "Study Notes",
            "center": "Study Topic",
            "branches": [
                {"text": "Fundamentals", "subs": ["Concepts", "Definitions", "History"]},
                {"text": "Core Theory", "subs": ["Principles", "Models", "Frameworks"]},
                {"text": "Practice", "subs": ["Exercises", "Projects", "Labs"]},
                {"text": "Advanced", "subs": ["Research", "Trends", "Case Studies"]},
                {"text": "Resources", "subs": ["Books", "Videos", "Papers"]},
                {"text": "Review", "subs": ["Summary", "Quiz", "Flashcards"]},
            ],
        },
        "creative": {
            "title": "Creative Process",
            "center": "Creative Project",
            "branches": [
                {"text": "Inspiration", "subs": ["Mood Board", "References", "Art"]},
                {"text": "Research", "subs": ["Audience", "Trends", "Analysis"]},
                {"text": "Ideation", "subs": ["Brainstorm", "Sketch", "Prototype"]},
                {"text": "Execution", "subs": ["Design", "Build", "Polish"]},
                {"text": "Feedback", "subs": ["Testing", "Review", "Iteration"]},
                {"text": "Launch", "subs": ["Publish", "Promote", "Measure"]},
            ],
        },
        "decision": {
            "title": "Decision Matrix",
            "center": "Decision",
            "branches": [
                {"text": "Option A", "subs": ["Pros", "Cons", "Score"]},
                {"text": "Option B", "subs": ["Pros", "Cons", "Score"]},
                {"text": "Option C", "subs": ["Pros", "Cons", "Score"]},
                {"text": "Criteria", "subs": ["Cost", "Impact", "Risk"]},
                {"text": "Research", "subs": ["Data", "Opinions", "Examples"]},
                {"text": "Verdict", "subs": ["Best Choice", "Why", "Next Steps"]},
            ],
        },
    }

    def load(self, name: str) -> MindMap:
        """Load a template by name."""
        if name not in self.TEMPLATES:
            raise KeyError(f"Unknown template: {name}")

        tpl = self.TEMPLATES[name]
        mind_map = MindMap(title=tpl["title"])

        import math
        center = Node(text=tpl["center"], x=400, y=300, node_type="center")
        mind_map.add_node(center)

        angle_step = (2 * math.pi) / len(tpl["branches"])
        for i, branch_data in enumerate(tpl["branches"]):
            angle = angle_step * i - math.pi / 2
            bx = center.x + 200 * math.cos(angle)
            by = center.y + 200 * math.sin(angle)

            branch = Node(text=branch_data["text"], x=bx, y=by, node_type="branch")
            mind_map.add_node(branch)
            mind_map.add_edge(Edge(source_id=center.id, target_id=branch.id))

            for j, sub_text in enumerate(branch_data.get("subs", [])):
                sub_angle = angle + (j - 1) * 0.35
                sx = bx + 130 * math.cos(sub_angle)
                sy = by + 130 * math.sin(sub_angle)

                sub = Node(text=sub_text, x=sx, y=sy, node_type="leaf")
                mind_map.add_node(sub)
                mind_map.add_edge(Edge(source_id=branch.id, target_id=sub.id))

        return mind_map

    def list_templates(self) -> list[dict]:
        """List all available templates."""
        return [
            {"name": name, "title": data["title"]}
            for name, data in self.TEMPLATES.items()
        ]
