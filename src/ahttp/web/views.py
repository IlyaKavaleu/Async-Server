import json

RESP_HTML = (
    "<DOCTYPE html>"
    "<html>"
    "<head><title>Home</title></head>"
    '<body bgcolor="white">'
    "<center><h1>Hello</h1></center>"
    "<hr><center>Custom python framework</center>"
    "</body>"
    "</html>"
)


async def home(request):
    if request.meth == 'GET':
        return RESP_HTML + '<p>Hello</p>'
    elif request.meth == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.body
            with open('save_POST_txt/file.txt', 'w') as file:
                file.write(data)
        else:
            with open('save_POST_json/data.json', 'w') as json_file:
                json.dump(json_data, json_file)
            return f"Data received and saved: {json_data}"
    else:
        return "Unsupported method"
