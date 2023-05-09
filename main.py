import httpx
import quart
import quart_cors
from quart import request, jsonify
import os

app = quart_cors.cors(quart.Quart(__name__),
                      allow_origin="https://chat.openai.com")


@app.route("/graphql", methods=['POST'])
async def graphql():
    # Get the JSON data from the request
    data = await request.get_json()

    # Get the query from the data
    query = data.get('query')

    # Define the URL for the GitHub GraphQL API endpoint
    url = "https://api.github.com/graphql"

    # Get the GitHub OAuth token from an environment variable
    token = os.getenv('GITHUB_TOKEN')

    # Define the headers for the request
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Define the payload for the request
    payload = {
        "query": query
    }

    # Make an HTTP POST request to the API endpoint
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        graphql_data = response.json()
        return jsonify(graphql_data)
    else:
        # Handle unsuccessful requests
        print(f"An error occurred: {response.status_code}")
        return None


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
