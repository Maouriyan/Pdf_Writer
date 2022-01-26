from flask import Flask,request
from waitress import serve
import argparse
from pdf import *

app = Flask(__name__)


@app.route('/',methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        try:
            generated_url = main(request.json)
        except Exception as e:
            print(e)
            return 404
        return str(generated_url)
    return '<h1>Hello, World!</h1>'

def mainu():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "-a",
        "--addr",
        default="0.0.0.0",
        type=str,
        help="The IP address to bind to.",
    )

    ap.add_argument(
        "-p",
        "--port",
        default=80,
        type=int,
        help="The port to bind to.",
    )

    args = ap.parse_args()
    serve(app, host=args.addr, port=args.port)


if __name__ == "__main__":
    #main()
    app.run(host='0.0.0.0', port=9019)
