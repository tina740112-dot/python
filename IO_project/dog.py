from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return """
    <meta charset="utf-8">
    <h1>拾光髮飾</h1>
    <p>為日常，添一點優雅。</p>
    <h2>珍珠髮箍｜NT$ 1,280</h2>
    <h2>琉璃花朵髮夾｜NT$ 980</h2>
    """

if __name__ == "__main__":
    app.run(debug=True)