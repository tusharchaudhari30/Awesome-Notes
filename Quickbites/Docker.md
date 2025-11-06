# Docker and Docker CLI - End-to-End Interview Notes

## Table of Contents

1. [Docker Fundamentals](#docker-fundamentals)
2. [Docker Architecture](#docker-architecture)
3. [Docker CLI Commands](#docker-cli-commands)
4. [Container Lifecycle Management](#container-lifecycle-management)
5. [Docker Images and Dockerfiles](#docker-images-and-dockerfiles)
6. [Docker Volumes and Storage](#docker-volumes-and-storage)
7. [Docker Networking](#docker-networking)
8. [Docker Compose](#docker-compose)
9. [Docker Security](#docker-security)
10. [Multi-stage Builds](#multi-stage-builds)
11. [Docker Swarm](#docker-swarm)
12. [Registry and Harbor](#registry-and-harbor)
13. [Monitoring and Debugging](#monitoring-and-debugging)
14. [Best Practices](#best-practices)
15. [Common Interview Questions](#common-interview-questions)

---

## Docker Fundamentals

### What is Docker?

Docker is an open-source containerization platform that enables developers to package applications with their dependencies into lightweight, portable containers. It provides application-level virtualization and allows consistent deployment across different environments.

### Key Benefits

- **Consistency**: Works the same across development, testing, and production
- **Portability**: Runs anywhere Docker is installed
- **Efficiency**: Lightweight compared to VMs
- **Scalability**: Easy horizontal scaling
- **Isolation**: Process and resource isolation

### Docker vs Virtual Machines

| Aspect         | Docker Containers     | Virtual Machines           |
| -------------- | --------------------- | -------------------------- |
| OS             | Shares host OS kernel | Each VM has full OS        |
| Resource Usage | Lightweight           | Heavy resource consumption |
| Startup Time   | Seconds               | Minutes                    |
| Isolation      | Process-level         | Hardware-level             |
| Portability    | Highly portable       | Less portable              |

---

## Docker Architecture

### Core Components

#### 1. Docker Client

- Command-line interface (CLI) tool
- Communicates with Docker daemon via REST API
- Sends build and run commands

#### 2. Docker Host (Docker Engine)

- **Docker Daemon**: Background service managing containers, images, networks
- **Docker API**: RESTful interface for daemon interaction
- **Runtime**: Container execution environment

#### 3. Docker Registry

- Stores and distributes Docker images
- **Docker Hub**: Public registry
- **Private registries**: Harbor, AWS ECR, Azure ACR

### Docker Engine Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Docker CLI    │───▶│  Docker Daemon   │
└─────────────────┘    │    (dockerd)     │
                       └──────────────────┘
                                │
                       ┌──────────────────┐
                       │   containerd     │
                       └──────────────────┘
                                │
                       ┌──────────────────┐
                       │       runc       │
                       └──────────────────┘
```

---

## Docker CLI Commands

### Essential Commands Cheatsheet

#### Image Management

```bash
# Build image from Dockerfile
docker build -t <image_name>:<tag> .
docker build -t app:v1.0 --no-cache .

# List images
docker images
docker image ls

# Remove images
docker rmi <image_id>
docker image rm <image_name>

# Pull/Push images
docker pull <image_name>:<tag>
docker push <image_name>:<tag>

# Image inspection
docker inspect <image_name>
docker history <image_name>
```

#### Container Management

```bash
# Run containers
docker run -it <image_name>              # Interactive
docker run -d <image_name>               # Detached
docker run -p 8080:80 <image_name>       # Port mapping
docker run --name myapp <image_name>     # Named container
docker run --rm <image_name>             # Auto-remove on exit
docker run -v /host:/container <image>   # Volume mount

# Container lifecycle
docker start <container_id>
docker stop <container_id>
docker restart <container_id>
docker pause <container_id>
docker unpause <container_id>
docker kill <container_id>

# List containers
docker ps                    # Running containers
docker ps -a                 # All containers
docker ps -q                 # Container IDs only

# Container inspection
docker inspect <container_id>
docker logs <container_id>
docker stats <container_id>
docker top <container_id>

# Execute commands in containers
docker exec -it <container_id> /bin/bash
docker exec <container_id> ls -la
docker attach <container_id>

# Copy files
docker cp file.txt <container_id>:/path/
docker cp <container_id>:/path/file.txt ./

# Remove containers
docker rm <container_id>
docker rm -f <container_id>  # Force remove
```

#### System Management

```bash
# System information
docker info
docker version
docker system df         # Disk usage
docker system events     # Real-time events

# Cleanup commands
docker system prune      # Remove unused data
docker container prune   # Remove stopped containers
docker image prune       # Remove dangling images
docker volume prune      # Remove unused volumes
docker network prune     # Remove unused networks

# Advanced cleanup
docker system prune -a   # Remove all unused data
docker builder prune     # Clear build cache
```

---

## Container Lifecycle Management

### Container States

Docker containers progress through five main states:

1. **Created**: Container created but not started
2. **Running**: Container is active and executing
3. **Paused**: Container processes temporarily suspended
4. **Stopped**: Container shut down gracefully
5. **Deleted**: Container removed from system

### State Transitions

```
┌─────────┐   docker run    ┌─────────┐
│ Created │ ──────────────▶ │ Running │
└─────────┘                 └─────────┘
     │                           │
     │ docker start              │ docker stop
     │                           ▼
     │                      ┌─────────┐
     └─────────────────────▶│ Stopped │
                            └─────────┘
                                 │
                            docker rm
                                 ▼
                            ┌─────────┐
                            │ Deleted │
                            └─────────┘
```

### Container Management Best Practices

```bash
# Health checks
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Resource limits
docker run --memory=512m --cpus=1.5 myapp

# Auto-restart policies
docker run --restart=unless-stopped myapp
docker run --restart=on-failure:3 myapp
```

---

## Docker Images and Dockerfiles

### Dockerfile Instructions

#### Essential Instructions

```dockerfile
FROM ubuntu:20.04                    # Base image
MAINTAINER author@email.com          # Author info (deprecated)
LABEL maintainer="author@email.com"  # Preferred metadata

WORKDIR /app                         # Set working directory
COPY . /app                          # Copy files
ADD http://example.com/file.tar.gz /app  # Copy/extract files

RUN apt-get update && \              # Execute commands
    apt-get install -y python3

ENV NODE_ENV=production              # Environment variables
ARG BUILD_VERSION=1.0               # Build-time variables

EXPOSE 8080                          # Document ports
VOLUME ["/data"]                     # Mount points

USER 1001                            # Run as user
CMD ["python3", "app.py"]            # Default command
ENTRYPOINT ["python3"]               # Fixed executable
```

#### ARG vs ENV Comparison

| Feature      | ARG                 | ENV                   |
| ------------ | ------------------- | --------------------- |
| Availability | Build-time only     | Build + Runtime       |
| Override     | `--build-arg`       | `-e` flag             |
| Final image  | Not included        | Persists              |
| Use case     | Build configuration | Runtime configuration |

### CMD vs ENTRYPOINT

| Aspect      | CMD                      | ENTRYPOINT              |
| ----------- | ------------------------ | ----------------------- |
| Override    | Easily overridden        | Requires `--entrypoint` |
| Purpose     | Default arguments        | Fixed executable        |
| Combination | Can work with ENTRYPOINT | Receives CMD as args    |

### Example Dockerfile

```dockerfile
FROM node:16-alpine AS builder

ARG NODE_ENV=production
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .
RUN npm run build

# Production stage
FROM node:16-alpine
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules

USER nextjs
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

ENTRYPOINT ["node"]
CMD ["dist/index.js"]
```

---

## Docker Volumes and Storage

### Storage Types

#### 1. Volumes (Recommended)

```bash
# Create and manage volumes
docker volume create mydata
docker volume ls
docker volume inspect mydata
docker volume rm mydata

# Use volumes
docker run -v mydata:/data alpine
docker run --mount source=mydata,target=/data alpine
```

#### 2. Bind Mounts

```bash
# Mount host directory
docker run -v /host/path:/container/path alpine
docker run --mount type=bind,source=/host/path,target=/container/path alpine
```

#### 3. tmpfs Mounts (Linux only)

```bash
# Temporary in-memory storage
docker run --tmpfs /tmp alpine
docker run --mount type=tmpfs,destination=/tmp alpine
```

### Volume vs Bind Mount Comparison

| Feature         | Volume            | Bind Mount        |
| --------------- | ----------------- | ----------------- |
| Docker managed  | ✅ Yes            | ❌ No             |
| Backup friendly | ✅ Yes            | ❌ No             |
| Performance     | ✅ Better         | ❌ Host dependent |
| Path control    | ❌ Docker decides | ✅ Full control   |
| Use case        | Production        | Development       |

### Volume Best Practices

```bash
# Named volumes with specific drivers
docker volume create --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.1,rw \
  --opt device=:/path/to/dir \
  nfs-volume

# Read-only volumes
docker run -v mydata:/data:ro alpine

# Volume cleanup
docker volume prune
```

---

## Docker Networking

### Network Types

#### 1. Bridge Networks (Default)

- Default network for containers on same host
- Provides isolation and DNS resolution
- Containers can communicate using container names

```bash
# Default bridge
docker run -d nginx

# Custom bridge
docker network create --driver bridge my-network
docker run --network=my-network nginx
```

#### 2. Host Networks

- Container shares host's network stack
- No network isolation
- Better performance, reduced security

```bash
docker run --network host nginx
```

#### 3. Overlay Networks

- Multi-host communication
- Used in Docker Swarm
- Encrypted by default

```bash
docker network create --driver overlay my-overlay
```

#### 4. None Network

- No networking
- Complete isolation

```bash
docker run --network none alpine
```

### Network Commands

```bash
# Network management
docker network create mynet
docker network ls
docker network inspect mynet
docker network rm mynet

# Connect/disconnect containers
docker network connect mynet container1
docker network disconnect mynet container1

# Container networking info
docker port container1
docker exec container1 ip addr show
```

### Network Comparison

| Type    | Scope          | Use Case             | Security           |
| ------- | -------------- | -------------------- | ------------------ |
| Bridge  | Single host    | Development, testing | Good isolation     |
| Host    | Single host    | Performance critical | No isolation       |
| Overlay | Multi-host     | Production clusters  | Encrypted          |
| None    | Container only | Security testing     | Complete isolation |

---

## Docker Compose

### docker-compose.yml Structure

```yaml
version: "3.8"

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8080:80"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - node_modules:/app/node_modules
    depends_on:
      - db
      - redis
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: redis:6-alpine
    networks:
      - app-network

volumes:
  postgres_data:
  node_modules:

networks:
  app-network:
    driver: bridge
```

### Docker Compose Commands

```bash
# Start services
docker-compose up
docker-compose up -d              # Detached mode
docker-compose up --build         # Rebuild images

# Stop services
docker-compose down
docker-compose down -v            # Remove volumes
docker-compose down --rmi all     # Remove images

# Service management
docker-compose start
docker-compose stop
docker-compose restart
docker-compose pause
docker-compose unpause

# Scaling services
docker-compose scale web=3

# Logs and monitoring
docker-compose logs
docker-compose logs -f web        # Follow logs
docker-compose ps
docker-compose top

# Execute commands
docker-compose exec web bash
docker-compose run web npm install
```

---

## Docker Security

### Image Security Best Practices

#### 1. Base Image Selection

```dockerfile
# Use official, minimal images
FROM alpine:3.14
FROM node:16-alpine
FROM distroless/java:11

# Avoid using 'latest' tag
FROM ubuntu:20.04  # Good
FROM ubuntu:latest # Avoid
```

#### 2. Non-root User

```dockerfile
# Create and use non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser

# Or use numeric IDs
USER 1001:1001
```

#### 3. Multi-stage Builds for Security

```dockerfile
# Build stage
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage - minimal
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
RUN rm -rf /var/cache/apk/*
```

### Container Security

```bash
# Run with limited capabilities
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx

# Read-only root filesystem
docker run --read-only nginx

# Security scanning
docker scan myimage:latest
```

### Resource Constraints

```bash
# Memory limits
docker run -m 512m nginx               # 512MB limit
docker run --memory=1g nginx          # 1GB limit
docker run --memory-reservation=256m nginx  # Soft limit

# CPU limits
docker run --cpus=1.5 nginx           # 1.5 CPU cores
docker run --cpu-shares=512 nginx     # Relative priority
docker run --cpuset-cpus=0,1 nginx    # Specific CPU cores

# Combined limits
docker run -m 512m --cpus=1 --pids-limit=100 nginx
```

---

## Multi-stage Builds

### Benefits

- **Smaller images**: Exclude build dependencies
- **Security**: Reduced attack surface
- **Efficiency**: Layer caching optimization
- **Flexibility**: Different stages for different purposes

### Multi-stage Example

```dockerfile
# Stage 1: Build application
FROM maven:3.8-openjdk-11 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Runtime
FROM openjdk:11-jre-slim
WORKDIR /app
COPY --from=builder /app/target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Advanced Multi-stage Patterns

```dockerfile
# Named stages
FROM node:16 AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:16 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Final stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=dependencies /app/node_modules ./node_modules
```

### Build Optimization

```bash
# Build specific stage
docker build --target builder -t myapp:build .

# Use BuildKit for advanced features
DOCKER_BUILDKIT=1 docker build -t myapp .

# Cache mount for dependencies
RUN --mount=type=cache,target=/root/.npm \
    npm install
```

---

## Docker Swarm

### Docker Swarm vs Kubernetes

| Feature          | Docker Swarm | Kubernetes     |
| ---------------- | ------------ | -------------- |
| Setup complexity | Simple       | Complex        |
| Learning curve   | Easy         | Steep          |
| Scalability      | Good         | Excellent      |
| Ecosystem        | Limited      | Extensive      |
| Load balancing   | Built-in     | Requires setup |
| Auto-scaling     | Manual       | Built-in       |

### Swarm Commands

```bash
# Initialize swarm
docker swarm init --advertise-addr <ip-address>

# Join worker nodes
docker swarm join --token <worker-token> <manager-ip>:2377

# Service management
docker service create --name web --replicas 3 -p 8080:80 nginx
docker service ls
docker service ps web
docker service scale web=5
docker service update --image nginx:latest web

# Stack deployment
docker stack deploy -c docker-compose.yml mystack
docker stack ls
docker stack services mystack
docker stack rm mystack

# Node management
docker node ls
docker node promote <node-id>
docker node demote <node-id>
```

### Swarm Service Example

```yaml
version: "3.8"
services:
  web:
    image: nginx:latest
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      placement:
        constraints:
          - node.role == worker
    ports:
      - "8080:80"
    networks:
      - overlay-net

networks:
  overlay-net:
    driver: overlay
    attachable: true
```

---

## Registry and Harbor

### Docker Hub vs Private Registry

| Feature     | Docker Hub          | Private Registry    |
| ----------- | ------------------- | ------------------- |
| Cost        | Free tier available | Infrastructure cost |
| Security    | Public by default   | Full control        |
| Compliance  | Limited             | Full compliance     |
| Integration | Easy                | Customizable        |
| Performance | Global CDN          | Local network       |

### Harbor Private Registry

Harbor is an enterprise-grade registry with:

- **Role-based access control (RBAC)**
- **Vulnerability scanning**
- **Image signing**
- **Audit logging**
- **Replication**

#### Harbor Installation

```bash
# Download Harbor
wget https://github.com/goharbor/harbor/releases/download/v2.5.0/harbor-offline-installer-v2.5.0.tgz
tar xvf harbor-offline-installer-v2.5.0.tgz
cd harbor

# Configure
cp harbor.yml.tmpl harbor.yml
# Edit harbor.yml with hostname and certificates

# Install
sudo ./install.sh
```

#### Using Harbor

```bash
# Login to Harbor
docker login harbor.example.com

# Tag and push image
docker tag nginx:latest harbor.example.com/library/nginx:latest
docker push harbor.example.com/library/nginx:latest

# Pull from Harbor
docker pull harbor.example.com/library/nginx:latest
```

---

## Monitoring and Debugging

### Health Checks

```dockerfile
# Health check in Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

```bash
# Health check at runtime
docker run -d --name web \
  --health-cmd="curl -f http://localhost/health || exit 1" \
  --health-interval=30s \
  --health-timeout=3s \
  --health-retries=3 \
  nginx
```

### Logging

```bash
# View logs
docker logs <container-id>
docker logs -f <container-id>           # Follow logs
docker logs --tail=50 <container-id>    # Last 50 lines
docker logs --since=1h <container-id>   # Last hour

# Logging drivers
docker run --log-driver=json-file nginx
docker run --log-driver=syslog nginx
docker run --log-driver=none nginx      # No logging
```

### Debugging Techniques

```bash
# Debug failing containers
docker run --rm -it --entrypoint=/bin/sh image_name
docker run --rm -it image_name /bin/bash

# Keep container running for debugging
docker run -d --name debug image_name sleep infinity
docker exec -it debug /bin/bash

# Debug with different entrypoint
docker run -it --entrypoint="" image_name /bin/bash

# Copy files for inspection
docker cp container_name:/app/logs ./logs
```

### Performance Monitoring

```bash
# Resource usage
docker stats                    # All containers
docker stats container_name     # Specific container

# System resource usage
docker system df               # Disk usage
docker system events           # Real-time events

# Container inspection
docker inspect container_name
docker top container_name      # Running processes
```

---

## Best Practices

### Dockerfile Best Practices

#### 1. Layer Optimization

```dockerfile
# Bad: Creates multiple layers
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y pip

# Good: Single layer
RUN apt-get update && \
    apt-get install -y python3 pip && \
    rm -rf /var/lib/apt/lists/*
```

#### 2. .dockerignore Usage

```gitignore
# .dockerignore
node_modules/
.git/
.gitignore
README.md
Dockerfile
.dockerignore
*.log
dist/
coverage/
.nyc_output/
```

#### 3. Build Context Optimization

```dockerfile
# Copy package files first for better caching
COPY package*.json ./
RUN npm install

# Copy source code after dependencies
COPY . .
```

### Security Best Practices

1. **Use official base images**
2. **Update regularly**
3. **Run as non-root user**
4. **Scan for vulnerabilities**
5. **Limit container capabilities**
6. **Use read-only filesystems when possible**
7. **Implement health checks**
8. **Monitor resource usage**

### Production Best Practices

1. **Use specific image tags**
2. **Implement proper logging**
3. **Set resource limits**
4. **Use multi-stage builds**
5. **Implement health checks**
6. **Use init systems for PID 1**
7. **Regular security updates**
8. **Monitor and alert**

---
