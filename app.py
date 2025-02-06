from flask import Flask, redirect, request, jsonify, flash
from helper import extract_table, check_extension, process_content, extract_subset_transaction_data
from werkzeug.utils import secure_filename
app = Flask(__name__)
ALLOWED_EXTENSION = {'pdf'}
import io

@app.route("/test", methods = ["GET"], endpoint = "test")
def test():
    return jsonify({"message" : "test route working"}), 200
@app.route("/process_file", methods = ["POST"], endpoint = "process_file")
def process_file():
    try:
        #request.files contain referal to files via their "name" in regular form or "key" in postman 
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({'message' : 'Cannot detect file in HTTP request'}), 400
        cur = request.files['file']
        if (check_extension(cur.filename) not in ALLOWED_EXTENSION):
            return jsonify({'message' : 'Only accept pdf file'}), 400
        contents = cur.read()
        temp, transaction_data, income_data = extract_table(io.BytesIO(contents))
        if len(temp) == 0:
            return jsonify({'message' : 'Unable to parse content of files or file is empty'}), 400
        res_model = process_content(temp)
        # extracted_data =  extract_subset_transaction_data(transaction_data)
        if (len(transaction_data) > 30):
            extracted_data = transaction_data[-25 :]
        else:
            extracted_data = transaction_data
        print(extracted_data)
        return jsonify({'message' : 'Successfully receive file', 'data' : res_model, 'transaction_data' : extracted_data, 'income_data' : income_data}), 200
    except Exception as e:
        print(e)
        return jsonify({'message' : f'Error at process_file: {e}'}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
