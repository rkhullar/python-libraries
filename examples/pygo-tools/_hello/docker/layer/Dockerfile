ARG PYTHON_VERSION=3.12
FROM public.ecr.aws/sam/build-python${PYTHON_VERSION}
COPY build-internal.sh ./
COPY wheel wheel/
RUN ./build-internal.sh
ENTRYPOINT ["/bin/sh"]
