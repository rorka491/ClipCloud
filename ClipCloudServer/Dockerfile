FROM python:3.13-slim


RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .


CMD [ "uvicorn", "main:app", "--reload", "--port", "8000" ]




