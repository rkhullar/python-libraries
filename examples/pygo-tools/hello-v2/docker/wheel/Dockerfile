ARG PYTHON_VERSION=3.12
FROM public.ecr.aws/sam/build-python${PYTHON_VERSION}
RUN dnf install -y golang make
RUN pip install -U pip setuptools
RUN pip install pygo-tools
COPY example example/
COPY pyproject.toml MANIFEST.in ./
RUN python -m build -n --wheel
ENTRYPOINT ["/bin/sh"]
