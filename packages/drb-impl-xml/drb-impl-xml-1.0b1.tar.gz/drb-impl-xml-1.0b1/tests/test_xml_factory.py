import unittest
import os
import tempfile
from io import BytesIO

from drb_impl_xml import XmlNodeFactory, XmlBaseNode
from drb_impl_file import DrbFileNode
from drb.utils.url_node import UrlNode


class TestXmlFactoryNode(unittest.TestCase):
    xml = """
    <fb:foobar xmlns:fb="https://foobar.org/foobar"
               xmlns:f="https://foobar.org/foo"
               xmlns:b="https://foobar.org/bar">
        <f:foo>3</f:foo>
        <b:bar>Hello</b:bar>
    </fb:foobar>
    """
    path = None
    invalid_path = None
    file_node = None

    @classmethod
    def setUpClass(cls) -> None:
        fd, cls.path = tempfile.mkstemp(suffix='.xml', text=True)
        with os.fdopen(fd, 'w') as file:
            file.write(cls.xml)
            file.flush()
        cls.file_node = DrbFileNode(cls.path)
        fd, cls.invalid_path = tempfile.mkstemp(suffix='.txt', text=True)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(cls.path)
        os.remove(cls.invalid_path)

    def test_create_from_node(self):
        factory = XmlNodeFactory()

        node = factory.create(self.file_node)
        self.assertIsNotNone(node)
        self.assertIsInstance(node, XmlBaseNode)
        node.close()

    def test_create_from_path(self):
        path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test.xml')

        node = XmlNodeFactory().create(path)

        self.assertIsNotNone(node)
        self.assertEqual(node.name, 'test.xml')
        self.assertEqual(len(node), 1)
        root = node[0]
        self.assertEqual(root.name, 'root')
        self.assertEqual(len(root), 3)

        node.close()

    def test_create_from_memory(self):
        content = b'<root><elem>1</elem><elem>2</elem><elem>3</elem></root>'

        class MemoryNode(UrlNode):
            def __init__(self, name: str):
                super(MemoryNode, self).__init__(name)

            def has_impl(self, impl: type) -> bool:
                if impl == BytesIO:
                    return True
                else:
                    return super(MemoryNode, self).has_impl(impl)

            def get_impl(self, impl: type):
                return BytesIO(content)

        node_name = 'memory_data'
        node = XmlNodeFactory().create(MemoryNode(node_name))

        self.assertIsNotNone(node)
        self.assertEqual(node.name, node_name)
        self.assertEqual(len(node), 1)
        root = node[0]
        self.assertEqual(root.name, 'root')
        self.assertEqual(len(root), 3)

        node.close()
