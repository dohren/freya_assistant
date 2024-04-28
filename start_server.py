from assistant import SkillCrawler, SkillWorker
from server import IntentFlaskServer

def main():
    flask_server = IntentFlaskServer()
    flask_server.run()

if __name__ == "__main__":
    main()