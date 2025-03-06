docker run -it --rm python:3.10 /bin/bash
# Dentro del contenedor:
python -m venv --copies /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt
