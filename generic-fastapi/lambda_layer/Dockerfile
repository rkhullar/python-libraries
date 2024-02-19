ARG PYTHON_VERSION=3.12
FROM public.ecr.aws/sam/build-python${PYTHON_VERSION}
COPY Pipfile build.sh ./
RUN ./build.sh
ENTRYPOINT ["/bin/sh"]
