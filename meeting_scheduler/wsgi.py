from meeting_scheduler.src import app_factory

if __name__ == '__main__':
    app_factory.get_app().run(host="0.0.0.0", port=5000, debug=True)
