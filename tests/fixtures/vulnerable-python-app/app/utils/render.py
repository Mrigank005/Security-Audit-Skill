from flask import Blueprint, request
from markupsafe import Markup
from flask import render_template_string

render_bp = Blueprint('render', __name__)


# --- Render user-provided template ---
@render_bp.route('/render', methods=['POST'])
def render_page():
    template = request.form.get('template', '')
    name = request.form.get('name', 'Guest')

    return render_template_string(template, name=name)


# --- Preview greeting ---
@render_bp.route('/preview', methods=['GET'])
def preview_greeting():
    name = request.args.get('name', 'World')

    html = f"<h1>Hello {name}!</h1><p>Welcome to our platform.</p>"
    return render_template_string(html)
