import numpy as np
from aos.sed import Blackbody, Monochromatic, Bandpass

def test_bandpass_static_methods():
    bp = Bandpass.u()
    Bandpass.g()
    Bandpass.r()
    Bandpass.i()
    Bandpass.z()
    Bandpass.y()

    assert np.all(bp.wavelengths <= bp.high)
    assert np.all(bp.wavelengths >= bp.low)

def test_monochromatic():
    mon = Monochromatic()
    wvs, spec = mon.spectrum()
    assert len(wvs) == 3
    assert len(spec) == 3

    assert np.all(mon.sample(100) == mon.wavelength)

def test_blackbody_init():
    Blackbody(wavelength=500e-9)
    bbd = Blackbody(temperature=6000)

    wvs, spec = bbd.spectrum()

    assert len(wvs) == len(spec)
    assert np.isclose(np.sum(spec), 1)

    wvs = bbd.sample(1e6)

    assert np.all(wvs <= bbd.bandpass.high)
    assert np.all(wvs >= bbd.bandpass.low)

    # wien's displacement law
    assert np.isclose(np.sum(bbd.spec[bbd.wavelengths < bbd.wavelength]), 0.5, atol=0.1)