sudo docker build -t edge_bundle .
sudo docker run -d -p 8002:8002 --name edge_budle --memory 128M --cpus 1 edge_bundle
