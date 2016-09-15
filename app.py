# TODO clear the code
import os
from time import time
from gridfs import GridFS
from werkzeug import secure_filename
from flask import Flask, redirect, url_for,request, render_template,make_response,jsonify,send_from_directory
from pymongo import MongoClient
from bson.objectid import ObjectId

from OCC.TopoDS import TopoDS_Compound
from OCC.BRep import BRep_Builder
from OCC.Visualization import Tesselator
import ifcopenshell.geom
import ifcopenshell
from py import scanner

ALLOWED_EXTENSIONS = set(['ifc'])
UPLOAD_FOLDER = './ifcfiles'
STATIC_FOLDER = './static'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#setup connection to mongo docker container
client = MongoClient(host='db',port=27017)
db = client.eastbimdb
grid_fs = GridFS(db)

@app.route('/pcd/<fid>')
def pcdViewer(fid):
    return render_template('pointcloud.html',fid=fid)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/scan')
def scan():
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')
    viewpoint = [float(x), float(y), float(z)]
    resolution = 0.02
#     m0 = request.args.get('m0', 0.0, type=float)
#     m1 = request.args.get('m1', 0.0, type=float)
#     m2 = request.args.get('m2', 0.0, type=float)
#     m3 = request.args.get('m3', 0.0, type=float)
#     m4 = request.args.get('m4', 0.0, type=float)
#     m5 = request.args.get('m5', 0.0, type=float)
#     m6 = request.args.get('m6', 0.0, type=float)
#     m7 = request.args.get('m7', 0.0, type=float)
#     m8 = request.args.get('m8', 0.0, type=float)
#     m9 = request.args.get('m9', 0.0, type=float)
#     m10 = request.args.get('m10', 0.0, type=float)
#     m11 = request.args.get('m11', 0.0, type=float)
#     m12= request.args.get('m12', 0.0, type=float)
#     m13 = request.args.get('m13', 0.0, type=float)
#     m14 = request.args.get('m14', 0.0, type=float)
#     m15 = request.args.get('m15', 0.0, type=float)
    # mat = request.args.getlist('cameraMatrix', 0.0, type=float)
    # mat = request.args.get('cameraMatrix', 0.0, type=float)

    # get the path together with the filename
    fid =  request.args.get('fid')
    ifcfilename = str(os.path.join(app.config['UPLOAD_FOLDER'],fid+'.ifc'))
    pcdfilename = str(os.path.join(app.config['STATIC_FOLDER'],fid+'.pcd'))
    scanner.scan(resolution,viewpoint,ifcfilename,pcdfilename)
    # return jsonify(result=0,fid=2)
    # return jsonify(result=a + b,fid=UPLOAD_FOLDER)
    return jsonify(x=x,y=y,z=z,fid=fid)
    # return jsonify(result=mat[0],fid=fid)


#parse the ifc file and render it
@app.route('/viewer/<fid>')
def ifcViewer(fid):
    filename = str(os.path.join(app.config['UPLOAD_FOLDER'], fid+'.ifc'))
    jsonfile = str(os.path.join(app.config['STATIC_FOLDER'], fid+'.js'))

    # Specify to return pythonOCC shapes from ifcopenshell.geom.create_shape()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    settings.set(settings.FORCE_CCW_FACE_ORIENTATION, True)
    # Open the IFC file using IfcOpenShell
    ifc_file = ifcopenshell.open(filename)
    # return str(ifc_file.by_type("IfcProject")[0])
    model=TopoDS_Compound()
    builder=BRep_Builder()
    builder.MakeCompound(model)
    products = ifc_file.by_type("IfcProduct")
    for product in products:
        if product.is_a("IfcOpeningElement"): continue
        if product.is_a("IfcGrid"): continue
        if product.Representation:
            try :
                shape = ifcopenshell.geom.create_shape(settings, product).geometry
                builder.Add(model,shape)
            except :
                print 'this line is skipped: '+ str(product.id())
    #Tesselate the shape to JSON
    print("Tesselate shape ...")
    t0 = time()
    tess = Tesselator(model)
    t1 = time()
    print("done in %f s." % (t1-t0))
    print("Exporting tesselation to JSON ...")
    t2 = time()
    tess.ExportShapeToJSON(jsonfile)
    t3 = time()
    print("done in %f s." % (t3-t2))
    return render_template('viewer.html',fid=str(fid))


#upload file to mongodb and webserver using html form
@app.route('/upload', methods=['POST'])
def upload_file():
    #get the file from the form in index.html
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        email = request.form['email']

        #add a new file, and add other attributes the file, e.g. user,..
        with grid_fs.new_file(filename=filename,email=email) as fp:
            fp.write(file)
            file_id = fp._id

        # save the file to the web server so that ifcopenshell can load it
        if grid_fs.find_one(file_id) is not None:
            mFile = grid_fs.get(ObjectId(file_id))
            pFile = open(os.path.join(app.config['UPLOAD_FOLDER'], str(file_id)+'.ifc'), 'w+')
            pFile.write(mFile.read())
            pFile.close()
            return redirect(url_for('ifcViewer',fid=str(file_id)))
    return redirect(url_for('home_page'))

#serve the file for future download
@app.route('/files/<oid>')
def serve_gridfs_file(oid):
    file = grid_fs.get(ObjectId(oid))
    response = make_response(file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(oid+'.ifc')
    return response

#serve the file for future download
@app.route('/pcd/<oid>')
def downloadPCD(oid):
    return send_from_directory(app.config['UPLOAD_FOLDER'], oid, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
