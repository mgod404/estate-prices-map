
## Run the project

1. create docker-compose.override.yml file in the root folder of the project. Paste code below

```yml
services:
  web:
    environment:
      - HOSTNAME=127.0.0.1:8000
      - GOOGLE_API=
      - SECRET_KEY=
      - DEBUG=
  scraper:
    environment:
      - GOOGLE_API=
      - API_URL=

```

For **GOOGLE_API** you'll need a Google Geocoding API key, more information here: https://developers.google.com/maps/documentation/geocoding/start

2. Run 
```bash
  docker-compose up
```
