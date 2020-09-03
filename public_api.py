import flask
import pandas_gbq
import pandas
import json
from flask import jsonify, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def getDataFromBigQuery():
    project_id = "helical-bonsai-275519"
    sql = "SELECT * FROM `helical-bonsai-275519.california_demand.today_demand` LIMIT 1000"
    df = pandas_gbq.read_gbq(sql, project_id=project_id)
    return df


@app.route('/', methods=['GET'])
def home():   
    return "<h2>Hello!</h2><p>If you want to get stock demand, please visit <a href='http://localhost:5000/getDemand'>http://localhost:5000/getDemand</a></p>"


@app.route('/getDemand', methods=['GET'])
def getDemand():
    df = getDataFromBigQuery()
    res = json.loads(df.to_json(orient="records"))
    
    return jsonify({'demands': res})    


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

''' Main '''
if __name__ == '__main__':
    app.run()
