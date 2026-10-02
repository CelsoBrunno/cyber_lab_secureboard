from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(
        email="admin@secureboard.local",
        password_hash=generate_password_hash("TroqueEssaSenha!2026"),
        role="admin"
    )
    aluno = User(
        email="aluno@secureboard.local",
        password_hash=generate_password_hash("TroqueEssaSenha!2026"),
        role="user"
    )

    db.session.add_all([admin, aluno])
    db.session.commit()
    print("Banco criado.")
    print("admin@secureboard.local / TroqueEssaSenha!2026")
    print("aluno@secureboard.local / TroqueEssaSenha!2026")
