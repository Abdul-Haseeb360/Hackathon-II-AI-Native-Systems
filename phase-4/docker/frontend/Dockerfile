# Multi-stage build for Next.js frontend
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci  # Install all dependencies including dev dependencies for building

COPY . .
RUN npm run build

# Stage 2: Production server
FROM node:20-alpine AS runner

WORKDIR /app

# Install dumb-init to handle signals properly
RUN apk add --no-cache dumb-init

# Copy package.json to install dependencies
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy the built application from the builder stage
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

EXPOSE 3000

# Add dumb-init to handle graceful shutdowns
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]