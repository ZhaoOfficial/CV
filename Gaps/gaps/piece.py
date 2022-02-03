from typing import Tuple

import numpy as np

class Piece(object):
    '''Represents single jigsaw puzzle piece.

    Each piece has identifier so it can be
    tracked across different individuals

    :param image: ndarray representing piece's RGB values
    :param index: Unique id withing piece's parent image

    Usage::

        >>> from gaps.piece import Piece
        >>> piece = Piece(image[:28, :28, :], 42)

    '''

    def __init__(self, image: np.ndarray, index: int):
        self.image = image
        self.id = index

        self.left   = image[:, 0, :]
        self.right  = image[:, -1, :]
        self.top    = image[0, :, :]
        self.bottom = image[-1, :, :]

        self.gradient_left   = (image[:, 0, :] - image[:, 1, :]).reshape(-1, 3)
        self.gradient_right  = (image[:, -1, :] - image[:, -2, :]).reshape(-1, 3)
        self.gradient_top    = (image[0, :, :] - image[1, :, :]).reshape(-1, 3)
        self.gradient_bottom = (image[-1, :, :] - image[-2, :, :]).reshape(-1, 3)

        self.mu_left   = np.mean(self.gradient_left, axis = 0)
        self.mu_right  = np.mean(self.gradient_right, axis = 0)
        self.mu_top    = np.mean(self.gradient_top, axis = 0)
        self.mu_bottom = np.mean(self.gradient_bottom, axis = 0)

        self.sigma_left_inv = np.linalg.pinv(np.cov(self.gradient_left.T))
        self.sigma_right_inv = np.linalg.pinv(np.cov(self.gradient_right.T))
        self.sigma_top_inv = np.linalg.pinv(np.cov(self.gradient_top.T))
        self.sigma_bottom_inv = np.linalg.pinv(np.cov(self.gradient_bottom.T))

    def __getitem__(self, index: int):
        return self.image.__getitem__(index)

    def size(self) -> int:
        '''Returns piece size'''
        return self.image.shape[0]

    def shape(self) -> Tuple[int, int, int]:
        '''Returns shape of piece's image'''
        return self.image.shape
