FROM python:3.10-bullseye

#Force the stdout and stderr streams to be unbuffered
ENV PYTHONUNBUFFERED 1

#Set env variables for working dir
ENV APP_PROJ=/southern_test

# create Django directory inside docker container & install django
COPY . $APP_PROJ

# create limited user and assign ownership to working directory
RUN useradd southern && chown southern:southern -R $APP_PROJ

# change to working directory
WORKDIR $APP_PROJ

# install dependencies
RUN pip install poetry
COPY pyproject.toml poetry.lock $APP_PROJ/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry lock \
  && poetry install --no-interaction --no-ansi


# copy bash script
COPY docker/start.sh /start.sh

#Expose port
EXPOSE 8000

# set permission for our bash file
RUN chmod +x /start.sh && chown southern:southern /start.sh

USER southern

CMD ["sh","/start.sh"]