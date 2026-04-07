from app import db, app

with app.app_context():
    engine = db.engine
    dialect = getattr(engine.dialect, 'name', None)
    print('dialect =', dialect)
    print('DB engine:', engine)
