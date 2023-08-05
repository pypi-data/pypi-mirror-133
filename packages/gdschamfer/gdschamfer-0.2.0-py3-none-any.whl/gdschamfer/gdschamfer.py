#!/usr/bin/env python
######################################################################
#                                                                    #
#              Copyright Arun Goud Akkala 2021.                      #
#  Distributed under the Boost Software License, Version 1.0.        #
#          (See accompanying LICENSE file or copy at                 #
#            https://www.boost.org/LICENSE_1_0.txt)                  #
#                                                                    #
######################################################################

import sys
import copy
import numpy as np

from gdspy.library import Cell, GdsWriter, GdsLibrary
from gdspy.polygon import Polygon, PolygonSet
from gdspy.operation import boolean


def chamfer_polygons(polys, radius, points_per_2pi=2, chamfer_style="inside_corners", orthogonal_corners_only=False):
    """
    Perform chamfering operation on corners of these polygons.

    Parameters
    ----------
    polys : iterable of array-like[N][2]
        List containing the coordinates of the vertices of each polygon.
    radius : number, array-like
        Radius of the corners (in *um*) within which the chamfer will
        be placed.  
        If number: all corners chamfered by that amount.  
        If array: specify chamfer radii on a per-polygon basis (length
        must be equal to the number of polygons in this `PolygonSet`).
        Each element in the array can be a number (all corners chamfered
        by the same amount) or another array of numbers, one per polygon
        vertex. Alternatively, the array can be flattened to have one
        radius per `PolygonSet` vertex.
    points_per_2pi : integer
        Number of vertices used to approximate a full circle. 
        If =2: results in a chamfer (corner is flattened)
        If >>2: results in a fillet (corner is rounded)
        The number of vertices in each corner of the polygon will be the
        fraction of this number corresponding to the angle encompassed by
        that corner with respect to 2 pi.
    chamfer_style : 'all_corners', 'inside_corners', 'outside_corners'
        Desired style of chamfer. Optionally, 'concave_corners' (same as
        same as 'inside_corners') and 'convex_corners' (same as 
        'outside_corners') can be passed.
    orthogonal_corners_only : bool
        If True, the application of chamfering operation will be restricted
        to corners that subtend 90 degrees. Use appropriate value for
        chamfer_style to choose between concave 90 degree and convex
        90 degree corners.

    Returns
    -------
    out : `PolygonSet`
        Polygons resulting from the chamfering operation..
    """
    two_pi = 2 * np.pi
    orig_polys = copy.deepcopy(polys)
    if np.isscalar(radius):
        radii = [[radius] * p.shape[0] for p in polys]
    else:
        if len(radius) == len(polys):
            radii = []
            for r, p in zip(radius, polys):
                if np.isscalar(r):
                    radii.append([r] * p.shape[0])
                else:
                    if len(r) != p.shape[0]:
                        raise ValueError(
                            "[GDSPY] Wrong length in chamfer radius list.  "
                            "Found {} radii for polygon with {} vertices.".format(
                                len(r), len(p.shape[0])
                            )
                        )
                    radii.append(r)
        else:
            total = sum(p.shape[0] for p in polys)
            if len(radius) != total:
                raise ValueError(
                    "[GDSPY] Wrong length in chamfer radius list.  "
                    "Expected lengths are {} or {}; got {}.".format(
                        len(polys), total, len(radius)
                    )
                )
            radii = []
            n = 0
            for p in polys:
                radii.append(radius[n : n + p.shape[0]])
                n += p.shape[0]

    for jj in range(len(polys)):
        vec = polys[jj].astype(float) - np.roll(polys[jj], 1, 0)
        length = (vec[:, 0] ** 2 + vec[:, 1] ** 2) ** 0.5
        ii = np.flatnonzero(length)
        if len(ii) < len(length):
            polys[jj] = np.array(polys[jj][ii])
            radii[jj] = [radii[jj][i] for i in ii]
            vec = polys[jj].astype(float) - np.roll(
                polys[jj], 1, 0
            )
            length = (vec[:, 0] ** 2 + vec[:, 1] ** 2) ** 0.5
        vec[:, 0] = vec[:, 0] / length
        vec[:, 1] = vec[:, 1] / length
        dvec = np.roll(vec, -1, 0) - vec
        norm = (dvec[:, 0] ** 2 + dvec[:, 1] ** 2) ** 0.5
        ii = np.flatnonzero(norm)
        dvec[ii, 0] = dvec[ii, 0] / norm[ii]
        dvec[ii, 1] = dvec[ii, 1] / norm[ii]
        dot = np.roll(vec, -1, 0) * vec
        theta = np.arccos(dot[:, 0] + dot[:, 1])
        ct = np.cos(theta * 0.5)
        tt = np.tan(theta * 0.5)

        new_points = []
        for ii in range(-1, len(polys[jj]) - 1):
            if theta[ii] > 1e-6:
                if orthogonal_corners_only:
                    if theta[ii] != 90.0*np.pi/180.0:
                        new_points.append(polys[jj][ii])
                        continue
                a0 = -vec[ii] * tt[ii] - dvec[ii] / ct[ii]
                a0 = np.arctan2(a0[1], a0[0])
                a1 = vec[ii + 1] * tt[ii] - dvec[ii] / ct[ii]
                a1 = np.arctan2(a1[1], a1[0])
                if a1 - a0 > np.pi:
                    a1 -= two_pi
                elif a1 - a0 < -np.pi:
                    a1 += two_pi
                n = max(
                    int(np.ceil(abs(a1 - a0) / two_pi * points_per_2pi) + 0.5), 2
                )
                a = np.linspace(a0, a1, n)
                ll = radii[jj][ii] * tt[ii]
                if ll > 0.49 * length[ii]:
                    r = 0.49 * length[ii] / tt[ii]
                    ll = 0.49 * length[ii]
                else:
                    r = radii[jj][ii]
                if ll > 0.49 * length[ii + 1]:
                    r = 0.49 * length[ii + 1] / tt[ii]
                new_points.extend(
                    r * dvec[ii] / ct[ii]
                    + polys[jj][ii]
                    + np.vstack((r * np.cos(a), r * np.sin(a))).transpose()
                )
            else:
                new_points.append(polys[jj][ii])
        polys[jj] = np.array(new_points)

    if chamfer_style.lower() == "all_corners":
        return PolygonSet(polys)
    elif chamfer_style.lower() in ["inside_corners", "concave_corners"]:
        chamfer_inside_corners = boolean(polys, orig_polys, operation="not", precision=1e-6, max_points=4000)
        return boolean(chamfer_inside_corners, orig_polys, operation="or", precision=1e-6, max_points=4000)
    elif chamfer_style.lower() in ["outside_corners", "convex_corners"]:
        return boolean(polys, orig_polys, operation="and", precision=1e-6, max_points=4000)
    else:
        raise ValueError("\nInvalid chamfer_style has been specified.\nAllowed values are:\n"
        "1) 'all_corners'\n2) 'inside_corners' (or) 'concave_corners'\n3) 'outside_corners' (or) 'convex_corners'")


