# Synthetic scanner
simulate scanning a model

## Installation:
### install trimesh, flask, pymongo and pandas
sudo apt-get update; sudo apt-get install cmake openscad blender libspatialindex-dev libgeos-dev -y; pip install trimesh[all] python-dotenv==0.5.0 flask pymongo;conda install pandas -y

### setup credentials in env
touch .env

MONGO_HOST=xxxx

MONGO_PORT=0000

MONGO_USERNAME=xxxx

MONGO_PASSWORD=xxxx

MONGO_DBNAME=xxxx