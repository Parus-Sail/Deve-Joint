FROM python:3.10.10-slim as python-base
# первая стадия, чистая база, только закешируем слой и зададим энвы
ENV APP_DIR=/app
ENV APP_USER=service_user

ENV BUILD = production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as poetry
# вторая стадия - поставим poetry и no-dev зависисмости (все долгоиграющие), закешировали слой
RUN pip install poetry
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml /
# т.к. мы используем докер, нужно отключить виртуальное окружение (масло масленное),
# затем ставим зависимости, если BUILD "production", пакеты для разработки не ставим
RUN poetry config virtualenvs.create false && \
    poetry install $(test $BUILD == production && echo "--no-dev")


FROM poetry as ready
# третья стадия, за счет того что большинство пакетов уже установлено, доустановка dev либ будет быстрая
WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR ${APP_DIR}
COPY app .

RUN chmod +x ./entrypoint.sh
CMD ["gunicorn", "DeveJoint.wsgi", "-b 0.0.0.0:8080"]
ENTRYPOINT [ "sh", "./entrypoint.sh" ]



