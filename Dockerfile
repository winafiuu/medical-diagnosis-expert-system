# Use Node.js as the base image
FROM node:20-slim

# Install Python 3 and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency definitions
COPY backend/package*.json ./backend/
COPY ai-engine/requirements.txt ./ai-engine/

# Install Node.js dependencies
RUN cd backend && npm install --production

# Create and activate Python virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies in the virtual environment
RUN pip install --upgrade pip && \
    pip install -r ai-engine/requirements.txt

# Copy the rest of the application code
COPY backend ./backend
COPY ai-engine ./ai-engine

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
# Python is available via the venv (activated by PATH modification above)
ENV PYTHON_ENGINE_PATH=/app/ai-engine/main.py

# Expose the API port
EXPOSE 3000

# Start the application
CMD ["node", "backend/src/index.js"]
