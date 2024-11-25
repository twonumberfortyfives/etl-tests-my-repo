FROM python:3.11-slim

# Environment configurations
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy requirements
COPY requirements.txt .

COPY pandas-2.2.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl .

# Install from wheels
RUN pip install --no-cache-dir pandas-2.2.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl


# Install base dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining application code
COPY . .

CMD ["python", "-m", "unittest"]
