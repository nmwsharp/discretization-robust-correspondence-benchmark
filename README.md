# Discretization Robust Segmentation Benchmark

Machine learning on 3D surfaces is challenging, because there could be many different representations/samplings ("discretizations") which all represent the same underlying shape. For instances, there could be many different triangle meshes of a surface. Often, one would want a model which generalizes across these representations, but many common models do not have that property. The purpose of this benchmark is to measure generalization of 3D machine learning models across different discretizations

This benchmark contains test meshes of human bodies, derived from the MPI-FAUST dataset, remeshed/resampled according to several policies. The task is to predict correspondence to a template mesh, defined by predicting vertex indicies. We intentionally provide *test data only*. The intent of this benchmark is that methods train on the ordinary FAUST template meshes, the evaluate on this dataset. This measures the ability of the method to generalize to new, unseen discretizations of shapes.

![example image of data](TODO link)

From: **DiffusionNet: Discretization Agnostic Learning on Surfaces**, *Nicholas Sharp, Souhaib Attaiki, Keenan Crane, Maks Ovsjanikov*, conditionally accepted to ACM ToG 2021.

Please cite this benchmark as:
```bib
@article{sharp2021diffusion,
  author = {Sharp, Nicholas and Attaiki, Souhaib and Crane, Keenan and Ovsjanikov, Maks},
  title = {DiffusionNet: Discretization Agnostic Learning on Surfaces},
  journal = {ACM Trans. Graph.},
  volume = {XX},
  number = {X},
  year = {20XX},
  publisher = {ACM},
  address = {New York, NY, USA},
}
```


### In this repository
- `data/` 
  - `iso/` Isotropically remeshed meshes
  - ...
- `scripts/` Meshlab & Python scripts which were used to generate the data.

#### Notes about the data
- ...


### Papers using this dataset
(create a pull request to add more!)
- ["DiffusionNet: Discretization Agnostic Learning on Surfaces"](https://arxiv.org/abs/2012.00888) by Sharp et al., ACM ToG 2021

### License

The scripts which generate the data are available for any use under an MIT license (C) Nicholas Sharp 2021.

The remeshed/sampled meshes are derived from the [MPI-FAUST](http://faust.is.tue.mpg.de/) dataset, and thus governed by [the same license](http://faust.is.tue.mpg.de/data_license), which in-particular forbids commercial use.
