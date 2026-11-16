import logging

def run_app():
    logging.basicConfig(
        filename="logs/application.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Application started successfully")

if __name__ == "__main__":
    run_app()

