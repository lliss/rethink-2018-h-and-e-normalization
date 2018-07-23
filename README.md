# rethink-2018-h-and-e-normalization

A Python module for image normalization of H&E stained histology slides.

## Dependencies

  - sklearn
  - numpy
  - imageio

## Usage

```python
import imageio
from h_and_e_normalization import colorassign_manual

loaded_image = imageio.imread('/path/to/image.tif')
result = colorassign_manual(loaded_image)
```