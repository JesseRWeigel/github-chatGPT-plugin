import json
import requests
import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__),
                      allow_origin="https://chat.openai.com")

# Keep track of todo's. Does not persist if Python session is restarted.
# _TODOS = {}

# @app.post("/todos/<string:username>")
# async def add_todo(username):
#     request = await quart.request.get_json(force=True)
#     if username not in _TODOS:
#         _TODOS[username] = []
#     _TODOS[username].append(request["todo"])
#     return quart.Response(response='OK', status=200)


@app.get("/repo/<string:username>/<string:repo_name>")
async def get_repo_data(username, repo_name):
    # Define the URL for the GitHub API endpoint
    url = f"https://api.github.com/repos/{username}/{repo_name}"

    # Make an HTTP GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        repo_data = response.json()
        return repo_data
    else:
        # Handle unsuccessful requests
        print(f"An error occurred: {response.status_code}")
        return None

# @app.delete("/todos/<string:username>")
# async def delete_todo(username):
#     request = await quart.request.get_json(force=True)
#     todo_idx = request["todo_idx"]
#     # fail silently, it's a simple plugin
#     if 0 <= todo_idx < len(_TODOS[username]):
#         _TODOS[username].pop(todo_idx)
#     return quart.Response(response='OK', status=200)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()
