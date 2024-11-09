# import requests

# from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

# # Replace with the actual API endpoint URL
# url = "https://swapi.dev/api/people/"

# response = requests.get(url)

# if response.status_code == 200:
#     # Successful request
#     data = response.json()  # Assuming the API returns JSON data
#     print(data)
# else:
#     # Handle errors
#     print(f"Error: {response.status_code}")



#     @app.route("https://swapi.dev/api/people/", methods=["GET"])
# def find_person():
#     """locate information on star wars person.

#     Returns JSON like:
#         {people: [{id, name, films, homeworld, height, mass, skin_color, eye_color, birth_year, gender}]}
#     """

#     data = request.json

#     people = People(
#         name=data['name'],
#         mass=data['mass'],
#         skin_color=data['skin_color'],
#         eye_color=data['eye_color'],
#         birth_year=data['birth_year'],
#         gender=data['gender'],
#         films=data['films'],
#         # fix films connect
#         homeworld=data['homeworld'],
#         height=data['image'] or None)

#     db.session.add()
#     db.session.commit()

#     # return (jsonify(cupcake=cupcake.to_dict()), 201)
#     # fix return

#     @app.route('/home')
# def home():
#     """Show homepage"""

#     return render_template("home.html")

# @app.route('/signup')
# def home():
#     """Show homepage"""

#     return render_template("signup.html")


#   @app.route('/login')
# def login():
#     """Show login template"""

#     return render_template("login.html")


# @app.route('/search')
# def search():
#     """Show search results template"""

#     return render_template("search.html")

# @app.route('/signup', methods=["GET", "POST"])
# def signup():
#     """Handle user signup.

#     Create new user and add to DB. Redirect to home page.

#     If form not valid, present form.

#     If the there already is a user with that username: flash message
#     and re-present form.
#     """
#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]
#     form = UserAddForm()

#     if form.validate_on_submit():
#         try:
#             user = User.signup(
#                 username=form.username.data,
#                 password=form.password.data,
#                 email=form.email.data,
#                 image_url=form.image_url.data or User.image_url.default.arg,
#             )
#             db.session.commit()

#         except IntegrityError as e:
#             flash("Username already taken", 'danger')
#             return render_template('users/signup.html', form=form)

#         do_login(user)

#         return redirect("/")

#     else:
#         return render_template('users/signup.html', form=form)

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Endpoint to search for a character by name
@app.route('/search', methods=['GET'])
def search_character():
    name = request.args.get('name')
   
    if not name:
        return jsonify({"error": "Name parameter is required"}), 400
   
    try:
        # Use SWAPI's search endpoint to find character by name
        response = requests.get(f'https://swapi.dev/api/people/?search={name}')
        # find out what is not working on 126 
        print(response.json())
        response.raise_for_status()
       
        # Parse the response JSON
        search_results = response.json().get("results")
       
        if not search_results:
            return jsonify({"message": "No characters found"}), 404
       
        # Return details of the first matching character
        character_data = search_results[0]
        # character_name = search_results[0]
        return jsonify({
            "name": character_data.get("name"),
            "height": character_data.get("height"),
            "mass": character_data.get("mass"),
            "hair_color": character_data.get("hair_color"),
            "skin_color": character_data.get("skin_color"),
            "eye_color": character_data.get("eye_color"),
            "birth_year": character_data.get("birth_year"),
            "gender": character_data.get("gender"),
        })

    except requests.exceptions.RequestException:
        return jsonify({"error": "Could not perform search"}), 500


# Run the app
if __name__ == '__main__':
    app.run(debug=True)

