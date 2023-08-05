# Diffractsim: A diffraction simulator for exploring and visualizing physical optics

[![animation](/images/diffraction_animated.gif)](https://www.youtube.com/watch?v=Ft8CMEooBAE&list=PLYkZehxPE_IhyO6wC21nFP0q1ZYGIW4l1&index=1)

Accurate and easy to use Python light diffraction simulator which includes several propagation and visualization methods. 
You can use it for simulating the diffraction pattern of an arbitrary aperture, both with monochromatic and polychromatic light.

How the main method (angular spectrum) and the simulator work is described in this [Article](https://rafael-fuente.github.io/simulating-diffraction-patterns-with-the-angular-spectrum-method-and-python.html). Take a look to the [videos](https://www.youtube.com/watch?v=Ft8CMEooBAE&list=PLYkZehxPE_IhyO6wC21nFP0q1ZYGIW4l1&index=1) to see the animated simulations!

## Features

- [x] Arbitrary apertures
- [x] Arbitrary light spectrums
- [x] Lenses
- [x] Phase holograms generation and reconstruction
- [x] GPU acceleration
- [ ] Incoherent Light (coming soon)


## Installation
```
pip install diffractsim
```

Alternatively, to download the examples and the apertures as well, you can also build from source by cloning the repository and running from the main folder project on the command prompt:
```
python setup.py install
```

## Examples

To perform the simulations, just run from the [examples subdirectory](https://github.com/rafael-fuente/Diffraction-Simulations--Angular-Spectrum-Method/tree/main/examples) the corresponding Python scripts on the command prompt. 
To compute your own diffraction pattern, you'll need to specify in the script the aperture as an image and input its size.

```
python hexagon_monochromatic.py
```

[![N|Solid](/images/hexagon_monochromatic.png)](/examples/hexagon_monochromatic.py)

```
python hexagon_polychromatic.py
```

[![N|Solid](/images/hexagon_polychromatic.png)](/examples/hexagon_polychromatic.py)

```
python rectangular_grating_small.py
```

[![N|Solid](/images/rectangular_grating_small.png)](/examples/rectangular_grating_small.py)

```
python rectangular_grating_big.py
```

[![N|Solid](/images/rectangular_grating_big.png)](/examples/rectangular_grating_big.py)

```
python bahtinov_mask.py
```

[![N|Solid](/images/bahtinov_mask.png)](/examples/bahtinov_mask.py)

```
python rings.py
```

[![N|Solid](/images/rings.png)](/examples/rings.py)

```
python hexagonal_grating.py
```

[![N|Solid](/images/hexagonal_grating.png)](/examples/hexagonal_grating.py)

```
python diffraction_text.py
```

[![N|Solid](/images/text.png)](/examples/text.py)

For a more detailed discussion about simulating diffraction patterns using lenses, take a look at [these examples](https://github.com/rafael-fuente/Diffraction-Simulations--Angular-Spectrum-Method/blob/main/Simulations%20with%20lenses.md).

GPU acceleration requires having [CuPy](https://docs.cupy.dev/en/stable/install.html) installed and [CUDA](https://developer.nvidia.com/cuda-downloads) in your computer. 
To use GPU acceleration in your simulations, after import `diffractsim` add the line:

```python
diffractsim.set_backend("CUDA")
```
Cupy and CUDA aren't required to install and use this package, but they can offer a significant speed boost.

The first GPU accelerated run can be slow because Python is caching the required functions. The next time it can be about 10x and 100x faster than a CPU backend depending on your GPU. The speed boost raises as the grid gets larger.
