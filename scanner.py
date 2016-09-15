from OCC.gp import gp_Pnt,gp_Lin,gp_Dir
from OCC.IntCurvesFace import IntCurvesFace_ShapeIntersector
from OCC.TopoDS import TopoDS_Compound
from OCC.BRep import BRep_Builder
import ifcopenshell.geom
import ifcopenshell
import math
import numpy as np
from time import time

def scan(resolution,viewpoint,ifcfilename,pcdfilename):
    # resolution = 0.02
    # viewpoint = [-21.08,11.63,3.29]
    # name = 'beam'

    t0 = time()
    origin=gp_pnt(viewpoint[0],viewpoint[1],viewpoint[2])
    # specify to return pythonocc shapes from ifcopenshell.geom.create_shape()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.use_python_opencascade, true)
    settings.set(settings.force_ccw_face_orientation, true)
    # open the ifc file using ifcopenshell
    #ifc_file = ifcopenshell.open(name + '.ifc')
    ifc_file = ifcopenshell.open(ifcfilename)
    pcd_file = pcdfilename

    model=topods_compound()
    builder=brep_builder()
    builder.makecompound(model)
    products = ifc_file.by_type("ifcproduct")
    for product in products:
        if product.is_a("ifcopeningelement"): continue
        if product.is_a("ifcgrid"): continue
        if product.representation:
            try :
                shape = ifcopenshell.geom.create_shape(settings, product).geometry
                builder.add(model,shape)
            except :
                print 'this line is skipped: '+ str(product.id())

    scanner = intcurvesface_shapeintersector()
    scanner.load(model,0.1)

    data = []
    for theta in np.arange(-math.pi/2, math.pi/2, resolution):
        for phi in np.arange(-math.pi/2, math.pi/2, resolution):
            direction = gp_dir(math.cos(theta) * math.sin(phi), math.sin(theta), -math.cos(theta) * math.cos(phi))
            line = gp_lin(origin, direction)
            scanner.performnearest(line,-1000,1000)
            if(scanner.isdone() and scanner.nbpnt()>0):
                intersection = scanner.pnt(1)
                point = {
                    "x": intersection.x(),
                    "y": intersection.y(),
                    "z": intersection.z()
                }
                data.append(point)
    count = len(data)
    f = open(pcd_file,'w')
    f.write('version .7\n')
    f.write('fields x y z\n')
    f.write('size 4 4 4\n')
    f.write('type f f f\n')
    f.write('count 1 1 1\n')
    f.write('width '+str(count)+'\n')
    f.write('height 1\n')
    f.write('viewpoint 0 0 0 1 0 0 0\n')
    f.write('points '+str(count)+'\n')
    f.write('data ascii\n')

    for i in xrange(count):
        f.write(str(data[i]['x'])+' '+str(data[i]['y'])+' '+str(data[i]['z'])+'\n')

    f.close()
    t1 = time()
    print("done in %f s." % (t1-t0))
