ARG PYTHON_VERSION=3.12
FROM public.ecr.aws/sam/build-python${PYTHON_VERSION}
RUN dnf install -y golang make
RUN pip install -U pip setuptools
RUN pip install pygo-tools
COPY example example/
COPY setup.py config.json MANIFEST.in ./
RUN python setup.py bdist_wheel
ENTRYPOINT ["/bin/sh"]
