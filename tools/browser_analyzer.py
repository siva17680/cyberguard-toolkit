from flask import Blueprint, render_template, request

browser_analyzer_bp = Blueprint('browser_analyzer', __name__)

@browser_analyzer_bp.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr
    return render_template('tools/browser_analyzer.html', ua=user_agent, ip=ip_address)