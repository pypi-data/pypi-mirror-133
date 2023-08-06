FROM public.ecr.aws/amazonlinux/amazonlinux:latest

RUN yum -y update
RUN yum -y install yum-utils
RUN yum -y groupinstall development

RUN yum list python3*
RUN yum -y install python3 python3-dev python3-pip python3-virtualenv

RUN mkdir /app
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install poetry venv-pack jupyter
RUN yum install -y which
RUN yum install -y java-1.8.0-openjdk

RUN pip3 install pyspark==2.4.5
RUN pip3 install findspark
RUN pip3 install tomlkit==0.7.2
RUN pip3 install boto3==1.20.23
RUN pip3 install tqdm==4.62.3
RUN pip3 install datefinder==0.7.1
RUN pip3 install fire==0.4.0
RUN pip3 install pandas==1.3.5
RUN pip3 install ipykernel==6.6.0
RUN pip3 install pexpect==4.8.0
RUN pip3 install black==21.12b0

COPY . /pyemr
COPY . /usr/local/lib/python3.7/site-packages/pyemr

WORKDIR /app
ENV PATH=/root/.local/bin:$PATH

ENV POETRY_VIRTUALENVS_PATH=./.docker_venv
ENV ARROW_PRE_0_15_IPC_FORMAT=1
ENV PYARROW_IGNORE_TIMEZONE=1
RUN echo 'alias pyemr="python3 -m pyemr.cli local_test $@"' >> ~/.bashrc