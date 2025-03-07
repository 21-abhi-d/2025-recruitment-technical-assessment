from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {} # make dict

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	recipeName = recipeName.replace("-", " ").replace("_", " ") # remove whitespace and hyphen
	recipeName = re.sub(r"[^a-zA-Z\s]", "", recipeName) # remove special chars
	recipeName = recipeName.title() # cap every word
	recipeName = re.sub(r"\s+", " ", recipeName) # Condense whitspc's
	return recipeName

# Tests:
# print(parse_handwriting("meatball"))
# print(parse_handwriting("Skibidi_spaghetti"))
# print(parse_handwriting("alpHa alFRedo"))  


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	data = request.get_json()
	
	# type/name condition none check
	if "type" not in data or "name" not in data:
		return jsonify({"error": "Missing required fields"}), 400

	entry_type = data["type"]
	entry_name = data["name"]
  
	# ensure no dupe names in cb
	if entry_name in cookbook:
		return jsonify({"error": "Entry name must be unique"}), 400

	# ensure type is valid
	if entry_type != "recipe" and entry_type != "ingredient":
		return jsonify({"error": "Entry type must be either recipe or ingredient"}), 400
 	
  	# recipe validation - Can't comment below this due to indentation issues :(
	if entry_type == "recipe":
		if "requiredItems" not in data:
			return jsonify({"error": "Recipe must have requiredItems"}), 400

		required_items = data["requiredItems"]
		seen_items = set()

		for item in required_items:
			if "name" not in item or "quantity" not in item:
				return jsonify({"error": "Required items must have name/quantity"}), 400
			
			if item["name"] in seen_items:	
				return jsonify({"error": "Duplicate names in requiredItems"}), 400
			
			seen_items.add(item["name"])

  	# ingredient validation - Can't comment below this due to indentation issues :(
	if entry_type == "ingredient":
		if "cookTime" not in data or data["cookTime"] < 0 or not isinstance(data["cookTime"], int):
			return jsonify({"error": "Invalid cookTime, must be integer greater than -1"}), 400

	# add entry into cb
	cookbook[entry_name] = data
 
	print("Current cookbook: ", cookbook)

	return "", 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
