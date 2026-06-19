import unittest


class FakeStream:
    def __init__(self) -> None:
        self.encoding = "cp936"

    def reconfigure(self, *, encoding: str) -> None:
        self.encoding = encoding


class CliIoTests(unittest.TestCase):
    def test_enable_utf8_reconfigures_supported_stream(self):
        from scripts.cli_io import _enable_utf8

        stream = FakeStream()
        _enable_utf8(stream)
        self.assertEqual(stream.encoding, "utf-8")

    def test_enable_utf8_ignores_streams_without_reconfigure(self):
        from scripts.cli_io import _enable_utf8

        # A stream that predates reconfigure() (or a plain object) must be a no-op,
        # not an error.
        _enable_utf8(object())

    def test_enable_utf8_swallows_reconfigure_failures(self):
        from scripts.cli_io import _enable_utf8

        class Detached:
            def reconfigure(self, *, encoding: str) -> None:
                raise ValueError("underlying buffer has been detached")

        _enable_utf8(Detached())

    def test_enable_utf8_output_is_safe_to_call(self):
        from scripts.cli_io import enable_utf8_output

        enable_utf8_output()


if __name__ == "__main__":
    unittest.main()
