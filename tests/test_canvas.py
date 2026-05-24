"""Tests for MindCanvas canvas and models."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mindcanvas import Canvas, Generator, AutoLayout, MindMap, Node, Edge
from mindcanvas.models import MindMap
from mindcanvas.exporter import Exporter


def test_create_node():
    """Test node creation."""
    n = Node(text="Hello", x=100, y=200)
    assert n.text == "Hello"
    assert n.x == 100


def test_create_edge():
    """Test edge creation."""
    e = Edge(source_id="a", target_id="b")
    assert e.source_id == "a"


def test_mindmap_operations():
    """Test mind map add/remove."""
    mm = MindMap()
    n1 = Node(text="A", node_type="center")
    n2 = Node(text="B")
    mm.add_node(n1)
    mm.add_node(n2)
    mm.add_edge(Edge(source_id=n1.id, target_id=n2.id))
    assert mm.node_count == 2
    assert mm.edge_count == 1
    mm.remove_node(n1.id)
    assert mm.node_count == 1
    assert mm.edge_count == 0


def test_canvas_add_node():
    """Test canvas node operations."""
    c = Canvas()
    n = c.add_node("Test", 100, 200)
    assert n.text == "Test"
    assert c.mind_map.node_count == 1


def test_canvas_undo():
    """Test canvas undo."""
    c = Canvas()
    c.add_node("A", 0, 0)
    c.add_node("B", 100, 100)
    assert c.mind_map.node_count == 2
    assert c.undo()
    assert c.mind_map.node_count == 1


def test_generator():
    """Test mind map generation."""
    gen = Generator()
    mm = gen.generate("AI startup ideas", depth=2)
    assert mm.node_count > 1
    assert mm.get_center() is not None


def test_auto_layout():
    """Test auto layout."""
    gen = Generator()
    mm = gen.generate("test topic", depth=2)
    al = AutoLayout()
    al.apply(mm)
    center = mm.get_center()
    assert center.x == 400


def test_export_json():
    """Test JSON export."""
    gen = Generator()
    mm = gen.generate("test", depth=1)
    exp = Exporter()
    json_str = exp.to_json(mm)
    assert '"title"' in json_str


def test_export_markdown():
    """Test markdown export."""
    gen = Generator()
    mm = gen.generate("test", depth=1)
    exp = Exporter()
    md = exp.to_markdown(mm)
    assert "# test" in md


def test_templates():
    """Test template loading."""
    gen = Generator()
    for tpl in ["startup", "project", "swot", "study"]:
        mm = gen.generate("", template=tpl)
        assert mm.node_count > 1


if __name__ == "__main__":
    tests = [
        test_create_node,
        test_create_edge,
        test_mindmap_operations,
        test_canvas_add_node,
        test_canvas_undo,
        test_generator,
        test_auto_layout,
        test_export_json,
        test_export_markdown,
        test_templates,
    ]
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
        except Exception as e:
            print(f"  ❌ {t.__name__}: {e}")
    print("\nAll tests complete!")
