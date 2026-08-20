#!/usr/bin/env python3

import pyvista as pv

if __name__ == '__main__':
    sphere = pv.Sphere()
    pl = pv.Plotter()
    pl.add_mesh(sphere,color='red',show_edges=True)
    pl.show()