FROM python:3.8-slim AS build
WORKDIR /app 

# Copy requirements first for better caching
COPY requirements.txt /app/  

RUN apt-get update && \
# Installs the necessary build tools (build-essential) and PostgreSQL development libraries (libpq-dev).
apt-get install -y build-essential libpq-dev && \
# When you install packages using apt-get, they are first downloaded to the cache, and after installation, this cache is usually not needed anymore. reducing the image size.
apt-get clean && \
# These files are used only for caching information about available packages. Removing them frees up space in your image.
rm -rf /var/lib/apt/lists/* && \
# install Python packages but not to cache them locally.
    pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /app/wheels -r /app/requirements.txt 

# Copy only the Python application files
COPY app/ /app/app/
# COPY . /app    

FROM python:3.8-slim
WORKDIR /app   

# Copy Python application files from build stage
COPY --from=build /app/app/ /app/app/

# Copy wheels and install
COPY --from=build /app/wheels /app/wheels
RUN pip install --no-cache-dir --find-links=/app/wheels/ --no-index /app/wheels/*.whl
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser
EXPOSE 5000
# main command that will run when the container starts is used to set the main command for the container.
ENTRYPOINT ["python", "app/app.py"]   



