import os
from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
from supabase import create_client, Client
load_dotenv()
app = Flask(__name__)
CORS(app)

supabase: Client = create_client (
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

@app.route("/", methods=["GET"])
def health():
    return {"message": "Online"}

@app.get("/api/tools")
def get_tools():
    tools = supabase.from_("makerspace_tools").select("*").execute()
    return {"tools": tools.data}

@app.post("api/tools")
def add_tool():
    data = request.json
    tool_name = data.get("tool_name")
    category = data.get("category")
    daily_rental_rate = data.get("daily_rental_rate")

    if not all([tool_name, category, daily_rental_rate]):
        return {"error": "Missing required fields"}, 400 # bad request

    new_tool = {
        "tool_name": tool_name,
        "category": category,
        "daily_rental_rate": daily_rental_rate,
    }

    response = supabase.from_("makerspace_tools").insert(new_tool).execute()
    return {"message": "Tool added successfully", "data": response.data}, 201
          
            
if __name__ == "__main__":
    app.run(debug=True, port=5000)

