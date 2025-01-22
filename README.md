
Build the Docker Image
```
docker build -t <image-name> .
```

Execute the container
```
docker run --rm -p <expose-port>:5000 <image-name>
```


Once the container is running, open your browser and go to:
```'localhost:<expose-port>'```
