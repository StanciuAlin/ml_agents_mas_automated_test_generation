# from units import u
from nddata import NDData, StdDevUncertainty, VarianceUncertainty, InverseVariance
import pytest
import sys
import os
sys.path.append(
    '/Users/alinstanciu/ml_agents_project/evaluation/input_python_code')


def test_nduncertainty_init():
    array = np.array([1, 2, 3])
    uncertainty = StdDevUncertainty(array)
    assert np.array_equal(uncertainty.array, array)


def test_nduncertainty_unit():
    array = np.array([1, 2, 3])
    uncertainty = StdDevUncertainty(array, unit=u.m)
    assert uncertainty.unit == u.m


def test_nduncertainty_copy():
    array = np.array([1, 2, 3])
    uncertainty = StdDevUncertainty(array, copy=False)
    array[0] = 10
    assert uncertainty.array[0] == 1


def test_nduncertainty_parent_nddata():
    ndd = NDData([1, 2, 3], unit='m',
                 uncertainty=StdDevUncertainty([0.1, 0.1, 0.1]))
    uncertainty = ndd.uncertainty
    assert uncertainty.parent_nddata is not None


def test_stddevuncertainty_propagate_add():
    ndd1 = NDData([1, 2, 3], unit='m',
                  uncertainty=StdDevUncertainty([0.1, 0.1, 0.1]))
    ndd2 = NDData([4, 5, 6], unit='m',
                  uncertainty=StdDevUncertainty([0.2, 0.2, 0.2]))
    result = ndd1 + ndd2
    assert np.array_equal(result.data, [5, 7, 9])
    assert isinstance(result.uncertainty, StdDevUncertainty)
    assert np.array_equal(result.uncertainty.array, [
                          0.14142136, 0.14142136, 0.14142136])


def test_stddevuncertainty_propagate_subtract():
    ndd1 = NDData([4, 5, 6], unit='m',
                  uncertainty=StdDevUncertainty([0.2, 0.2, 0.2]))
    ndd2 = NDData([1, 2, 3], unit='m',
                  uncertainty=StdDevUncertainty([0.1, 0.1, 0.1]))
    result = ndd1 - ndd2
    assert np.array_equal(result.data, [3, 3, 3])
    assert isinstance(result.uncertainty, StdDevUncertainty)
    assert np.array_equal(result.uncertainty.array, [
                          0.14142136, 0.14142136, 0.14142136])


def test_stddevuncertainty_propagate_multiply():
    ndd1 = NDData([2, 4, 6], unit='m',
                  uncertainty=StdDevUncertainty([0.1, 0.2, 0.3]))
    ndd2 = NDData([3, 6, 9], unit='m',
                  uncertainty=StdDevUncertainty([0.2, 0.4, 0.6]))
    result = ndd1 * ndd2
    assert np.array_equal(result.data, [6, 24, 54])
    assert isinstance(result.uncertainty, StdDevUncertainty)
    assert np.array_equal(result.uncertainty.array, [0.12, 0.96, 3.24])


def test_stddevuncertainty_propagate_divide():
    ndd1 = NDData([6, 24, 54], unit='m',
                  uncertainty=StdDevUncertainty([0.3, 1.2, 3.6]))
    ndd2 = NDData([2, 4, 6], unit='m',
                  uncertainty=StdDevUncertainty([0.1, 0.2, 0.3]))
    result = ndd1 / ndd2
    assert np.array_equal(result.data, [3, 6, 9])
    assert isinstance(result.uncertainty, StdDevUncertainty)
    assert np.array_equal(result.uncertainty.array, [0.12, 0.96, 3.24])


def test_varianceuncertainty_propagate_add():
    ndd1 = NDData([1, 2, 3], unit='m',
                  uncertainty=VarianceUncertainty([0.01, 0.04, 0.09]))
    ndd2 = NDData([4, 5, 6], unit='m',
                  uncertainty=VarianceUncertainty([0.16, 0.25, 0.36]))
    result = ndd1 + ndd2
    assert np.array_equal(result.data, [5, 7, 9])
    assert isinstance(result.uncertainty, VarianceUncertainty)
    assert np.array_equal(result.uncertainty.array, [0.17, 0.29, 0.45])


