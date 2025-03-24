from services.entities.materias import Materias
from services.materiamodel import MateriaModel
from services.configmodel import ConfigModel
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
import traceback
from datetime import datetime
from services.trazabilidadmodel import TrazabilidadModel
from services.entities.trazabilidad import Trazabilidad

materia = Blueprint('materia_blueprint', __name__)

@materia.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@materia.route('/')
@jwt_required()
def get_materias():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        materias = MateriaModel.get_materias()

        # Registrar trazabilidad
        trazabilidad = Trazabilidad(
            accion="Obtener todas las Materias",
            usuario=usuario,
            fecha=datetime.now(),
            modulo="Materias",
            nivel_alerta=1
        )
        TrazabilidadModel.add_trazabilidad(trazabilidad)

        return jsonify({"ok": True, "status": 200, "data": materias})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": str(ex)}), 500

@materia.route('/<id>')
@jwt_required()
def get_materia(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        materias = MateriaModel.get_materia(id)
        
        if materias is not None:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener Materia con id: {id}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Materias",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": materias})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "materia no encontrada"}}), 404
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}), 500

@materia.route('/inscribir/<cedula_estudiante>', methods=['GET'])
@jwt_required()
def get_materias_validas(cedula_estudiante: str):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')
        materias = MateriaModel.get_materias_validas(cedula_estudiante)
        
        if materias:
            # Convertimos cada objeto de la clase Materias en JSON
            materias_json = [materia.to_JSON_with_quantity() for materia in materias]
            
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Obtener materias válidas para inscripción del estudiante con cédula: {cedula_estudiante}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Materias",
                nivel_alerta=1
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": {"materias": materias_json}}), 200
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "No se pueden inscribir materias"}}), 404
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@materia.route('/add', methods=['POST'])
@jwt_required()
def add_materia():
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        cod = request.json['id']
        nombre = request.json['nombre']
        prelacion = request.json.get('prelacion', None)
        unidad_credito = request.json['unidad_credito']
        hp = request.json['hp']
        ht = request.json['ht']
        semestre = request.json['semestre']
        id_carrera = request.json['id_carrera']
        id_docente = request.json['id_docente']
        dia = request.json.get('dia', None)
        hora_inicio = request.json.get('hora_inicio', None)
        hora_fin = request.json.get('hora_fin', None)
        dia2 = request.json.get('dia2', None)
        hora_inicio2 = request.json.get('hora_inicio2', None)
        hora_fin2 = request.json.get('hora_fin2', None)
        maximo = request.json['maximo']
        ciclo = ConfigModel.get_configuracion("1").ciclo
        modalidad = request.json['modalidad']

        materia = Materias(cod, nombre, prelacion, unidad_credito, hp, ht, semestre, id_carrera, id_docente, dia, hora_inicio, hora_fin, dia2, hora_inicio2, hora_fin2, None, ciclo, modalidad, maximo)
        affected_rows = MateriaModel.add_materia(materia)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Añadir Materia con id: {cod}, nombre: {nombre}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Materias",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500
    except Exception as ex:
        print(ex)
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500

@materia.route('/update/<id>', methods=['PUT'])
@jwt_required()
def update_materia(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        nombre = request.json['nombre']
        prelacion = request.json['prelacion']
        unidad_credito = request.json['unidad_credito']
        hp = request.json['hp']
        ht = request.json['ht']
        semestre = request.json['semestre']
        id_carrera = request.json['id_carrera']
        id_docente = request.json['id_docente']
        dia = request.json.get('dia', None)
        hora_inicio = request.json.get('hora_inicio', None)
        hora_fin = request.json.get('hora_fin', None)
        modalidad = request.json['modalidad']
        dia2 = request.json.get('dia2', None)
        hora_inicio2 = request.json.get('hora_inicio2', None)
        hora_fin2 = request.json.get('hora_fin2', None)
        maximo = request.json['maximo']
        ciclo = ConfigModel.get_configuracion("1").ciclo

        materia = Materias(str(id), nombre, prelacion, unidad_credito, hp, ht, semestre, id_carrera, id_docente, dia, hora_inicio, hora_fin, dia2, hora_inicio2, hora_fin2, None, ciclo, modalidad, maximo)
        affected_rows = MateriaModel.update_materia(materia)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Actualizar Materia con id: {id}, nombre: {nombre}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Materias",
                nivel_alerta=2
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

@materia.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete_materia(id):
    try:
        claims = get_jwt()
        usuario = claims.get('nombre')

        materia = Materias(str(id))
        affected_rows = MateriaModel.delete_materia(materia)

        if affected_rows == 1:
            # Registrar trazabilidad
            trazabilidad = Trazabilidad(
                accion=f"Eliminar Materia con id: {id}",
                usuario=usuario,
                fecha=datetime.now(),
                modulo="Materias",
                nivel_alerta=3
            )
            TrazabilidadModel.add_trazabilidad(trazabilidad)

            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "materia no encontrada"}}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
