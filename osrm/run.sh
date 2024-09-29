#!/bin/bash

docker compose run osrm-easy osrm-extract -p /opt/bicycle-easy.lua /data/osm-data.osm
docker compose run osrm-easy osrm-contract /data/osm-data.osrm

docker compose run osrm-medium osrm-extract -p /opt/bicycle-medium.lua /data/osm-data.osm
docker compose run osrm-medium osrm-contract /data/osm-data.osrm

docker compose run osrm-hard osrm-extract -p /opt/bicycle-hard.lua /data/osm-data.osm
docker compose run osrm-hard osrm-contract /data/osm-data.osrm
docker compose up -d