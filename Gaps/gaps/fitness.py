from gaps.piece import Piece

import numpy as np


def dissimilarity_measure(first: Piece, second: Piece, method: str = 'Mahalanobis', orientation: str = 'LR') -> float:
    '''Calculates color difference over all neighboring pixels over all color channels.

    The dissimilarity measure relies on the premise that adjacent jigsaw pieces in the original image tend to share
    similar colors along their abutting edges, i.e., the sum (over all neighboring pixels) of squared color differences
    (over all three color bands) should be minimal. Let pieces pi , pj be represented in normalized L*a*b*
    space by corresponding W x W x 3 matrices, where W is the height/width of each piece (in pixels).

    :params first:        First input piece for calculation.
    :params second:       Second input piece for calculation.
    :params orientation:  How input pieces are oriented.
    :params method:       The way to calculate the error.

                          LR => 'Left - Right'
                          TD => 'Top - Down'

    Usage::

        >>> from gaps.fitness import dissimilarity_measure
        >>> from gaps.piece import Piece
        >>> p1, p2 = Piece(), Piece()
        >>> dissimilarity_measure(p1, p2, method = 'Mahalanobis', orientation = 'TD')

    '''
    color_diff = None

    if method == 'L2':
        if orientation == 'LR':
            color_diff = first.right - second.left
        if orientation == 'TD':
            color_diff = first.bottom - second.top

    elif method == 'Mahalanobis':
        if orientation == 'LR':
            # l_to_r.shape = (piece_size, 3)
            l_to_r = (second.left - first.right) - first.mu_right
            diff_lr = l_to_r @ first.sigma_right_inv @ l_to_r.T
            diff_rl = l_to_r @ second.sigma_left_inv @ l_to_r.T
            color_diff = diff_lr + diff_rl
        if orientation == 'TD':
            # t_to_d.shape = (piece_size, 3)
            t_to_d = (second.top - first.bottom) - first.mu_bottom
            diff_td = t_to_d @ first.sigma_bottom_inv @ t_to_d.T
            diff_dt = t_to_d @ second.sigma_top_inv @ t_to_d.T
            color_diff = diff_td + diff_dt

    squared_color_difference = np.power(color_diff / 255.0, 2)
    value = np.sqrt(np.sum(squared_color_difference))
    return value
