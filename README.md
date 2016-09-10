# Synthetic scanner

simulate scanning a model

## Installation:

### nstall eve
sudo pip install git+git://github.com/nicolaiarocci/eve.git
sudo pip install python-dotenv==0.5.0 pyjwt

### install trimesh and its required libs
sudo apt-get install cmake openscad blender libspatialindex-dev libgeos-dev -y
sudo pip install trimesh[all]

### install pandas
conda install pandas -y

### setup credentials in env
touch .env

MONGO_HOST=xxxx

MONGO_PORT=0000

MONGO_USERNAME=xxxx

MONGO_PASSWORD=xxxx

MONGO_DBNAME=xxxx