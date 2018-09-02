import unittest
from channels.routing import ProtocolTypeRouter
from . import asgi


class AsgiTest(unittest.TestCase):
    def test_asgi(self):
        self.assertIsInstance(asgi.application, ProtocolTypeRouter)


if __name__ == '__main__':
    unittest.main()
