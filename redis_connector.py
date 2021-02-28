import redis
import pika
redis_pool=redis.ConnectionPool(host="localhost",port=6379,password="",max_connections=512)
redis_conn=redis.Redis(connection_pool=redis_pool)
def plus_counter(goods_id,storage=100):
    count=redis_conn.incr("sumcounters:"+str(goods_id))
    if count>storage:
        return False
    return True
def create_order(order_info):
    user_id=order_info.get("order_info")
    order_id=order_info.get("order_info")
    goods_id=order_info.get("goods_id")
    redis_conn.hset("order:"+str(goods_id),str(order_id),str(user_id))
    return True