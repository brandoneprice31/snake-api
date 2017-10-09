from sanic import Sanic

from users import users

app = Sanic()
app.blueprint(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
