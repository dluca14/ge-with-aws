FROM public.ecr.aws/lambda/python:3.8

# Copy aws credentials
ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Copy project and data
COPY great_expectations ./project/great_expectations
COPY data ./project/data

# Install requirements
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
