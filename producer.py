import json
import pika
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Multimedios Async Notification Service",
    description="Microservicio para encolar tareas asíncronas con RabbitMQ",
    version="1.0.0"
)

RABBITMQ_HOST = "rabbitmq"

def send_to_queue(queue_name: str, message: dict):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        channel = connection.channel()
        
        # Declarar cola durable (los mensajes no se pierden si RabbitMQ se reinicia)
        channel.queue_declare(queue=queue_name, durable=True)
        
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # Mensaje persistente en disco
            )
        )
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con RabbitMQ: {str(e)}")

# Modelos de datos recibidos por la API
class NewsletterRequest(BaseModel):
    article_title: str
    target_group: str
    subscribers_count: int

class ImageProcessRequest(BaseModel):
    image_url: str
    dimensions: str

@app.post("/api/v1/notifications/send-newsletter")
def enqueue_newsletter(payload: NewsletterRequest):
    message = {
        "event": "SEND_NEWSLETTER",
        "data": payload.model_dump()
    }
    send_to_queue("notifications_queue", message)
    return {
        "status": "queued",
        "message": f"Boletín '{payload.article_title}' encolado correctamente para {payload.subscribers_count} suscriptores."
    }

@app.post("/api/v1/media/process-image")
def enqueue_image_processing(payload: ImageProcessRequest):
    message = {
        "event": "RESIZE_IMAGE",
        "data": payload.model_dump()
    }
    send_to_queue("media_queue", message)
    return {
        "status": "queued",
        "message": f"Procesamiento de imagen encolado para {payload.image_url}."
    }
