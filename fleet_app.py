from app import create_app

app = create_app("FLEET")

if __name__ == "__main__":
    app.logger.info("Starting Fleet Management System...")
    app.run(host="0.0.0.0", port=app.port, debug=True)
