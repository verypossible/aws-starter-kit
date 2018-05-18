FROM python:2

RUN pip install -U \
        pip \
        python-dateutil==2.6.1 \
        boto3

RUN mkdir -p /stacks
COPY setup.py /stacks
WORKDIR /stacks

# Set up this project as an editable package, so we can iterate on the blueprints
RUN pip install -e .
