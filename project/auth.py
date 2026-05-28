# ============================================================
# SECTION B: AUTHENTICATION & SECURITY (FULL VERSION)
# Created by: Vinod
# ============================================================
#
# This file contains:
# - Login functions for Owner and Tourist (with hashed password support)
# - Registration function
# - Custom decorators for role-based access control
# - Helper functions
#
# These work with the existing raw session system.
# ============================================================

from functools import wraps
from flask import session, redirect, url_for, flash
from project import models
from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
# LOGIN FUNCTIONS
# ============================================================

def login_owner(username, password):
    """
    SECTION B - Vinod
    Login for Owner/Seller with hashed password verification.
    """
    conn = models.getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM owners WHERE username = ?", (username,))
    owner = cursor.fetchone()
    print("=== DEBUG OWNER LOGIN ===")
    print("Owner found:", owner)
    conn.close()

    if owner is None:
        flash("Invalid username or password", "danger")
        return redirect(url_for("index"))

    if not check_password_hash(owner["password"], password):
        flash("Invalid username or password", "danger")
        return redirect(url_for("index"))

    # Set session
    session["owner_id"] = owner["owner_id"]
    session["role"] = "seller"
    session["username"] = owner["username"]

    flash(f"Welcome back, {owner['username']}!", "success")
    return redirect(url_for("index"))


def login_tourist(username, password):
    """
    SECTION B - Vinod
    Login for Tourist/Buyer with hashed password verification.
    """
    conn = models.getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tourists WHERE username = ?", (username,))
    tourist = cursor.fetchone()
    conn.close()

    if tourist is None:
        flash("Invalid username or password", "danger")
        return redirect(url_for("index"))

    if not check_password_hash(tourist["password"], password):
        flash("Invalid username or password", "danger")
        return redirect(url_for("index"))

    # Set session
    session["tourist_id"] = tourist["tourist_id"]
    session["role"] = "buyer"
    session["username"] = tourist["username"]

    flash(f"Welcome back, {tourist['username']}!", "success")
    return redirect(url_for("index"))


# ============================================================
# REGISTRATION
# ============================================================

def register_user(username, password, email, role):
    """
    SECTION B - Vinod
    Register new user as 'seller' or 'buyer'.
    Returns (success: bool, message: str)
    """
    if not username or not password or not email or role not in ["seller", "buyer"]:
        return False, "All fields are required and role must be seller or buyer."

    hashed_pw = generate_password_hash(password, method="pbkdf2:sha256")

    try:
        conn = models.getConnection()
        cursor = conn.cursor()

        if role == "seller":
            cursor.execute(
                "SELECT owner_id FROM owners WHERE username = ? OR email = ?", 
                (username, email)
            )
            if cursor.fetchone():
                conn.close()
                return False, "Username or email already exists."

            cursor.execute(
                "INSERT INTO owners (username, password, email) VALUES (?, ?, ?)",
                (username, hashed_pw, email)
            )

        elif role == "buyer":
            cursor.execute(
                "SELECT tourist_id FROM tourists WHERE username = ? OR email = ?", 
                (username, email)
            )
            if cursor.fetchone():
                conn.close()
                return False, "Username or email already exists."

            cursor.execute(
                "INSERT INTO tourists (username, password, email) VALUES (?, ?, ?)",
                (username, hashed_pw, email)
            )

        conn.commit()
        conn.close()
        return True, f"{role.capitalize()} account created successfully!"

    except Exception as e:
        return False, f"Registration failed: {str(e)}"


# ============================================================
# LOGOUT
# ============================================================

def logout_user():
    """SECTION B - Vinod"""
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("index"))


# ============================================================
# CUSTOM DECORATORS
# ============================================================

def login_required(f):
    """SECTION B - Vinod"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "owner_id" not in session and "tourist_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


def seller_required(f):
    """SECTION B - Vinod"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "seller":
            flash("Only sellers can access this page.", "warning")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


def buyer_required(f):
    """SECTION B - Vinod"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "buyer":
            flash("Only buyers can access this page.", "warning")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_current_user():
    """SECTION B - Vinod"""
    if "owner_id" in session:
        return {
            "owner_id": session.get("owner_id"),
            "role": session.get("role"),
            "username": session.get("username")
        }
    if "tourist_id" in session:
        return {
            "tourist_id": session.get("tourist_id"),
            "role": session.get("role"),
            "username": session.get("username")
        }
    return None


def is_seller():
    """SECTION B - Vinod"""
    return session.get("role") == "seller"


def is_buyer():
    """SECTION B - Vinod"""
    return session.get("role") == "buyer"


def is_logged_in():
    """SECTION B - Vinod"""
    return "owner_id" in session or "tourist_id" in session