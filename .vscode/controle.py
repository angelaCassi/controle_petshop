from flask import request, jsonify, make_response
from banco import donos, animais, produtos, consultas

class Dono:
    def __init__(self, nome, contato, cpf, animais):
        self.nome = nome
        self.cpf = cpf
        self.contato = contato
        self.animais = animais=[]

    #Criar dono
    def CriarDono(self, novo_dono):
        novo_dono = request.get_json()
        donos.append(novo_dono)
        return make_response(jsonify(
            Aceito='Novo Dono Criado!',
            Lista=donos
            )
        )
    #Ver dono
    def VerDono():
        return make_response(jsonify(
            Aceito='Lista de Donos:',
            Lista=donos
            )
        )
    #Modificar dono
    def EditarDonoCpf(self, dono_modificado, cpf):
        dono_modificado = request.get_json()
        for indice, dono in enumerate(donos):
            if dono.get('cpf') == cpf:
                dono[indice].update(dono_modificado)
        return make_response(jsonify(
            Aceito='Dono modificado!',
            Lista=donos
            )
        ) 
    #Excluir dono
    def ExcluirDono(self, cpf):
        for indice, dono in enumerate(donos):
            if dono.get('cpf') == cpf:
                del donos[indice]
        return make_response(jsonify(
            Aceito='Dono excluído!',
            Lista=donos
            )
        )
    
    #Adicionar animal ao dono
    def AdicionarAnimal(self, especie, nome):
        novo_animal = Animal(especie=especie, nome=nome, dono=self.nome)
        self.animais.append(novo_animal)
        animais.append(novo_animal) 
        return make_response(jsonify(
            Aceito='Animal adicionado!',
            Lista=animais
            )
        )
    
    #Ver todos os animais do dono
    def VerAnimais(self):
        return jsonify({'Animais do Dono': [animal.__dict__ for animal in self.animais]})

    #Excluir animal pelo ID
    def ExcluirAnimal(self, id):
        for indice, animal in enumerate(self.animais):
            if animal.id == id:
                del self.animais[indice]
                break
        return jsonify({'Aceito': 'Animal excluído!', 'Animais restantes': [animal.__dict__ for animal in self.animais]})

# Classe Animal
class Animal:
    def __init__(self, id, especie, nome, dono):
        self.id = id
        self.especie = especie
        self.nome = nome
        self.dono = dono

# Classe Consulta
class Consulta:
    def __init__(self, dono, animal, data):
        self.animal = animal
        self.data = data
        self.dono = dono

    #AgendarConsulta()
    def AgendarConsulta(self, dono, animal, data_hora):
        if animal in self.consultas:
            return make_response(jsonify(
            Aceito='Consulta já agendada!',
            Lista=self.consultas
            )
        )

        else:
            self.consultas[animal] = data_hora
            return make_response(jsonify(
            Aceito='Nova consulta agendada!',
            Lista=self.consultas
            )
        )
    #RemarcarConsulta()
    def RemarcarConsulta(self, animal, nova_data_hora):
        if animal in self.consulta:
            antiga_data = self.consultas[animal]
            self.consultas[animal] = nova_data_hora
            return make_response(jsonify(
            Aceito='Consulta remarcada!',
            Lista=self.consultas
            )
        )
    #ExlcuirConsulta()
    def ExcluirConsulta(self, animal):
        if animal in self.consultas:
            del self.consultas[animal]
            return make_response(jsonify(
            Aceito='Consulta excluída!',
            Lista=self.consultas
            )
        )

class Produtos:
    def __init__(self, codigo, preco, nome):
        self.codigo = codigo
        self.preco = preco
        self.nome = nome
    
    #VerProdutos
    def VerProdutos(self):
        make_response(jsonify(
            Aceito='Lista de Produtos:',
            Lista=produtos
            )
        )

    #AdicionarProduto
    def AdicionarProduto(self, novo_produto):
        novo_produto = request.get_json()
        produtos.append(novo_produto)
        return jsonify(produtos)
    
    #ExcluirProdutoPorCodigo
    def ExcluirAnimal(self, codigo):
        for indice, produto in enumerate(produtos):
            if produto.get('codigo') == codigo:
                del produtos[indice]
        make_response(jsonify(
            Aceito='Produto excluído!',
            Lista=produtos
            )
        )
