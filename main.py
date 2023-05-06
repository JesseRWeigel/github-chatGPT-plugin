import httpx
import quart
import quart_cors
from quart import request, jsonify
import base64

app = quart_cors.cors(quart.Quart(__name__),
                      allow_origin="https://chat.openai.com")


@app.route("/repo/<string:username>/<string:repo_name>", methods=['GET'])
async def get_repo_data(username, repo_name):
    # Define the URL for the GitHub API endpoint
    url = f"https://api.github.com/repos/{username}/{repo_name}"

    # Make an HTTP GET request to the API endpoint
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        repo_data = response.json()
        return jsonify(repo_data)
    else:
        # Handle unsuccessful requests
        print(f"An error occurred: {response.status_code}")
        return None


@app.get("/file/<string:owner>/<string:repo>/<string:file_path>")
async def get_file_data(owner, repo, file_path):
    # Construct the API URL
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'

    # Make the GET request to the GitHub API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        file_data = response.json()

        # Decode the file content (which is base64 encoded)
        import base64
        file_content = base64.b64decode(file_data['content']).decode('utf-8')

        # Return the file content as a JSON response
        return jsonify({'content': file_content})
    else:
        # Return an error response with the status code
        return jsonify({'error': f'Error: {response.status_code}'}), response.status_code


@app.route("/list-files/<string:owner>/<string:repo>/<path:path>", methods=['GET'])
async def list_files(owner, repo, path=""):
    # Construct the API URL
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

    # Make the GET request to the GitHub API
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        contents = response.json()

        # Extract the names of the files and directories
        file_names = [item["name"] for item in contents]

        # Return the file names as a JSON response
        return jsonify({'files': file_names})
    else:
        # Return an error response with the status code
        return jsonify({'error': f'Error: {response.status_code}'}), response.status_code


@app.route("/logo.png", methods=['GET'])
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.route("/.well-known/ai-plugin.json", methods=['GET'])
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
