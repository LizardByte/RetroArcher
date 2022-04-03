"""test_definitions.py

unit tests for pyra.definitions.py
"""
# local imports
from pyra import definitions


def test_files():
    """Tests Files class"""
    files = definitions.Files()

    assert files.CONFIG


def test_names():
    """Tests Names class"""
    names = definitions.Names()

    assert names.name == 'RetroArcher'


def test_paths():
    """Tests Paths class"""
    paths = definitions.Paths()

    assert paths.PYRA_DIR
    assert paths.ROOT_DIR
    assert paths.DATA_DIR
    assert paths.LOCALE_DIR
    assert paths.LOG_DIR


def test_platform():
    """Tests Platform class"""
    platform = definitions.Platform()

    assert platform.bits == 64 or platform.bits == 32

    assert platform.operating_system
    assert platform.platform
    assert platform.processor
    assert platform.machine
    assert platform.node
    assert platform.release
    assert platform.version
    assert isinstance(platform.edition, (str, type(None)))
    assert isinstance(platform.iot, bool)
