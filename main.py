from dotenv import load_dotenv
import os
import time
from PIL import Image
from http.server import BaseHTTPRequestHandler, HTTPServer

from imagegen import generate_image
from getcollection import get_collection

# Load environment variables
load_dotenv()

api_key = os.getenv("HYPIXEL_API_KEY")
uuid = os.getenv("PLAYER_UUID")
profile_name = os.getenv("PROFILE")

hostname = "0.0.0.0"
port = 8000

lastGenerated = 0

# Create a Webserver
class MyServer(BaseHTTPRequestHandler):
    # When receiving a GET request to redstone.png, get the collection amount and generate the image.
    def do_GET(self):
        global lastGenerated

        path = self.path.split("?")[0]
        params = self.path.split("?")[1].split("&") if len(self.path.split("?")) > 1 else []
        params = { p.split("=")[0]: p.split("=")[1] for p in params } if len(params) > 0 else {}

        if path == "/redstone.png":

            # Debug
            print(f"Request received. It has been {time.time() - lastGenerated} seconds since the last image generation.")

            # Send some image immediately
            cached_image = Image.open("image.png")
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            cached_image.save(self.wfile, "PNG")

            # If it's been more than 5 minutes since the last image generation, generate a new one
            if time.time() - lastGenerated > 300:

                # Generate and prepare a new image
                collection = get_collection(api_key, uuid, profile_name)
                new_image = generate_image(collection, params["rank"] if "rank" in params else 0)
                new_image.save("image.png")

                # Set the last generated time
                lastGenerated = time.time()

        # Otherwise, send a 404
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":        
    webServer = HTTPServer((hostname, port), MyServer)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")