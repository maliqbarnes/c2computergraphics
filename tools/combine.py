"""Recombine partial renders (per-light weighted sum, interleaved tiles)."""
import numpy as np


def weighted_sum(images, weights):
    return sum(w * img for w, img in zip(weights, images))


def interleave(images, factor):
    # TODO: images[i] rendered with pixel offset i; merge into one high-res image
    raise NotImplementedError
