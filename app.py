from flask import Flask

# Create Flask App
app = Flask(__name__)

# Secret Key
app.secret_key = "Ajith@9751"

# Import Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.employee import employee_bp
from routes.department import department_bp
from routes.reports import reports_bp

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(department_bp)
app.register_blueprint(reports_bp)

# Run Application
if __name__ == "__main__":
    app.run(debug=True, port=8000)