import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask('flask')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_carro'

mybd = SQLAlchemy(app)



class tb_carro(mybd.Model):
    __tablename__ = 'tb_carro'
    id = mybd.Column(mybd.Integer, primary_key = True)
    nome = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.Integer)     

    def to_json(self):
        return{"id":self.id,"nome":self.nome, "modelo":self.modelo, "valor":self.valor, "cor":self.cor, "numero_Vendas":self.numero_vendas, "ano":self.ano}

@app.route("/bd_carro_all", methods=["GET"])
def selecionar_carros():
    carro_objetos = tb_carro.query.all()
    
    carro_json = [carro.to_json() for carro in  carro_objetos]
    return gera_response(200, "carros", carro_json)


@app.route("/bd_carro/<id>", methods=["GET"])
def seleciona_carro_id(id):
    carro_objetos = tb_carro.query.filter_by(id=id).first();
    carro_json = carro_objetos.to_json()
    return gera_response(200, "carros", carro_json)

@app.route("/bd_carro", methods=["POST"])
def criar_carro():
    body = request.get_json()
    
    try:
        carro = tb_carro(id=body["id"], nome=body["nome"], modelo=body["modelo"], valor=body["valor"], cor=body["cor"], numero_vendas=body["numero_vendas"], ano=body["ano"])
        
        mybd.session.add(carro)
        mybd.session.commit()
        return gera_response(201, "carros", carro.to_json(), "Criado com sucesso!")
        
    except Exception as e:
        print("Erro", e)
        return gera_response(400, "carros", {}, "Erro ao cadastrar!")
    

@app.route("/bd_carro/<id>", methods=["PUT"])
def atualizar_carro(id):
    carro_objetos = tb_carro.query.filter_by(id=id).first() 
    body = request.get_json()
    
    try: 
        for key, value in body.items():
            if hasattr(carro_objetos, key):
                setattr(carro_objetos, key, value)
                
        mybd.session.commit();
        
        return gera_response(200, "carros", carro_objetos.to_json(), "Atualizado com sucesso!")
    except Exception as e: 
        print("Erro", e)
        return gera_response(400, "carros", {}, "Erro ao atualizar")
    
@app.route("/bd_carro/<id>", methods=["DELETE"])
def deletar_carro(id):
    carro_objetos = tb_carro.query.filter_by(id = id).first()
    
    try:
        mybd.session.delete(carro_objetos)
        mybd.session.commit()
        
        return gera_response(200, "carros", carro_objetos.to_json(), "Deletado com sucesso!") 
    except Exception as e:
        print("Erro", e)
        return gera_response(400, "carros", {}, "Erro ao deletar")
    
def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo
    
    if(mensagem):
        body["mensagem"] = mensagem
        
    return Response(json.dumps(body), status=status, mimetype="application/json");

app.run(port=5000, host='localhost', debug=True)