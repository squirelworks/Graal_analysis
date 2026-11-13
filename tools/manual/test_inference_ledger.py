import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location(
    "inference_ledger", pathlib.Path(__file__).with_name("inference_ledger.py"))
il = importlib.util.module_from_spec(spec)
spec.loader.exec_module(il)


def test_inf_only_counts():
    assert "inf" in il.tags("[inf] (a/b.md)")
    t = il.tags("[bin][inf] (a/b.md)")
    assert t == {"bin", "inf"}


def test_ledger_is_current():
    assert il.OUT.read_text(encoding="utf-8") == il.render()
