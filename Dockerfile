FROM ghcr.io/andrewembry312-hub/elabs-server/cosyvoice-runpod:latest

COPY handler.py /workspace/handler.py

WORKDIR /workspace
CMD ["python", "-u", "handler.py"]
