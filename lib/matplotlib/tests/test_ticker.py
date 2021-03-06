from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

from numpy.testing import assert_almost_equal
import numpy as np
import pytest

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.testing.decorators import cleanup

import warnings


@cleanup(style='classic')
def test_MaxNLocator():
    loc = mticker.MaxNLocator(nbins=5)
    test_value = np.array([20., 40., 60., 80., 100.])
    assert_almost_equal(loc.tick_values(20, 100), test_value)

    test_value = np.array([0., 0.0002, 0.0004, 0.0006, 0.0008, 0.001])
    assert_almost_equal(loc.tick_values(0.001, 0.0001), test_value)

    test_value = np.array([-1.0e+15, -5.0e+14, 0e+00, 5e+14, 1.0e+15])
    assert_almost_equal(loc.tick_values(-1e15, 1e15), test_value)


@cleanup
def test_MaxNLocator_integer():
    loc = mticker.MaxNLocator(nbins=5, integer=True)
    test_value = np.array([-1, 0, 1, 2])
    assert_almost_equal(loc.tick_values(-0.1, 1.1), test_value)

    test_value = np.array([-0.25, 0, 0.25, 0.5, 0.75, 1])
    assert_almost_equal(loc.tick_values(-0.1, 0.95), test_value)


def test_LinearLocator():
    loc = mticker.LinearLocator(numticks=3)
    test_value = np.array([-0.8, -0.3, 0.2])
    assert_almost_equal(loc.tick_values(-0.8, 0.2), test_value)


def test_MultipleLocator():
    loc = mticker.MultipleLocator(base=3.147)
    test_value = np.array([-9.441, -6.294, -3.147, 0., 3.147, 6.294,
                           9.441, 12.588])
    assert_almost_equal(loc.tick_values(-7, 10), test_value)


@cleanup
def test_AutoMinorLocator():
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1.39)
    ax.minorticks_on()
    test_value = np.array([0.05, 0.1, 0.15, 0.25, 0.3, 0.35, 0.45,
                           0.5, 0.55, 0.65, 0.7, 0.75, 0.85, 0.9,
                           0.95, 1, 1.05, 1.1, 1.15, 1.25, 1.3, 1.35])
    assert_almost_equal(ax.xaxis.get_ticklocs(minor=True), test_value)


def test_LogLocator():
    loc = mticker.LogLocator(numticks=5)
    with pytest.raises(ValueError):
        loc.tick_values(0, 1000)

    test_value = np.array([1.00000000e-05, 1.00000000e-03, 1.00000000e-01,
                           1.00000000e+01, 1.00000000e+03, 1.00000000e+05,
                           1.00000000e+07, 1.000000000e+09])
    assert_almost_equal(loc.tick_values(0.001, 1.1e5), test_value)

    loc = mticker.LogLocator(base=2)
    test_value = np.array([0.5, 1., 2., 4., 8., 16., 32., 64., 128., 256.])
    assert_almost_equal(loc.tick_values(1, 100), test_value)


def test_LinearLocator_set_params():
    """
    Create linear locator with presets={}, numticks=2 and change it to
    something else. See if change was successful. Should not exception.
    """
    loc = mticker.LinearLocator(numticks=2)
    loc.set_params(numticks=8, presets={(0, 1): []})
    assert loc.numticks == 8
    assert loc.presets == {(0, 1): []}


def test_LogLocator_set_params():
    """
    Create log locator with default value, base=10.0, subs=[1.0], numdecs=4,
    numticks=15 and change it to something else.
    See if change was successful.
    Should not exception.
    """
    loc = mticker.LogLocator()
    loc.set_params(numticks=7, numdecs=8, subs=[2.0], base=4)
    assert loc.numticks == 7
    assert loc.numdecs == 8
    assert loc._base == 4
    assert list(loc._subs) == [2.0]


def test_NullLocator_set_params():
    """
    Create null locator, and attempt to call set_params() on it.
    Should not exception, and should raise a warning.
    """
    loc = mticker.NullLocator()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        loc.set_params()
        assert len(w) == 1


def test_MultipleLocator_set_params():
    """
    Create multiple locator with 0.7 base, and change it to something else.
    See if change was successful.
    Should not exception.
    """
    mult = mticker.MultipleLocator(base=0.7)
    mult.set_params(base=1.7)
    assert mult._base == 1.7


