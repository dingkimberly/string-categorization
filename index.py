from flask import render_template
from flask import Flask 
from flask_restful import Resource, Api
import sys
sys.path.insert(0, './backend')
from cos_sim import getCategory
app = Flask(__name__)

api = Api(app)

class Category(Resource):
    def get(self, str):
        return {'Category': getCategory(str)}

api.add_resource(Category, '/<string:str>')

