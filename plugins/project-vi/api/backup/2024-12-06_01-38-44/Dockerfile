# Build stage
FROM node:18 as development

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY postcss.config.js ./
COPY tailwind.config.js ./

# Install dependencies
RUN npm install

# Copy source code and public directory
COPY public/ ./public/
COPY src/ ./src/

# Build Tailwind CSS
RUN npm run build:css

# Set environment variable for React
ENV WATCHPACK_POLLING=true
ENV PORT=3000
ENV HOST=0.0.0.0

# Start the app in development mode
CMD ["npm", "start"]