def chamfer_cell(cell, layer=None, radius=2, points_per_2pi=2, chamfer_style="inside_corners", orthogonal_corners_only=False):
    """
    Perform chamfering operation on corners of this Cell object.

    Parameters
    ----------
    cell : `Cell`
        Cell object which needs to be chamfered.
    layer : tuple of integer or None
        The GDSII layer number, datatype (between 0 and 255) within the
        Cell to which chamfering needs to be applied. If None, then
        chamfering will be performed on all layers.
    radius : number, array-like
        Radius of the corners (in *um*) within which the chamfer will
        be placed.  
        If number: all corners chamfered by that amount.  
        If array: specify chamfer radii on a per-polygon basis (length
        must be equal to the number of polygons in this `PolygonSet`).
        Each element in the array can be a number (all corners chamfered
        by the same amount) or another array of numbers, one per polygon
        vertex. Alternatively, the array can be flattened to have one
        radius per `PolygonSet` vertex.
    points_per_2pi : integer
        Number of vertices used to approximate a full circle. 
        If =2: results in a chamfer (corner is flattened)
        If >>2: results in a fillet (corner is rounded)
        The number of vertices in each corner of the polygon will be the
        fraction of this number corresponding to the angle encompassed by
        that corner with respect to 2 pi.
    chamfer_style : string
        Desired style of chamfer - 'all_corners', 'inside_corners' or
        'concave_corners', 'outside_corners' or 'convex_corners'.
    orthogonal_corners_only : bool
        If True, the application of chamfering operation will be restricted
        to corners that subtend 90 degrees. Use appropriate value for
        chamfer_style to choose between concave 90 degree and convex
        90 degree corners.

    Returns
    -------
    out : `Cell`
        Cell resulting from the chamfering operation.
    """
    D_ch = Cell(cell.name+"_chamfered")
    poly_dict = {}
    if layer != None and not isinstance(layer, (tuple, list)):
        raise ValueError("\nInvalid layer has been specified.\nAllowed values are:\n1) None\n2) Tuple of length 2\n3) List of length")

    poly_dict = cell.get_polygons(by_spec=True)

    if layer != None and layer not in poly_dict:
        raise ValueError("\nSpecified layer (%s) could not be found in the cell."%(",".join(map(str, layer))))

    for lname in poly_dict:
        polygons = poly_dict[lname]
        if layer == None or lname == layer:
            chamfer_polys = chamfer_polygons(polygons, radius=radius, points_per_2pi=points_per_2pi, chamfer_style=chamfer_style, orthogonal_corners_only=orthogonal_corners_only)
        else:
            chamfer_polys = PolygonSet(polygons)
        for cp in chamfer_polys.polygons:
            D_ch.add(Polygon(cp, layer=lname[0], datatype=lname[1]))    
    return D_ch


