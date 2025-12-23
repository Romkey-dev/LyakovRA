# Асинхронное программирование в Go

## Структура проекта

```
lab-async-go/
├── cmd/
│   └── main.go                      # Демонстрация
├── internal/
│   ├── async/
│   │   ├── goroutines.go           # Базовые операции с горутинами
│   │   ├── goroutines_test.go      # Тесты горутин
│   │   ├── channels.go             # Работа с каналами
│   │   ├── channels_test.go        # Тесты каналов
│   │   ├── worker_pool.go          # Worker Pool паттерн
│   │   └── worker_pool_test.go     # Тесты Worker Pool
│   └── server/
│       ├── http.go                 #  HTTP сервер
│       └── http_test.go            # Тесты HTTP сервера
├── go.mod
└── README.md
```

## Запуск

```bash
# Запуск демонстрационстрации
go run cmd/main.go

# Запуск всех тестов
go test ./...

# Запуск тестов с race
go test -race ./...

# Запуск тестов с покрытием
go test -cover ./...
```

