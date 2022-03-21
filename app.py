from flask import Flask, request, jsonify
import pickle
import numpy as np

model = pickle.load(open('model.pkl','rb'))
app=Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/')
def home():
    return "Hello"

@app.route('/route', methods=['POST'])
def route():
    src = request.form.get('src')
    des = request.form.get('des')
    
    input_query = np.array([[src,des]])
    # result = model.predict(input_query)[0]
    return jsonify({'safest route': str(input_query)})



if __name__ == "__main__":
    app.run(debug='true')