"""Recombine one-render-per-light images with adjustable weights."""


def weighted_sum(images, weights):
    return sum(w * img for w, img in zip(weights, images))
