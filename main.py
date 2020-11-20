from app import app, db
import views

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(host='0.0.0.0')