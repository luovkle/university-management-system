FROM node:19-alpine3.15 AS builder
WORKDIR /app
COPY ["./app/package.json", "/app/"]
RUN npm install
COPY [ \
  "./app/index.html", \
  "./app/tsconfig.json", \
  "./app/tsconfig.node.json", \
  "./app/vite.config.ts", \
  "/app/" \
]
ADD ["./app/public", "/app/public/"]
ADD ["./app/src", "/app/src/"]
RUN npm run build

FROM nginx:1.23-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
