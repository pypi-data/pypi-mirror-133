# gdschamfer
***gdschamfer*** is a Python add-on module for [gdspy](https://github.com/heitzmann/gdspy) that can perform [chamfering](https://tutorial45.com/autocad-tutorial-16-chamfer-and-autocad-fillet/) operation on GDSII files. It extends the [fillet function](https://github.com/heitzmann/gdspy/blob/bdf29791f7bc41a9f867b6467eb9f1cb911e501d/gdspy/polygon.py#L383) in gdspy so that:

- inside corners (i.e., concave bends) or outside corners (i.e., convex bends) can be selectively chamfered or filleted.

- orthogonal corners can be selectively chamfered or filleted.

The operation of chamfering leads to corners being replaced with 45&deg; slanting edges. An example of inside corners of a polygon being chamfered is shown below:
<p align="center" width="100%"><img src="https://github.com/arun-goud/gdschamfer/blob/main/demo/chamfer_example.png" width="50%" height="50%"><p>

On the other hand, the filleting operation that gdspy's `fillet()` function does will result in concave curved corners for inside corners and convex (or rounded) corners for outside corners. When the fillet radius of curvature tends to infinity the resulting fillet starts to approximate a chamfer.

# Usage #
To use ***gdschamfer*** install its [PyPI python distribution package](https://pypi.org/project/gdschamfer/) using pip:

```
pip install gdschamfer
```

In your python scripts place the import statement
```
import gdschamfer
```

There are 3 functions available for use:

1) **`gdschamfer.chamfer_polygons(...)`**: Use this to perform chamfering of gdspy Polygon objects.

2) **`gdschamfer.chamfer_cell(...)`**: Use this to perform chamfering of gdspy Cell objects.

3) **`gdschamfer.chamfer_gds(...)`**: Use this to perform chamfering on GDSII file.

# Chamfer style #
To understand how the option **chamfer_style** modifies the corners consider the GDSII file [`demo/input.gds`](https://github.com/arun-goud/gdschamfer/blob/main/demo/input.gds) shown below:

<p align="center" width="100%"><img src="https://github.com/arun-goud/gdschamfer/blob/main/demo/input_gds.png"><p>

---
## a) When **chamfer_style = <span style="color:blue">"inside_corners"</span>**: ##

![GDSII with 3 polygons, with 2 on layer 20 and 1 on layer 22 showing chamfered inside corners](https://github.com/arun-goud/gdschamfer/blob/main/demo/chamfer_inside_corners.png)

---
## b) When **chamfer_style = <span style="color:red">"outside_corners"</span>**: ##

![GDSII with 3 polygons, with 2 on layer 20 and 1 on layer 22 showing chamfered outside corners](https://github.com/arun-goud/gdschamfer/blob/main/demo/chamfer_outside_corners.png)

---

## c) When **chamfer_style = <span style="color:green">"all_corners"</span>**: ##

![GDSII with 3 polygons, with 2 on layer 20 and 1 on layer 22 showing chamfered corners](https://github.com/arun-goud/gdschamfer/blob/main/demo/chamfer_all_corners.png)

---

