FROM neo4j:latest
EXPOSE 7474
EXPOSE 7687

VOLUME $PWD/data:/data
VOLUME $PWD/plugins:/plugins

ENV NEO4JLABS_PLUGINS=[\"apoc\"]
ENV NEO4J_apoc_export_file_enabled=true
ENV NEO4J_apoc_import_file_enabled=true
ENV NEO4J_apoc_import_file-use__neo4j__config=true
ENV NEO4J_AUTH=none

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y python3.9 python3-pip
RUN apt-get install -y unzip
RUN apt-get install -y vim
RUN curl -s https://api.github.com/repos/jeremylong/DependencyCheck/releases/latest | grep browser_download_url | grep .zip\" | grep -v ant | cut -d '"' -f 4 | wget -qi -
RUN unzip dependency-check*.zip
RUN rm dependency-check*.zip
RUN pip3 install neo4j
RUN wget https://go.dev/dl/go1.17.7.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.17.7.linux-amd64.tar.gz
RUN rm go1.17.7.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/usr/local/go"

ADD config.in /var/lib/neo4j
ADD get_dc_data.py /var/lib/neo4j
ADD ingest_data_neo4j.py /var/lib/neo4j
ADD neosource.py /var/lib/neo4j
RUN go get github.com/Flaque/filet