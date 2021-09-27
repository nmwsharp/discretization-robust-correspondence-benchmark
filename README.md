# Discretization Robust Segmentation Benchmark

One challenge of machine learning on 3D surfaces is that there are many different representations/samplings ("discretizations") which all encode the same underlying shape---consider e.g. different triangle meshes of a surface. We expect models to generalize across these representations; the purpose of this benchmark is to measure generalization of 3D machine learning models across different discretizations

This benchmark contains test meshes of human bodies, derived from the [MPI-FAUST](http://faust.is.tue.mpg.de/) dataset, remeshed/resampled according to several policies. The task is to predict correspondence, defined by predicting the nearest vertex index on the template mesh. We intentionally provide *test data only*. The intent of this benchmark is that methods train on the ordinary FAUST template meshes, then evaluate on this dataset. This measures the ability of the method to generalize to new, unseen discretizations of shapes.

![example image of data](https://github.com/nmwsharp/discretization-robust-segmentation-benchmark/blob/main/data_image.png?raw=true)

From: [**DiffusionNet: Discretization Agnostic Learning on Surfaces**](https://arxiv.org/abs/2012.00888), *Nicholas Sharp, Souhaib Attaiki, Keenan Crane, Maks Ovsjanikov*, conditionally accepted to ACM ToG 2021.

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

### Remeshing/sampling policies
- `iso` Meshes are isotropically remeshed, to have a roughly uniform distribution of vetices, with approximately equilateral triangles
- `qes` Meshes are first refined to have many more vertices, then simplified back to approximately 2x the original resolution using Quadric Error Simplification
- `mc` Meshes are volumetrically reconstructed, and a mesh is extracted via the marching cubes algorithm.
- `dense` Meshes are refined to have nonuniform density by choosing 5 random faces, refining the mesh in the vicinity of the face, then isotropically remeshing.
- `cloud` A point cloud, with normals, sampled uniformly from the mesh


### In this repository
- `data/` 
  - `iso/` 
    - `tr_reg_iso_080.ply` FAUST test mesh 80, remeshed according to the `iso` strategy
    - `tr_reg_iso_080.txt` Ground-truth correspondence indices, per-vertex
    - ...
    - `tr_reg_iso_099.ply`
    - `tr_reg_iso_099.txt`
  - `qes/`
    - `tr_reg_qes_080.ply`
    - `tr_reg_qes_080.txt`
    - ...
  - `mc/` 
    - `tr_reg_mc_080.ply`
    - `tr_reg_mc_080.txt`
    - ...
  - `dense/`
    - `tr_reg_dense_080.ply`
    - `tr_reg_dense_080.txt`
    - ...
  - `cloud/`
    - `tr_reg_cloud_080.ply` A sampled point cloud from FAUST test mesh 80, with normals
    - `tr_reg_cloud_080.txt` Ground-truth correspondence indices, per-point
    - ...
- `scripts/` Meshlab & Python scripts which were used to generate the data.

#### Notes about the data
- The meshes are not necessarily high quality! In particular, the `mc` meshes have coincident vertices and degenerate leftover from the marching cubes process. Such artifacts are a common occurence in real data.


### Benchmark Task

This benchmark is designed for template correspondence via vertex index prediction. That is, for each vertex (resp., point) in a test shape, we predict the corresponding nearest vertex on a template mesh. The FAUST template mesh has 6890 vertices, so this is essentially a segmentation problem with classes from [0, 6899]. Note that although popular in past work, this categorical formulation is surely *not* the best notion of correspondence between surfaces. However, it is very simple, and exposes a tendancy to overfit to discretization, which makes it a good choice for this benchmark.

The first 80 original [MPI-FAUST](http://faust.is.tue.mpg.de/) template meshes should be used as training data: i.e. `tr_reg_000.ply`-`tr_reg_080.ply`. The last 20 shapes are taken as the test set, and remeshed/resampled for the purpose of this benchmark. These original meshes are already deformations of the template, so the ground truth vertex labels are simply `[0,1,2,3,4...]`. We do not host the original data here; you must download it from http://faust.is.tue.mpg.de/.

After training on the first 80 original FAUST meshes, we evaluate on the test meshes, predicting corresponding vertices. Error is measured by the geodesic distance along the template mesh between the predicted vertex and the ground-truth vertex. (% of vertices predicted exactly correct is *not* really a meaningful metric.) See [this repo](https://github.com/nmwsharp/diffusion-net/tree/master/experiments) for a full example of training and eval scripts.

### Papers using this dataset
(create a pull request to add more!)
- ["DiffusionNet: Discretization Agnostic Learning on Surfaces"](https://arxiv.org/abs/2012.00888) by Sharp et al., ACM ToG 2021

### License

The scripts which generate the data are available for any use under an MIT license (C) Nicholas Sharp 2021.

The remeshed/sampled meshes are derived from the [MPI-FAUST](http://faust.is.tue.mpg.de/) dataset, governed by [this license](http://faust.is.tue.mpg.de/data_license) (which allows derivative works). 
