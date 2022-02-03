from typing import Tuple, List
import itertools

import numpy as np

from gaps.piece import Piece


def flatten_image(image: np.ndarray, piece_size: int, indexed: bool = False) -> Tuple[List[np.ndarray], int, int]:
    """Converts image into list of square pieces.

    Input image is divided into square pieces of specified size and than
    flattened into list. Each list element is PIECE_SIZE x PIECE_SIZE x 3

    :params image:      Input image.
    :params piece_size: Size of single square piece. Each piece is PIECE_SIZE x PIECE_SIZE
    :params indexed:    If True, list of Pieces with IDs will be returned, otherwise just plain list of ndarray pieces

    Usage::

        >>> from gaps.image_helpers import flatten_image
        >>> flat_image = flatten_image(image, 32)

    """
    rows, columns = image.shape[0] // piece_size, image.shape[1] // piece_size
    pieces = []

    # Crop pieces from original image
    for y in range(rows):
        for x in range(columns):
            left, top, right, down = x * piece_size, y * piece_size, (x + 1) * piece_size, (y + 1) * piece_size
            piece = np.empty((piece_size, piece_size, image.shape[2]))
            piece[:, :, :] = image[top:down, left:right, :]
            pieces.append(piece)

    if indexed:
        pieces = [Piece(value, index) for index, value in enumerate(pieces)]

    return pieces, rows, columns


def assemble_image(pieces: List[np.ndarray], rows: int, columns: int) -> np.ndarray:
    """Assembles image from pieces.

    Given an array of pieces and desired image dimensions, function
    assembles image by stacking pieces.

    :params pieces:  Image pieces as an array.
    :params rows:    Number of rows in resulting image.
    :params columns: Number of columns in resulting image.

    Usage::

        >>> from gaps.image_helpers import assemble_image
        >>> from gaps.image_helpers import flatten_image
        >>> pieces, rows, cols = flatten_image(...)
        >>> original_img = assemble_image(pieces, rows, cols)

    """
    image = np.vstack([
        np.hstack([pieces[i * columns + j] for j in range(columns)]) for i in range(rows)
    ]).astype(np.uint8)
    return image
