# Microservicio de Notificaciones Asíncronas & Procesamiento de Media

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Microservicio desacoplado diseñado para optimizar tareas pesadas en segundo plano mediante colas de mensajes. Permite procesar peticiones masivas (boletines informativos a miles de usuarios) y procesamiento de imágenes sin bloquear la API principal de una plataforma de noticias de alto tráfico.

---

## 📐 Arquitectura del Sistema

El sistema utiliza el patrón **Productor / Consumidor** mediante el protocolo AMQP:

```text
  [ Cliente / Front / Webhook ]
               │
               ▼
   [ API Productor - FastAPI ]  ── (Publica tarea) ──► [ Broker - RabbitMQ ]
   (Responde <200 OK> al instan-                      (Mantiene persistencia
    te sin bloquear al usuario)                       en colas con ACK)
                                                              │
                                                              ▼
                                                   [ Worker - Consumidor ]
                                                   (Procesa tareas asíncronas
                                                    en segundo plano)
