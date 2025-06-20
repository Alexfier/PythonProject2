from http.server import BaseHTTPRequestHandler, HTTPServer

# Параметры запуска сервера
hostName = "localhost"
serverPort = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Метод для обработки GET-запросов"""
        try:
            # Читаем HTML-файл
            with open("contacts.html", "r", encoding="utf-8") as file:
                html_content = file.read()

            # Устанавливаем код ответа и заголовки
            self.send_response(200)
            self.send_header("Content-type", "text/html")  # Изменено на text/html
            self.end_headers()

            # Отправляем содержимое HTML-файла в ответ
            self.wfile.write(bytes(html_content, "utf-8"))
        except FileNotFoundError:
            # Если файл не найден, отправляем код 404
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Page Not Found</h1>")

if __name__ == "__main__":
    # Инициализация и запуск веб-сервера
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started at http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    # Остановка сервера
    webServer.server_close()
    print("Server stopped.")