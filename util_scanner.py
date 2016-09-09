# from OCC.gp import gp_Pnt,gp_Lin,gp_Dir
# from OCC.IntCurvesFace import IntCurvesFace_ShapeIntersector
# from OCC.TopoDS import TopoDS_Compound
# from OCC.BRep import BRep_Builder
# import ifcopenshell.geom
# import ifcopenshell
# import math
# import numpy as np
# from time import time

class Scanner:
    def __init__(self):
        pass
    
    def scan(self, resolution,viewpoint,ifcfilename,pcdfilename):
        pass
#     # resolution = 0.02
#     # viewpoint = [-21.08,11.63,3.29]
#     # name = 'Beam'

#     t0 = time()
#     origin=gp_Pnt(viewpoint[0],viewpoint[1],viewpoint[2])
#     # Specify to return pythonOCC shapes from ifcopenshell.geom.create_shape()
#     settings = ifcopenshell.geom.settings()
#     settings.set(settings.USE_PYTHON_OPENCASCADE, True)
#     settings.set(settings.FORCE_CCW_FACE_ORIENTATION, True)
#     # Open the IFC file using IfcOpenShell
#     #ifc_file = ifcopenshell.open(name + '.ifc')
#     ifc_file = ifcopenshell.open(ifcfilename)
#     pcd_file = pcdfilename

#     model=TopoDS_Compound()
#     builder=BRep_Builder()
#     builder.MakeCompound(model)
#     products = ifc_file.by_type("IfcProduct")
#     for product in products:
#         if product.is_a("IfcOpeningElement"): continue
#         if product.is_a("IfcGrid"): continue
#         if product.Representation:
#             try :
#                 shape = ifcopenshell.geom.create_shape(settings, product).geometry
#                 builder.Add(model,shape)
#             except :
#                 print 'this line is skipped: '+ str(product.id())

#     scanner = IntCurvesFace_ShapeIntersector()
#     scanner.Load(model,0.1)

#     data = []
#     for theta in np.arange(-math.pi/2, math.pi/2, resolution):
#         for phi in np.arange(-math.pi/2, math.pi/2, resolution):
#             direction = gp_Dir(math.cos(theta) * math.sin(phi), math.sin(theta), -math.cos(theta) * math.cos(phi))
#             line = gp_Lin(origin, direction)
#             scanner.PerformNearest(line,-1000,1000)
#             if(scanner.IsDone() and scanner.NbPnt()>0):
#                 intersection = scanner.Pnt(1)
#                 point = {
#                     "x": intersection.X(),
#                     "y": intersection.Y(),
#                     "z": intersection.Z()
#                 }
#                 data.append(point)
#     count = len(data)
#     f = open(pcd_file,'w')
#     f.write('VERSION .7\n')
#     f.write('FIELDS x y z\n')
#     f.write('SIZE 4 4 4\n')
#     f.write('TYPE F F F\n')
#     f.write('COUNT 1 1 1\n')
#     f.write('WIDTH '+str(count)+'\n')
#     f.write('HEIGHT 1\n')
#     f.write('VIEWPOINT 0 0 0 1 0 0 0\n')
#     f.write('POINTS '+str(count)+'\n')
#     f.write('DATA ascii\n')

#     for i in xrange(count):
#         f.write(str(data[i]['x'])+' '+str(data[i]['y'])+' '+str(data[i]['z'])+'\n')

#     f.close()
#     t1 = time()
#     print("done in %f s." % (t1-t0))
