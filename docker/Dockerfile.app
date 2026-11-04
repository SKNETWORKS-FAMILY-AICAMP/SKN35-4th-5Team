FROM python:3.12-slim

WORKDIR /app

# Use the same pinned dependencies and Python version as the API image.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src:/app \
    PROJECT_ROOT=/app \
    UI_DATA_MODE=api

# The UI reads regulations, ingredients, market references and forecasts locally.
COPY --chown=appuser:appuser src ./src
COPY --chown=appuser:appuser configs ./configs
COPY --chown=appuser:appuser data ./data
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser .streamlit/config.toml ./.streamlit/config.toml

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=3).close()"]

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--browser.gatherUsageStats=false"]
