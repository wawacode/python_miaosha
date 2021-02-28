import pika
import json
credentials=pika.PlainCredentials("guest","guest")
rabbitmq_conn=pika.BlockingConnection(pika.ConnectionParameters(host="localhost",credentials=credentials))
def enter_order_queue(order_info):
    user_id=order_info.get("user_id")
    order_id=order_info.get("order_id")
    goods_id=order_info.get("goods_id")
    if user_id is None or order_id is None or goods_id is None:
        return False
    channel=rabbitmq_conn.channel()
    exchange="order.exchange"
    queue="order.queue"
    routing_key="order."+str(goods_id)+"."+str(user_id)
    channel.exchange_declare(exchange=exchange,exchange_type="topic",durable=True)
    channel.queue_bind(exchange=exchange,queue=queue)
    message=json.dumps(order_info)
    print("333333333333")
    channel.basic_publish(exchange=exchange,routing_key=routing_key,body=message)
    return True
def enter_overtime_queue(order_info,timeout=15):
    user_id=order_info.get("user_id")
    order_id=order_info.get("order_id")
    goods_id=order_info.get("goods_id")
    if user_id is None or goods_id is None or order_id is None:
        return False
    channel=rabbitmq_conn.channel()
    delay_exchange="overtime.exchange.delay"
    delay_queue="overtime.queue.delay"
    exchange="overtime.exchange"
    queue="overtime.queue"
    channel.exchange_declare(exchange=exchange,exchange_type="fanout",durable=True)
    channel.queue_bind(exchange=exchange,queue=queue)
    arguments={
        "x-message-ttl":1000*60*timeout,
        "x-dead-letter-exchange":exchange,
        "x-dead-letter-routing-key":queue
    }
    channel.exchange_declare(exchange=delay_exchange,exchange_type="fanout",durable=True)
    channel.queue_declare(queue=delay_queue,durable=True,arguments=arguments)
    channel.queue_bind(exchange=delay_exchange,queue=delay_queue)
    message=json.dumps(order_info)
    channel.basic_publish(exchange=delay_exchange,body=message,routing_key="")
    return True
