from argparse import ArgumentParser
from os.path import isfile
from flask import Flask, send_file
from MapRenderCache import MapRenderCache
from loguru import logger as log


def main():
    ap = ArgumentParser()
    ap.add_argument("-s", "--stylesheet", type=str, required=True, help="Path to the mapnik xml stylesheet")
    ap.add_argument("--width", type=int, default=256, help="Width of the tiles")
    ap.add_argument("--height", type=int, default=256, help="Height of the tiles")
    ap.add_argument("--host", type=str, default="127.0.0.1", help="Host to listen on")
    ap.add_argument("--port", type=int, default=6363, help="Port to listen on")
    ap.add_argument("--debug", action="store_true", help="Enable debug mode")
    ap.add_argument("--directory", type=str, default="cache", help="Directory to store the tiles in")
    a = ap.parse_args()

    if not isfile(a.stylesheet):
        log.error(f"Stylesheet '{a.stylesheet}' does not exist.")
        exit()

    cache = MapRenderCache(a.stylesheet, a.directory, a.width, a.height)
    app = Flask(__name__)

    # zoom / longitude / latitude
    @app.route("/<int:z>/<float:x>/<float:y>")
    def get_tile(z: int, x: float, y: float):
        return send_file(cache.get_tile(x, y, z), "image/png")

    app.run(a.host, a.port, a.debug, threaded=True)


if __name__ == '__main__':
    main()
