from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipe.db"
db.init_app(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


@app.context_processor
def inject_year():
    year = datetime.today().year
    return dict(year=year)


@app.route("/")
def home():
    all_recipes = db.session.query(Recipe).all()
    recipe_id = request.args.get("id")
    return render_template("index.html", all_recipes=all_recipes, recipe_id=recipe_id)


@app.route("/recipe/<int:id>")
def recipe_detail(id):
    recipe = db.get_or_404(Recipe, id)
    return render_template("recipe.html", recipe=recipe)


@app.route("/recipe/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        new_recipe = Recipe(title=request.form["title"],
                            ingredients=request.form["ingredients"],
                            instructions=request.form["instructions"])
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit_recipe(id):
    recipe_to_edit = db.get_or_404(Recipe, id)
    if request.method == "POST":
        recipe_to_edit.title = request.form["title"]
        recipe_to_edit.ingredients = request.form["ingredients"]
        recipe_to_edit.instructions = request.form["instructions"]
        db.session.commit()
        return redirect(url_for("recipe_detail", id=id))
    return render_template("edit.html", recipe_to_edit=recipe_to_edit)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    recipe_to_delete = db.get_or_404(Recipe, id)
    db.session.delete(recipe_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