def test_LogitLocator_set_params():
    """
    Create logit locator with default minor=False, and change it to something
    else. See if change was successful. Should not exception.
    """
    loc = mticker.LogitLocator()  # Defaults to false.
    loc.set_params(minor=True)
    assert loc.minor


def test_FixedLocator_set_params():
    """
    Create fixed locator with 5 nbins, and change it to something else.
    See if change was successful.
    Should not exception.
    """
    fixed = mticker.FixedLocator(range(0, 24), nbins=5)
    fixed.set_params(nbins=7)
    assert fixed.nbins == 7


def test_IndexLocator_set_params():
    """
    Create index locator with 3 base, 4 offset. and change it to something
    else. See if change was successful.
    Should not exception.
    """
    index = mticker.IndexLocator(base=3, offset=4)
    index.set_params(base=7, offset=7)
    assert index._base == 7
    assert index.offset == 7


def test_SymmetricalLogLocator_set_params():
    """
    Create symmetrical log locator with default subs =[1.0] numticks = 15,
    and change it to something else.
    See if change was successful.
    Should not exception.
    """
    # since we only test for the params change. I will pass empty transform
    sym = mticker.SymmetricalLogLocator(None)
    sym.set_params(subs=[2.0], numticks=8)
    assert sym._subs == [2.0]
    assert sym.numticks == 8


@cleanup
@pytest.mark.parametrize('left, right, offset',
                         [(123, 189, 0),
                          (-189, -123, 0),
                          (12341, 12349, 12340),
                          (-12349, -12341, -12340),
                          (99999.5, 100010.5, 100000),
                          (-100010.5, -99999.5, -100000),
                          (99990.5, 100000.5, 100000),
                          (-100000.5, -99990.5, -100000),
                          (1233999, 1234001, 1234000),
                          (-1234001, -1233999, -1234000),
                          (1, 1, 1),
                          (123, 123, 120),
                          # Test cases courtesy of @WeatherGod
                          (.4538, .4578, .45),
                          (3789.12, 3783.1, 3780),
                          (45124.3, 45831.75, 45000),
                          (0.000721, 0.0007243, 0.00072),
                          (12592.82, 12591.43, 12590),
                          (9., 12., 0),
                          (900., 1200., 0),
                          (1900., 1200., 0),
                          (0.99, 1.01, 1),
                          (9.99, 10.01, 10),
                          (99.99, 100.01, 100),
                          (5.99, 6.01, 6),
                          (15.99, 16.01, 16),
                          (-0.452, 0.492, 0),
                          (-0.492, 0.492, 0),
                          (12331.4, 12350.5, 12300),
                          (-12335.3, 12335.3, 0)])
def test_ScalarFormatter_offset_value(left, right, offset):
    fig, ax = plt.subplots()
    formatter = ax.get_xaxis().get_major_formatter()

    ax.set_xlim(left, right)
    # Update ticks.
    next(ax.get_xaxis().iter_ticks())
    assert formatter.offset == offset

    ax.set_xlim(right, left)
    # Update ticks.
    next(ax.get_xaxis().iter_ticks())
    assert formatter.offset == offset


def _sub_labels(axis, subs=()):
    "Test whether locator marks subs to be labeled"
    fmt = axis.get_minor_formatter()
    minor_tlocs = axis.get_minorticklocs()
    fmt.set_locs(minor_tlocs)
    coefs = minor_tlocs / 10**(np.floor(np.log10(minor_tlocs)))
    label_expected = [np.round(c) in subs for c in coefs]
    label_test = [fmt(x) != '' for x in minor_tlocs]
    assert label_test == label_expected


@cleanup
def test_LogFormatter_sublabel():
    # test label locator
    fig, ax = plt.subplots()
    ax.set_xscale('log')
    ax.xaxis.set_major_locator(mticker.LogLocator(base=10, subs=[]))
    ax.xaxis.set_minor_locator(mticker.LogLocator(base=10,
                                                  subs=np.arange(2, 10)))
    ax.xaxis.set_major_formatter(mticker.LogFormatter())
    ax.xaxis.set_minor_formatter(mticker.LogFormatter(labelOnlyBase=False))
    # axis range above 3 decades, only bases are labeled
    ax.set_xlim(1, 1e4)
    fmt = ax.xaxis.get_major_formatter()
    fmt.set_locs(ax.xaxis.get_majorticklocs())
    show_major_labels = [fmt(x) != '' for x in ax.xaxis.get_majorticklocs()]
    assert np.all(show_major_labels)
    _sub_labels(ax.xaxis, subs=[])

    # axis range at 2 to 3 decades, label sub 3
    ax.set_xlim(1, 800)
    _sub_labels(ax.xaxis, subs=[3])

    # axis range at 1 to 2 decades, label subs 2 and 5
    ax.set_xlim(1, 80)
    _sub_labels(ax.xaxis, subs=[2, 5])

    # axis range at 0 to 1 decades, label subs 2, 3, 6
    ax.set_xlim(1, 8)
    _sub_labels(ax.xaxis, subs=[2, 3, 6])


