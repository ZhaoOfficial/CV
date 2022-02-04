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

        gradient_left   = (self.left - image[:, 1, :]).reshape(-1, 3)
        gradient_right  = (self.right - image[:, -2, :]).reshape(-1, 3)
        gradient_top    = (self.top - image[1, :, :]).reshape(-1, 3)
        gradient_bottom = (self.bottom - image[-2, :, :]).reshape(-1, 3)

        # for Mahalanobis error
        self.mu_left   = np.mean(gradient_left, axis = 0)
        self.mu_right  = np.mean(gradient_right, axis = 0)
        self.mu_top    = np.mean(gradient_top, axis = 0)
        self.mu_bottom = np.mean(gradient_bottom, axis = 0)

        self.sigma_left_inv = np.linalg.pinv(np.cov(gradient_left.T))
        self.sigma_right_inv = np.linalg.pinv(np.cov(gradient_right.T))
        self.sigma_top_inv = np.linalg.pinv(np.cov(gradient_top.T))
        self.sigma_bottom_inv = np.linalg.pinv(np.cov(gradient_bottom.T))

    def __getitem__(self, index: int):
        return self.image.__getitem__(index)

    def size(self) -> int:
        '''Returns piece size'''
        return self.image.shape[0]

    def shape(self) -> Tuple[int, int, int]:
        '''Returns shape of piece's image'''
        return self.image.shape
