# Streaming client

This is a separate project to start a command line client for sending and receiving messages to the server

## Usage

- Rename the shellscripts/batscripts from .txt to .sh/.bat and then execute the respective files

```shell script
$StreamingClient/shellscirpts>mv start_client.txt start_client.sh
$StreamingClient/shellscirpts>sh start_client.sh
```
- Another way of running the client can be as below
```shell script
$StreamingClient/pyscripts>python streaming_client.py 127.0.0.1 2222
```

## Assumptions
- It uses the same IP and PORT as the server was configured, which can be changed in the shellscripts according to our needs