FROM public.ecr.aws/docker/library/python:3.12.3-bullseye

COPY requirements.txt ${LAMBDA_TASK_ROOT} 

RUN pip3 install -r requirements.txt

COPY src/* ${LAMBD_TASK_ROOT}

CMD [ "uvicorn", "main:app", "--reload" ]