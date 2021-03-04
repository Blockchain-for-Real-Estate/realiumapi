FROM postgres:12-alpine
ADD scripts/01_init.sql /docker-entrypoint-initdb.docker
RUN chmod a+r /docker-entrypoint-initdb.d*
EXPOSE 5432