def test_varianceuncertainty_propagate_subtract():
    ndd1 = NDData([4, 5, 6], unit='m',
                  uncertainty=VarianceUncertainty([0.16, 0.25, 0.36]))
    ndd2 = NDData([1, 2, 3], unit='m',
                  uncertainty=VarianceUncertainty([0.01, 0.04, 0.09]))
    result = ndd1 - ndd2
    assert np.array_equal(result.data, [3, 3, 3])
    assert isinstance(result.uncertainty, VarianceUncertainty)
    assert np.array_equal(result.uncertainty.array, [0.17, 0.29, 0.45])


def test_varianceuncertainty_propagate_multiply():
    ndd1 = NDData([2, 4, 6], unit='m',
                  uncertainty=VarianceUncertainty([0.01, 0.04, 0.09]))
    ndd2 = NDData([3, 6, 9], unit='m',
                  uncertainty=VarianceUncertainty([0.16, 0.25, 0.36]))
    result = ndd1 * ndd2
    assert np.array_equal(result.data, [6, 24, 54])
    assert isinstance(result.uncertainty, VarianceUncertainty)
    assert np.array_equal(result.uncertainty.array, [0.12, 0.96, 3.24])


def test_varianceuncertainty_propagate_divide():
    ndd1 = NDData([6, 24, 54], unit='m',
                  uncertainty=VarianceUncertainty([0.09, 0.36, 1.44]))
    ndd2 = NDData([2, 4, 6], unit='m',
                  uncertainty=VarianceUncertainty([0.01, 0.04, 0.09]))
    result = ndd1 / ndd2
    assert np.array_equal(result.data, [3, 6, 9])
    assert isinstance(result.uncertainty, VarianceUncertainty)
    assert np.array_equal(result.uncertainty.array, [0.12, 0.96, 3.24])


def test_inversevariance_propagate_add():
    ndd1 = NDData([1, 2, 3], unit='m',
                  uncertainty=InverseVariance([100, 400, 900]))
    ndd2 = NDData([4, 5, 6], unit='m',
                  uncertainty=InverseVariance([1600, 2500, 3600]))
    result = ndd1 + ndd2
    assert np.array_equal(result.data, [5, 7, 9])
    assert isinstance(result.uncertainty, InverseVariance)
    assert np.array_equal(result.uncertainty.array, [
                          1066.66666667, 2933.33333333, 4800.0])


def test_inversevariance_propagate_subtract():
    ndd1 = NDData([4, 5, 6], unit='m',
                  uncertainty=InverseVariance([1600, 2500, 3600]))
    ndd2 = NDData([1, 2, 3], unit='m',
                  uncertainty=InverseVariance([100, 400, 900]))
    result = ndd1 - ndd2
    assert np.array_equal(result.data, [3, 3, 3])
    assert isinstance(result.uncertainty, InverseVariance)
    assert np.array_equal(result.uncertainty.array, [
                          1066.66666667, 2933.33333333, 4800.0])


def test_inversevariance_propagate_multiply():
    ndd1 = NDData([2, 4, 6], unit='m',
                  uncertainty=InverseVariance([100, 400, 900]))
    ndd2 = NDData([3, 6, 9], unit='m',
                  uncertainty=InverseVariance([1600, 2500, 3600]))
    result = ndd1 * ndd2
    assert np.array_equal(result.data, [6, 24, 54])
    assert isinstance(result.uncertainty, InverseVariance)
    assert np.array_equal(result.uncertainty.array, [
                          1066.66666667, 2933.33333333, 4800.0])


def test_inversevariance_propagate_divide():
    ndd1 = NDData([6, 24, 54], unit='m',
                  uncertainty=InverseVariance([900, 3600, 14400]))
    ndd2 = NDData([2, 4, 6], unit='m',
                  uncertainty=InverseVariance([100, 400, 900]))
    result = ndd1 / ndd2
    assert np.array_equal(result.data, [3, 6, 9])
    assert isinstance(result.uncertainty, InverseVariance)
    assert np.array_equal(result.uncertainty.array, [
                          1066.66666667, 2933.33333333, 4800.0])
