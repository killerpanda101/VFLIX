import os
from website import app

if __name__ == '__main__':
	# Debug mode exposes an interactive debugger; enable only locally via FLASK_DEBUG=1
	app.run(debug=os.environ.get('FLASK_DEBUG') == '1')