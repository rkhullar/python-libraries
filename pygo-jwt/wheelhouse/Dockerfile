ARG BUILD_MODE
ARG PYTHON_VERSION=3.12

FROM public.ecr.aws/sam/build-python${PYTHON_VERSION} as aws_sam_base
FROM python:${PYTHON_VERSION}-alpine as alpine_base

FROM ${BASE_IMAGE == "alpine" ? "alpine_base" : "sam_base"} AS final_base
COPY *.whl ./
COPY test.py ./
ENTRYPOINT ["sh"]

# docker build --build-arg BASE_IMAGE=alpine --platform amd64 -t test-alpine-amd64 .
# docker build --build-arg BASE_IMAGE=alpine --platform arm64 -t test-alpine-arm64 .
# docker build --build-arg BASE_IMAGE=aws-sam --platform amd64 -t test-aws-sam-amd64 .
# docker build --build-arg BASE_IMAGE=aws-sam --platform arm64 -t test-aws-sam-arm64 .