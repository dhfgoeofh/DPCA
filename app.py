from flask import Flask, request, jsonify, render_template
from flask_restx import Resource, Api

import json
import clr
clr.AddReference("System.Data")
from System.Data import Odbc
from System.Data import CommandType
from System.Data.Odbc import OdbcCommand, OdbcParameter
from multipledispatch import dispatch
from module.modules import *

app = Flask(__name__)
api = Api(app)

    
@api.route("/api/<string:query>/<string:formData>")  # http://127.0.0.1:5000/test?CALL TEST1(?);&{"id":"1"}
class webAPI(Resource):
    def get(self, query, formData):
        try:
            formData = eval(formData)
            data = queryFunc(query, formData)
        except:
            try:
                data = queryFunc(query)
            except Exception as e:
                data = str(e)
        return jsonify(data)
    
    def post(self, query, formData):
        print("post")
        try:
            formData = eval(formData)
            data = queryFunc(query, formData)
        except:
            try:
                data = queryFunc(query)
            except Exception as e:
                data = str(e)
        return jsonify(data)

    def put(self, query, formData):
        print("put")
        try:
            formData = eval(formData)
            data = get_count(query, formData)
        except:
            try:
                data = queryFunc(query)
            except Exception as e:
                data = str(e)
        return jsonify(data)

    def delete(self, query, formData):
        print("delete")
        try:
            formData = eval(formData)
            data = queryFunc(query, formData)
        except:
            try:
                data = queryFunc(query)
            except Exception as e:
                data = str(e)
        return jsonify(data)

@api.route("/count/<string:query>/<string:formData>")  # http://127.0.0.1:5000/test?query=CALL TEST1(?);&formData={"id":"1"}
class DPCA_Count(Resource):
    def get(self, query, formData):
        try:
            formData = eval(formData)
            data = get_count(query, formData)
        except:
            try:
                data = get_count(query)
            except Exception as e:
                data = str(e)
        return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
