import json
import time
import pika

RABBITMQ_HOST = "rabbitmq"

def process_notification(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    event_type = data.get("event")
    payload = data.get("data")

    print(f"\n[Worker] 📥 Tarea recibida: {event_type}")

    if event_type == "SEND_NEWSLETTER":
        print(f"[Worker] 📧 Enviando boletín: '{payload['article_title']}' a {payload['subscribers_count']} usuarios...")
        time.sleep(3)  # Simula el tiempo de envío de correos
        print("[Worker] ✅ Boletín enviado con éxito.")

    # Confirmación de tarea completada
    ch.basic_ack(delivery_tag=method.delivery_tag)

def process_media(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    event_type = data.get("event")
    payload = data.get("data")

    print(f"\n[Worker] 📥 Tarea recibida: {event_type}")

    if event_type == "RESIZE_IMAGE":
        print(f"[Worker] 🖼️ Generando miniaturas para '{payload['image_url']}' ({payload['dimensions']})...")
        time.sleep(2)  # Simula procesamiento/compresión de la imagen
        print("[Worker] ✅ Imagen procesada y subida al servidor CDN.")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()

            channel.queue_declare(queue="notifications_queue", durable=True)
            channel.queue_declare(queue="media_queue", durable=True)

            # Evita sobrecargar al worker asignándole 1 mensaje a la vez
            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(queue="notifications_queue", on_message_callback=process_notification)
            channel.basic_consume(queue="media_queue", on_message_callback=process_media)

            print("[Worker] 🚀 Escuchando colas 'notifications_queue' y 'media_queue' en RabbitMQ...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("[Worker] ⚠️ Reintentando conexión con RabbitMQ en 5 segundos...")
            time.sleep(5)

if __name__ == "__main__":
    main()
