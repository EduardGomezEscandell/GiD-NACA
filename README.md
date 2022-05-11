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
<img src="https://user-images.githubusercontent.com/47142856/167839599-f3affaf1-d86f-4858-8c09-461eb7b32d8e.png" height="250"> <img src="https://user-images.githubusercontent.com/47142856/167840533-f9a1d9fc-ec5f-4fa2-b380-a53cc5624b47.png" height="250">


### NACA 0012 in a bullet domain
```python
naca_digits = "0012"
npoints = 100

boundary_type = "bullet"
boundary_radius = 10
```
<img src="https://user-images.githubusercontent.com/47142856/167840803-e8b9e6e8-e213-4676-9a6c-f9f955b91260.png" height="300"> <img src="https://user-images.githubusercontent.com/47142856/167841064-fd0857e8-08e7-49ef-9cd0-acedeb33d35c.png" height="300">

