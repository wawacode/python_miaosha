from flask import Flask,request
from redis_connector import plus_counter,create_order
from rabbitmq_connector import enter_order_queue
from rabbitmq_connector import enter_overtime_queue
import uuid
import jsonify
import json
app=Flask(__name__)
@app.route("/purchase")
def purchase():
    user_id=request.args.get("user_id")
    goods_id=request.args.get("goods_id")
    res={
        "status":False,
        "msg":""
    }
    flag=plus_counter(goods_id)
    if flag:
        order_id=uuid.uuid1()
        order_info={
            "goods_id":goods_id,
            "user_id":user_id,
            "order_id":str(order_id)
        }
        try:
            create_order(order_info)
            enter_order_queue(order_info)
            enter_overtime_queue(order_info)
            res["status"]=True
            res["msg"]="抢购成功，请在15分钟内付款"
            res["order_id"]=str(order_id)
            res=json.dumps(res,ensure_ascii=False)
            print(res)
            print("成功")
            return  app.response_class(res,content_type="application/json")
        except Exception as e:
            print("log:",e)
            res["status"]=False
            res["msg"]="抢购出错，请重试"+str(e)
            res=json.dumps(res,ensure_ascii=False)
            print(res)
            print("失败")
            return app.response_class(res,content_type="application/json")
    else:
        res["status"]=False
        res["msg"]="商品已售馨"
        res=json.dumps(res,ensure_ascii=False)
        print(res)
        print("失败")
        return app.response_class(res,content_type="application/json")
if __name__=="__main__":
    app.run(threaded=True)