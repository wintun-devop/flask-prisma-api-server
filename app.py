from urllib import response
from flask import Flask,request,jsonify,make_response
from prisma import Prisma, register
from prisma.models import Product
import config
import asyncio


app = Flask(__name__)

app.config['SECRET_KEY']=config.APP_SECRET_KEY

@app.route('/', methods=['GET'])
def index():
  response = {
      "status":"success",
      "message":"API Server is working well!"
  }
  return make_response(jsonify(response))

@app.route("/api/v1/product",methods=["POST"])
async def create_item():
    #database connection
    db =Prisma(auto_register=True)
    await db.connect()
    data = request.get_json()
    name=data["name"]
    model_no=data["model_no"]
    description=data["description"]
    try:
        product = await db.product.create(data={
                "name":name,
                "model_no":model_no,
                "description":description
            })
        response = dict(product)
        return make_response(jsonify(response),201)
    except Exception as e:
        response = {
        "status":"fail",
        "message":"Resource already exit!"
        }
        return e
     


if __name__ == "__main__":   
  app.run(debug=True, port=5000, host='0.0.0.0')