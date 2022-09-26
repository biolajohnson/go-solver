import numpy as np 


def euler_number():
  # as image can be a label image, transform it to binary
    image = (image > 0).astype(int)
    image = np.pad(image, pad_width=1, mode='constant')
    config = np.array([[0, 0, 0], [0, 1, 4], [0, 2, 8]])

    if image.ndim == 2:
        return coefs @ h
    else:
        return int(0.125 * coefs @ h)
