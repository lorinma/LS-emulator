# Author: Dr. Ling Ma
# https://il.linkedin.com/in/cvlingma
import trimesh
import pandas as pd
import numpy as np

class Scanner:
    def __init__(self):
        pass
    
    def scan(self, l2g, entities,Resolution):
        delta=np.deg2rad(Resolution)
        g2l=trimesh.transformations.inverse_matrix(l2g)
        all_points=pd.DataFrame()
        for entity in entities:
            geometry=entity['Geometry']
            GlobalId=entity['GlobalId']
            mesh=trimesh.Trimesh(vertices=geometry['Vertices'],faces=geometry['Faces'])
            # transform to local
            mesh.apply_transform(g2l)
            # get all the rays
            min_v=mesh.bounds[0]
            max_v=mesh.bounds[1]
            r_min=np.sqrt(np.sum(min_v**2))
            r_max=np.sqrt(np.sum(max_v**2))
            theta_min=np.arcsin(min_v[1]/r_min)
            theta_max=np.arcsin(max_v[1]/r_max)
            phi_min=-np.arctan(min_v[0]/min_v[2])
            phi_max=-np.arctan(max_v[0]/max_v[2])
            theta_range=np.arange(np.floor(min(theta_min,theta_max)/delta),np.ceil(max(theta_min,theta_max)/delta)+1)
            phi_range=np.arange(np.floor(min(phi_min,phi_max)/delta),np.ceil(max(phi_min,phi_max)/delta)+1)
            rays=list()
            theta_val=list()
            phi_val=list()
            for theta in theta_range:
                for phi in phi_range:
                    v=[[0,0,0],[-np.sin(phi*delta)*np.cos(theta*delta),np.sin(theta*delta),np.cos(phi*delta)*np.cos(theta*delta)]]
                    rays.append(v)
                    phi_val.append(int(phi))
                    theta_val.append(int(theta))
            # get intersected points
            intersects=mesh.ray.intersects_location(rays)
            cord=list()
            theta_indices=list()
            phi_indices=list()
            Rs=list()
            for inx,intersect in enumerate(intersects):
                if len(intersect)>0:
                    for v in intersect:
                        cord.append(v)
                        theta_indices.append(theta_val[inx])
                        phi_indices.append(phi_val[inx])
                        Rs.append(np.sum(v**2))
            data = pd.DataFrame({ 'GlobalId':GlobalId,'phi_indices':phi_indices,'theta_indices':theta_indices,'Distance':Rs,'Point':cord})
            all_points=all_points.append(data)
        return all_points
    
    def savePCD(self,all_points,TrimbleVersionID,_id,l2g):
        all_points=all_points.reset_index(drop=True)
        data_grouped = all_points.groupby(['phi_indices','theta_indices']).agg({'Distance':'min'})
        data_grouped = data_grouped.reset_index()
        data_grouped = data_grouped.rename(columns={'Distance':'Distance_min'})
        PCD = pd.merge(all_points, data_grouped, how='left', on=['phi_indices','theta_indices'])
        PCD = PCD[PCD['Distance'] == PCD['Distance_min']]
        PCD = PCD.reset_index(drop=True)
        PCD_transformed = trimesh.transformations.transform_points(PCD['Point'].tolist(), l2g).tolist()
        PCD['Point']=PCD_transformed
        PCD['TrimbleVersionID']=TrimbleVersionID
        pcd_file='pcd/'+_id+'.pcd'
        count=len(PCD)
        if 1:
            f = open(pcd_file,'w')
            f.write('VERSION .7\n')
            f.write('FIELDS x y z\n')
            f.write('SIZE 4 4 4\n')
            f.write('TYPE F F F\n')
            f.write('COUNT 1 1 1\n')
            f.write('WIDTH '+str(count)+'\n')
            f.write('HEIGHT 1\n')
            f.write('VIEWPOINT 0 0 0 1 0 0 0\n')
            f.write('POINTS '+str(count)+'\n')
            f.write('DATA ascii\n')
            for inx, row in PCD.iterrows():
                point=row['Point']
                f.write(str(point[0])+' '+str(point[1])+' '+str(point[2])+' '+'\n')
            f.close()
        