class FakeAxis(object):
    """Allow Formatter to be called without having a "full" plot set up."""
    def __init__(self, vmin=1, vmax=10):
        self.vmin = vmin
        self.vmax = vmax

    def get_view_interval(self):
        return self.vmin, self.vmax


@pytest.mark.parametrize(
    'labelOnlyBase, exponent, locs, positions, expected',
    [
        (True, 4, np.arange(-3, 4.0), np.arange(-3, 4.0),
         ['-3', '-2', '-1', '0', '1', '2', '3']),
        # With labelOnlyBase=False, non-integer powers should be nicely
        # formatted.
        (False, 10, np.array([0.1, 0.00001, np.pi, 0.2, -0.2, -0.00001]),
         range(6), ['0.1', '1e-05', '3.14', '0.2', '-0.2', '-1e-05']),
        (False, 50, np.array([3, 5, 12, 42], dtype='float'), range(6),
         ['3', '5', '12', '42']),
    ])
@pytest.mark.parametrize('base', [2.0, 5.0, 10.0, np.pi, np.e])
def test_LogFormatterExponent(labelOnlyBase, base, exponent,
                              locs, positions, expected):
    formatter = mticker.LogFormatterExponent(base=base,
                                             labelOnlyBase=labelOnlyBase)
    formatter.axis = FakeAxis(1, base**exponent)
    vals = base**locs
    labels = [formatter(x, pos) for (x, pos) in zip(vals, positions)]
    assert labels == expected


def test_LogFormatterExponent_blank():
    # Should be a blank string for non-integer powers if labelOnlyBase=True
    formatter = mticker.LogFormatterExponent(base=10, labelOnlyBase=True)
    formatter.axis = FakeAxis()
    assert formatter(10**0.1) == ''


def test_LogFormatterSciNotation():
    test_cases = {
        10: (
             (1e-05, '${10^{-5}}$'),
             (1, '${10^{0}}$'),
             (100000, '${10^{5}}$'),
             (2e-05, '${2\\times10^{-5}}$'),
             (2, '${2\\times10^{0}}$'),
             (200000, '${2\\times10^{5}}$'),
             (5e-05, '${5\\times10^{-5}}$'),
             (5, '${5\\times10^{0}}$'),
             (500000, '${5\\times10^{5}}$'),
        ),
        2: (
            (0.03125, '${2^{-5}}$'),
            (1, '${2^{0}}$'),
            (32, '${2^{5}}$'),
            (0.0375, '${1.2\\times2^{-5}}$'),
            (1.2, '${1.2\\times2^{0}}$'),
            (38.4, '${1.2\\times2^{5}}$'),
        )
    }

    for base in test_cases.keys():
        formatter = mticker.LogFormatterSciNotation(base=base)
        formatter.sublabel = set([1, 2, 5, 1.2])
        for value, expected in test_cases[base]:
            with matplotlib.rc_context({'text.usetex': False}):
                assert formatter(value) == expected


