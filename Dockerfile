FROM python:3.11
SHELL ["/bin/bash", "-c"]
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim
RUN useradd -rms /bin/bash migration && chmod 777 /opt /run
WORKDIR /migration
RUN mkdir -p /migration/static /migration/media && chown -R migration:migration /migration && chmod 755 /migration
COPY --chown=migration:migration . .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
USER migration
CMD ["gunicorn", "-b", "0.0.0.0:8000", "djangomigration.wsgi:application"]


