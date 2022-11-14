import json
import html
import requests

def application(env, start_response):
    status = "200 OK"

    res_headers = [("Content-type", "audio/x-wav")]
    # print(env["REQUEST_METHOD"])
    length = int(env["CONTENT_LENGTH"])
    content = env["wsgi.input"].read(length)
    params = json.loads(content)

    if "type" in params:
        if 'ssml' in params["type"]:
            url = "http://172.18.0.146:9090/rest/v2/synthesize/ssml"

            headers = {
                "Content-Type": "application/ssml+xml",
                "X-Encoder": "wav/16000/16/1",
                "X-Rate": "1",
                "X-Voice": "rosana-highquality.voice",
                "X-Cache": "True"
            }

            text = params["text"].encode("utf-8", 'xmlcharrefreplace')

            req = requests.request("POST", url, data=text, headers=headers)
            start_response(status, res_headers)

            return req

        else:
            res_headers = [("Content-type", "text/html")]
            start_response("400 Bad Request", res_headers)
            return [b"Error 400 Malformed request"]

    url = "http://172.18.0.146:9090/rest/v2/synthesize"
    body = {
        "text": params['text'],
        "voice": "rosana-highquality.voice",
        "rate": 1,
        "encoder": "wav/16000/16/1"
    }
    req = requests.post(url, json=body)
    print(req)
    start_response(status, res_headers)

    return req


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    with make_server("", 8000, application) as httpd:
        print("Servidor de teste http rodando na porta 8000")
        print("\033[31m>>>>>Este é um servidor de teste e não deve ser usado em ambientes de produção!<<<<<")
        print(
            "\033[0mPara ambiente de produção consulte a documentação do seu servidor http para conexão com aplicativos WSGI")

        httpd.serve_forever()