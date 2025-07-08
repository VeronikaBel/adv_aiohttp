#!/bin/bash

# Запуск PostgreSQL
echo "Запускаем PostgreSQL..."
docker-compose up -d

# Ждем 3 секунды
sleep 3

# Запуск сервера
echo "Запускаем сервер..."
python server.py