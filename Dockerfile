FROM python:3.12

RUN mkdir /FA

WORKDIR /FA

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

#RUN pip install -r requirements.txt \
#    && apt-get update \
#    && apt-get install -y openssh-server \
#    && mkdir /var/run/sshd \
#    && echo 'root:root123' | chpasswd \
#    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
#EXPOSE 22
#HEALTHCHECK --interval=1s --timeout=3s \
#    CMD ["/usr/sbin/sshd", "-D"]
#EXPOSE 8005:8005
#CMD ["uvicorn", "main:app", "--port", "8005", "--host", "0.0.0.0", "--reload"]
#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
