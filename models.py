from database import db

class Inventario(db.Model):
    __tablename__ = "inventario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    quantidade = db.Column(db.Integer)
    localizacao = db.Column(db.String(50))
    
    def __init__(self, nome, quantidade, localizacao):
        self.nome = nome
        self.quantidade = quantidade
        self.localizacao = localizacao

    def __repr__(self):
        return "<Inventário {}>".format(self.nome)