from flask import render_template, redirect, url_for, flash, request, abort, session
from market import app, db
from market.models import Item, User
from market.forms import RegistrationForm, LoginForm, PurchaseForm, SellItemForm
from passlib.hash import pbkdf2_sha256
from flask_login import login_user, login_required, logout_user, current_user
from market.helper import is_safe_url


@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")


@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        item_id = request.form.get("purchased_item")
        if item_id:
            purchased_item = Item.query.filter_by(id=item_id).first()
            if purchased_item:
                if current_user.budget >= purchased_item.price:
                    purchased_item.assign_owner(current_user)
                    flash(f"You have successfully purchased our {purchased_item.name}", category="success")
                else:
                    flash("Insufficient balance", category="danger")
        else:
            item_id = request.form.get("sold_item")
            sold_item = Item.query.filter_by(id=item_id).first()
            if sold_item.owner == current_user.id:
                sold_item.sell_item(current_user)
                flash(f"You have successfully sold your {sold_item.name}", category="success")
            else:
                flash(f"You are unauthorized to sell this item", category="danger")

        return redirect(url_for("market_page"))

    items = Item.query.filter(Item.owner==None).all()
    owned_items = current_user.items

    return render_template("market.html", items=items, purchase_form=purchase_form,
                           owned_items=owned_items, selling_form=selling_form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email_address.data
        password = form.password.data
        password_hash = pbkdf2_sha256.hash(password)

        new_user = User(username=username,
                        email_address=email,
                        password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("User account created successfuly", "success")
        return redirect(url_for("market_page"))
    if form.errors:
        for err_msg in form.errors.values():
            flash(err_msg[0], category="danger")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if user and pbkdf2_sha256.verify(password, user.password):
            login_user(user)
            flash("You have successfully logged in.", category="success")
            if "next" in session:
                next_url = session.get("next")
                if not is_safe_url(next_url):
                    return abort(400)
                return redirect(next_url or url_for("market_page"))

        else:
            flash("Invalid username and password", category="danger")
            return redirect(url_for("login"))

    if login_form.errors:
        for err_msg in login_form.errors.values():
            flash(err_msg[0], category="danger")

    return render_template("login.html", form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", category="info")
    return redirect(url_for("index"))