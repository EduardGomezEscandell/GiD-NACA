# GiD NACA generator
This repository contains scripts to generate NACA airfoils in a format easy to import to GiD.

## How to use
In order to generate the airfoil, run file `generate_airfoil.py`. To choose the settings, open the file
and you can edit:
- Which NACA 4-digit airfoil you want to generate
- How many points do you want in each surface
- The shape of the boundary and its size
- The output filename

To open from GiD, use `Files > Import > Batch File` and select the file you generated. You can also use `Ctrl+b`.

## Examples
### NACA 4412 in a lens domain
```python
naca_digits = "4412"
npoints = 100

boundary_type = "lens"
boundary_radius = 10
```

### NACA 0012 in a buller domain
```python
naca_digits = "0012"
npoints = 100

boundary_type = "bullet"
boundary_radius = 10
```
