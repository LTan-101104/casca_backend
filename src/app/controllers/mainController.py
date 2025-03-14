from controllers import Controller
from models import SampleModel
from flask import jsonify

class mainController(Controller[SampleModel]):
    # containing main operations to be mapped by routes
    def test():
        return jsonify({'message' : 'test route working'}), 200
    
    def process_file():
        return jsonify({'message' : 'sample process file functions working'}), 200