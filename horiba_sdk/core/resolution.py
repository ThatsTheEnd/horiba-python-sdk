from typing import final


@final
class Resolution:
    """Width x height, non-zero, non-negative resolution in pixels.

    Attributes:
        width (int): The width in pixels
        height (int): The height in pixels
    """

    def __init__(self, width: int, height: int) -> None:
        """Initializes a new Resolution instance

        Args:
            width (int): width
            height (int): height

        Raises:
            Exception: when an invalid (<= 0) width or height is given
        """
        if width <= 0 or height <= 0:
            raise Exception(f'Cannot have width or height less or equal to 0: {width} x {height} not allowed')

        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        """Width in pixels.

        Returns:
            int: width
        """
        return self._width

    @property
    def height(self) -> int:
        """Height in pixels.

        Returns:
            int: height
        """
        return self._height