@pytest.mark.parametrize('value, domain, expected', [
        (3.141592654e-05, 0.001, '3.142e-5'),
        (0.0003141592654, 0.001, '3.142e-4'),
        (0.003141592654, 0.001, '3.142e-3'),
        (0.03141592654, 0.001, '3.142e-2'),
        (0.3141592654, 0.001, '3.142e-1'),
        (3.141592654, 0.001, '3.142'),
        (31.41592654, 0.001, '3.142e1'),
        (314.1592654, 0.001, '3.142e2'),
        (3141.592654, 0.001, '3.142e3'),
        (31415.92654, 0.001, '3.142e4'),
        (314159.2654, 0.001, '3.142e5'),
        (1e-05, 0.001, '1e-5'),
        (0.0001, 0.001, '1e-4'),
        (0.001, 0.001, '1e-3'),
        (0.01, 0.001, '1e-2'),
        (0.1, 0.001, '1e-1'),
        (1, 0.001, '1'),
        (10, 0.001, '10'),
        (100, 0.001, '100'),
        (1000, 0.001, '1000'),
        (10000, 0.001, '1e4'),
        (100000, 0.001, '1e5'),
        (3.141592654e-05, 0.015, '0'),
        (0.0003141592654, 0.015, '0'),
        (0.003141592654, 0.015, '0.003'),
        (0.03141592654, 0.015, '0.031'),
        (0.3141592654, 0.015, '0.314'),
        (3.141592654, 0.015, '3.142'),
        (31.41592654, 0.015, '31.416'),
        (314.1592654, 0.015, '314.159'),
        (3141.592654, 0.015, '3141.593'),
        (31415.92654, 0.015, '31415.927'),
        (314159.2654, 0.015, '314159.265'),
        (1e-05, 0.015, '0'),
        (0.0001, 0.015, '0'),
        (0.001, 0.015, '0.001'),
        (0.01, 0.015, '0.01'),
        (0.1, 0.015, '0.1'),
        (1, 0.015, '1'),
        (10, 0.015, '10'),
        (100, 0.015, '100'),
        (1000, 0.015, '1000'),
        (10000, 0.015, '10000'),
        (100000, 0.015, '100000'),
        (3.141592654e-05, 0.5, '0'),
        (0.0003141592654, 0.5, '0'),
        (0.003141592654, 0.5, '0.003'),
        (0.03141592654, 0.5, '0.031'),
        (0.3141592654, 0.5, '0.314'),
        (3.141592654, 0.5, '3.142'),
        (31.41592654, 0.5, '31.416'),
        (314.1592654, 0.5, '314.159'),
        (3141.592654, 0.5, '3141.593'),
        (31415.92654, 0.5, '31415.927'),
        (314159.2654, 0.5, '314159.265'),
        (1e-05, 0.5, '0'),
        (0.0001, 0.5, '0'),
        (0.001, 0.5, '0.001'),
        (0.01, 0.5, '0.01'),
        (0.1, 0.5, '0.1'),
        (1, 0.5, '1'),
        (10, 0.5, '10'),
        (100, 0.5, '100'),
        (1000, 0.5, '1000'),
        (10000, 0.5, '10000'),
        (100000, 0.5, '100000'),
        (3.141592654e-05, 5, '0'),
        (0.0003141592654, 5, '0'),
        (0.003141592654, 5, '0'),
        (0.03141592654, 5, '0.03'),
        (0.3141592654, 5, '0.31'),
        (3.141592654, 5, '3.14'),
        (31.41592654, 5, '31.42'),
        (314.1592654, 5, '314.16'),
        (3141.592654, 5, '3141.59'),
        (31415.92654, 5, '31415.93'),
        (314159.2654, 5, '314159.27'),
        (1e-05, 5, '0'),
        (0.0001, 5, '0'),
        (0.001, 5, '0'),
        (0.01, 5, '0.01'),
        (0.1, 5, '0.1'),
        (1, 5, '1'),
        (10, 5, '10'),
        (100, 5, '100'),
        (1000, 5, '1000'),
        (10000, 5, '10000'),
        (100000, 5, '100000'),
        (3.141592654e-05, 100, '0'),
        (0.0003141592654, 100, '0'),
        (0.003141592654, 100, '0'),
        (0.03141592654, 100, '0'),
        (0.3141592654, 100, '0.3'),
        (3.141592654, 100, '3.1'),
        (31.41592654, 100, '31.4'),
        (314.1592654, 100, '314.2'),
        (3141.592654, 100, '3141.6'),
        (31415.92654, 100, '31415.9'),
        (314159.2654, 100, '314159.3'),
        (1e-05, 100, '0'),
        (0.0001, 100, '0'),
        (0.001, 100, '0'),
        (0.01, 100, '0'),
        (0.1, 100, '0.1'),
        (1, 100, '1'),
        (10, 100, '10'),
        (100, 100, '100'),
        (1000, 100, '1000'),
        (10000, 100, '10000'),
        (100000, 100, '100000'),
        (3.141592654e-05, 1000000.0, '3.1e-5'),
        (0.0003141592654, 1000000.0, '3.1e-4'),
        (0.003141592654, 1000000.0, '3.1e-3'),
        (0.03141592654, 1000000.0, '3.1e-2'),
        (0.3141592654, 1000000.0, '3.1e-1'),
        (3.141592654, 1000000.0, '3.1'),
        (31.41592654, 1000000.0, '3.1e1'),
        (314.1592654, 1000000.0, '3.1e2'),
        (3141.592654, 1000000.0, '3.1e3'),
        (31415.92654, 1000000.0, '3.1e4'),
        (314159.2654, 1000000.0, '3.1e5'),
        (1e-05, 1000000.0, '1e-5'),
        (0.0001, 1000000.0, '1e-4'),
        (0.001, 1000000.0, '1e-3'),
        (0.01, 1000000.0, '1e-2'),
        (0.1, 1000000.0, '1e-1'),
        (1, 1000000.0, '1'),
        (10, 1000000.0, '10'),
        (100, 1000000.0, '100'),
        (1000, 1000000.0, '1000'),
        (10000, 1000000.0, '1e4'),
        (100000, 1000000.0, '1e5')
])
def test_logformatter_pprint(value, domain, expected):
    fmt = mticker.LogFormatter()
    label = fmt.pprint_val(value, domain)
    assert label == expected