def chamfer_gds(in_gds, out_gds, cellname="TOP", layer=None, precision=1e-9, radius=2, points_per_2pi=2, chamfer_style="inside_corners", orthogonal_corners_only=False):
    """
    Perform chamfering operation on corners of polygons in this GDSII file.

    Parameters
    ----------
    in_gds : string
        Filename of GDSII file which needs to be chamfered.
    out_gds : string
        Filename of GDSII file which is generated as the output of
        chamfering operation.
    cellname : string
        Name of cell in GDSII file which needs to be chamfered.
    layer : tuple of integer or None
        The GDSII layer number, datatype (between 0 and 255) within the
        Cell to which chamfering needs to be applied. If None, then
        chamfering will be performed on all layers.
    precision : positive integer or `None`
        Maximal number of digits for coordinates after scaling.
    radius : number, array-like
        Radius of the corners (in *um*) within which the chamfer will
        be placed.  
        If number: all corners chamfered by that amount.  
        If array: specify chamfer radii on a per-polygon basis (length
        must be equal to the number of polygons in this `PolygonSet`).
        Each element in the array can be a number (all corners chamfered
        by the same amount) or another array of numbers, one per polygon
        vertex. Alternatively, the array can be flattened to have one
        radius per `PolygonSet` vertex.
    points_per_2pi : integer
        Number of vertices used to approximate a full circle. 
        If =2: results in a chamfer (corner is flattened)
        If >>2: results in a fillet (corner is rounded)
        The number of vertices in each corner of the polygon will be the
        fraction of this number corresponding to the angle encompassed by
        that corner with respect to 2 pi.
    chamfer_style : string
        Desired style of chamfer - 'all_corners', 'inside_corners' or
        'concave_corners', 'outside_corners' or 'convex_corners'.
    orthogonal_corners_only : bool
        If True, the application of chamfering operation will be restricted
        to corners that subtend 90 degrees. Use appropriate value for
        chamfer_style to choose between concave 90 degree and convex
        90 degree corners.
    """
    gdsii = GdsLibrary()
    D = gdsii.read_gds(infile=in_gds)

    if layer != None and not isinstance(layer, (tuple, list)):
        raise ValueError("\nInvalid layer has been specified.\nAllowed values are:\n1) None\n2) Tuple of length 2\n3) List of length")

    D_ch = chamfer_cell(cell=D.cells[cellname], layer=layer, radius=radius, points_per_2pi=points_per_2pi, chamfer_style=chamfer_style, orthogonal_corners_only=orthogonal_corners_only)

    writer = GdsWriter(outfile=out_gds, precision=precision)
    writer.write_cell(D_ch)
    writer.close()


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Usage:\n\t%s <input_gds> <chamfered_output_gds> <cell_name> <layer> <radius> <points_per_2pi> <chamfer_style> <orthogonal_corners_only>" % sys.argv[0])
        sys.exit(1)

    infile = sys.argv[1] #"input.gds"
    outfile = sys.argv[2] #"output.gds"
    cellname = sys.argv[3]
    layer = [None  if x in ["", "None"] else tuple(map(int, x.strip("(").strip(")").split(","))) for x in [sys.argv[4]]][0]
    radius = float(sys.argv[5])
    points_per_2pi = float(sys.argv[6])
    chamfer_style = sys.argv[7]
    orthogonal_corners_only = [True if x == "True" else False for x in [sys.argv[8]]][0]

    print("Invoking chamfer_gds(in_gds='%s', out_gds='%s', cellname='%s', layer=%s, radius=%s, points_per_2pi=%s, chamfer_style='%s', orthogonal_corners_only=%s)"
            %(infile, outfile, cellname, layer, radius, points_per_2pi, chamfer_style, orthogonal_corners_only))
    chamfer_gds(in_gds=infile, out_gds=outfile, cellname=cellname, layer=layer, radius=radius, points_per_2pi=points_per_2pi, chamfer_style=chamfer_style, orthogonal_corners_only=orthogonal_corners_only)


