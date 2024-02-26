import uvicorn
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=args.port, reload=True)