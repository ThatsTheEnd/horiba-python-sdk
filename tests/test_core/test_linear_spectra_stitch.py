import re

import pytest
from numpy.testing import assert_array_almost_equal

from horiba_sdk.core.linear_spectra_stitch import LinearSpectraStitch


def test_stitch_spectra_with_overlap():
    # Arrange
    spectrum1 = [[500.1, 510.3, 520.7, 530.5], [10.0, 20.5, 30.2, 40.1]]
    spectrum2 = [[520.5, 530.8, 540.0, 550.2], [35.4, 45.1, 55.0, 65.3]]
    stitch = LinearSpectraStitch([spectrum1, spectrum2])

    expected_x = [500.1, 510.3, 520.7, 530.5, 530.8, 540.0, 550.2]
    expected_y = [10.0, 20.5, 32.8,  37.75, 45.1, 55.0, 65.3]

    # Act
    x_combined, y_combined = stitch.stitched_spectra()

    # Assert
    assert_array_almost_equal(x_combined, expected_x)
    assert_array_almost_equal(y_combined, expected_y)


def test_stitch_spectra_raises_exception_on_no_overlap():
    # Arrange
    spectrum1 = [[500.1, 510.3], [10.0, 20.5]]
    spectrum2 = [[520.7, 530.5], [30.2, 40.1]]

    # Act & Assert
    with pytest.raises(Exception, match=re.compile('^No overlapping region between spectra')):
        _stitch = LinearSpectraStitch([spectrum1, spectrum2])
