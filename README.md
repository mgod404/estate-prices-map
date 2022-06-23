
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

2. In **ecommerce/frontend/src/** create file named "CONFIG.tsx" with the code:
```typescript
export const HOST_URL = '' 
export const API_URL = `${HOST_URL}/api/v1`
```
HOST_URL is the url your backend will be available on. If the project is run locally,
the HOST_URL will be http://127.0.0.1:8000

3. Run 
```bash
  docker-compose up
```
