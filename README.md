## Usage

from asyncio import protocols


1. Build the app

```bash
$ docker-compose build
```

2. Bring the app up
```bash
$ docker-compose up
```

3. Browse to localhost:3001 to see the app in action.

## Running Tests
1. After app is running run
```bash
$  docker exec -it warehouse_warehouse_1 bash
```

2. Inside the container run
```bash
$  pytest test/*.py
```

## Future Improvements
- Add more test cases
- Optimize Dockerfile
- Cythonize python code for production deployment
- Improve logging

