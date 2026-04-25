from raga.models import Raga, Tala, load_ragas, load_talas


def test_load_ragas_nonempty(ragas):
    assert len(ragas) > 0


def test_load_talas_nonempty(talas):
    assert len(talas) > 0


def test_ragas_are_raga_instances(ragas):
    assert all(isinstance(r, Raga) for r in ragas)


def test_talas_are_tala_instances(talas):
    assert all(isinstance(t, Tala) for t in talas)


def test_raga_required_fields(ragas):
    for r in ragas:
        assert r.name
        assert r.arohana
        assert r.avarohana
        assert r.vadi
        assert r.samvadi
        assert r.time


def test_load_ragas_is_cached():
    assert load_ragas() is load_ragas()


def test_load_talas_is_cached():
    assert load_talas() is load_talas()
