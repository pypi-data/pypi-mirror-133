from jinja2 import Template
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Union

from md_citeproc.utils import Utilities
from md_citeproc.structures import NotationStyle, OutputStyle, CiteprocConfigDefaults


class TestHelpers:

    @staticmethod
    def get_fixture_dir() -> Path:
        p = Path(__file__).parent / "fixtures"
        if not p.is_dir():
            raise ValueError("Asset directory not found at {}".format(str(p)))
        return p

    @staticmethod
    def get_fixture_text(filename: str) -> str:
        fpath = TestHelpers.get_fixture_dir() / filename
        with fpath.open() as f:
            testdata = f.read()
        return testdata

    @staticmethod
    def get_fixture_list(filename: str) -> list[list[str]]:
        testdata = TestHelpers.get_fixture_text(filename)
        return [doc.splitlines(keepends=False) for doc in testdata.split("\n---\n")]

    @staticmethod
    def get_t_config(
            csljson: Optional[str],
            stylefile: Optional[str],
            notation: NotationStyle,
            output: OutputStyle,
            uncited: Optional[list] = None,
            strict: bool = False
    ):
        return {
            "csljson": None if csljson is None else TestHelpers.get_fixture_dir() / csljson,
            "cslfile": None if stylefile is None else TestHelpers.get_fixture_dir() / stylefile,
            "uncited": [] if uncited is None else uncited,
            "locale": "de-CH",
            "localedir": CiteprocConfigDefaults.BUILTIN,
            "notation": notation,
            "output": output,
            "num_template": Utilities.get_default_templates("num.html"),
            "footnote_template": Utilities.get_default_templates("footnote.html"),
            "inline_template": Utilities.get_default_templates("inline.html"),
            "footnotes_token": "[FOOTNOTES]",
            "bibliography_token": "[BIBLIOGRAPHY]",
            "citeproc_executable": CiteprocConfigDefaults.AVAILABLE,
            "strict": strict
        }
