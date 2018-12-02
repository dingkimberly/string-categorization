from flask import render_template
from flask import Flask 
from flask_restful import Resource, Api
import sys
sys.path.insert(0, './backend')
import cos_sim
app = Flask(__name__)

api = Api(app)

class Category(Resource):
    def get(self, str):
        return {'Category': cos_sim.getCategory(str)}

api.add_resource(Category, '/<string:str>')