def test_use_offset():
    for use_offset in [True, False]:
        with matplotlib.rc_context({'axes.formatter.useoffset': use_offset}):
            tmp_form = mticker.ScalarFormatter()
            assert use_offset == tmp_form.get_useOffset()


def test_formatstrformatter():
    # test % style formatter
    tmp_form = mticker.FormatStrFormatter('%05d')
    assert '00002' == tmp_form(2)

    # test str.format() style formatter
    tmp_form = mticker.StrMethodFormatter('{x:05d}')
    assert '00002' == tmp_form(2)


percentformatter_test_cases = (
    # Check explicitly set decimals over different intervals and values
    (100, 0, '%', 120, 100, '120%'),
    (100, 0, '%', 100, 90, '100%'),
    (100, 0, '%', 90, 50, '90%'),
    (100, 0, '%', 1.7, 40, '2%'),
    (100, 1, '%', 90.0, 100, '90.0%'),
    (100, 1, '%', 80.1, 90, '80.1%'),
    (100, 1, '%', 70.23, 50, '70.2%'),
    # 60.554 instead of 60.55: see https://bugs.python.org/issue5118
    (100, 1, '%', 60.554, 40, '60.6%'),
    # Check auto decimals over different intervals and values
    (100, None, '%', 95, 1, '95.00%'),
    (1.0, None, '%', 3, 6, '300%'),
    (17.0, None, '%', 1, 8.5, '6%'),
    (17.0, None, '%', 1, 8.4, '5.9%'),
    (5, None, '%', -100, 0.000001, '-2000.00000%'),
    # Check percent symbol
    (1.0, 2, None, 1.2, 100, '120.00'),
    (75, 3, '', 50, 100, '66.667'),
    (42, None, '^^Foobar$$', 21, 12, '50.0^^Foobar$$'),
)


@pytest.mark.parametrize('xmax, decimals, symbol, x, display_range, expected',
                         percentformatter_test_cases)
def test_percentformatter(xmax, decimals, symbol, x, display_range, expected):
    formatter = mticker.PercentFormatter(xmax, decimals, symbol)
    assert formatter.format_pct(x, display_range) == expected

    # test str.format() style formatter with `pos`
    tmp_form = mticker.StrMethodFormatter('{x:03d}-{pos:02d}')
    assert '002-01' == tmp_form(2, 1)


def test_EngFormatter_formatting():
    """
    Create two instances of EngFormatter with default parameters, with and
    without a unit string ('s' for seconds). Test the formatting in some cases,
    especially the case when no SI prefix is present, for values in [1, 1000).

    Should not raise exceptions.
    """
    unitless = mticker.EngFormatter()
    assert unitless(0.1) == u'100 m'
    assert unitless(1) == u'1'
    assert unitless(999.9) == u'999.9'
    assert unitless(1001) == u'1.001 k'

    with_unit = mticker.EngFormatter(unit=u's')
    assert with_unit(0.1) == u'100 ms'
    assert with_unit(1) == u'1 s'
    assert with_unit(999.9) == u'999.9 s'
    assert with_unit(1001) == u'1.001 ks'
