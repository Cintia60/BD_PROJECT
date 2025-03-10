
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime
app = Flask(__name__)

SECRET_KEY = 'my_secret_key'
# Função para criar uma conexão com o banco de dados
def db_connection():
    conn = psycopg2.connect(
        user='postgres',     # Nome do usuário do PostgreSQL
        password='postgres',  # Senha do usuário do PostgreSQL
        host='127.0.0.1',    # Host onde o PostgreSQL está sendo executado
        port='5432',         # Porta padrão do PostgreSQL
        database='SGH' # Nome da base de dados que acabou de criar
    )
    return conn
@app.route('/dbproj/register/patient', methods=['POST'])
def register_patient():
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Extrair dados da solicitação
        data = request.json
        cc = data['cc']
        nif = data['nif']
        nome = data['nome']
        data_de_nascimento = data['data_de_nascimento']
        morada = data.get('morada')  # Use .get() para lidar com campos opcionais
        telefone = data.get('telefone')
        genero = data.get('genero')
        mail = data['mail']
        senha = data['senha']
        contato_emergencia = data.get('contato_emergencia')
        nome_ce = data.get('nome_ce')
        grau_de_parentesco = data.get('grau_de_parentesco')
        grupo_sanguineo = data.get('grupo_sanguineo')

        # Inserir dados na tabela pessoa
        cursor.execute("""
            INSERT INTO pessoa (cc, nif, nome, data_de_nascimento, morada, telefone, genero, mail, senha)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING cc
        """, (cc, nif, nome, data_de_nascimento, morada, telefone, genero, mail, senha))
        pessoa_cc = cursor.fetchone()[0]

        # Inserir dados na tabela paciente
        cursor.execute("""
            INSERT INTO paciente (contacto_emergencia, nome_ce, grau_de_parentesco, grupo_sanguineo, pessoa_cc)
            VALUES (%s, %s, %s, %s, %s)
        """, (contato_emergencia, nome_ce, grau_de_parentesco, grupo_sanguineo, pessoa_cc))

        # Commit da transação
        conn.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Retornar resposta de sucesso
        return jsonify({'status': 'success', 'message': 'Patient registered successfully'}), 200
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500



@app.route('/dbproj/register/doctor', methods=['POST'])
def register_doctor():
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Extrair dados da solicitação
        data = request.json
        cc = data['cc']
        nif = data['nif']
        nome = data['nome']
        data_de_nascimento = data['data_de_nascimento']
        morada = data.get('morada')  # Use .get() para lidar com campos opcionais
        telefone = data.get('telefone')
        genero = data.get('genero')
        mail = data['mail']
        senha = data['senha']
        numero_de_licensa = data['numero_de_licensa']
        salario = data['salario']
        premios = data.get('premios')
        funcao = data['funcao']
        especializacoes = data['especializacoes']  # Lista de especializações do médico

        # Inserir dados na tabela pessoa
        cursor.execute("""
            INSERT INTO pessoa (cc, nif, nome, data_de_nascimento, morada, telefone, genero, mail, senha)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING cc
        """, (cc, nif, nome, data_de_nascimento, morada, telefone, genero, mail, senha))
        pessoa_cc = cursor.fetchone()[0]

        # Inserir dados na tabela empregado
        cursor.execute("""
            INSERT INTO empregado (numero_de_empregado, data_de_entreada, data_de_fim_de_contracto, salario, premios, funcao, pessoa_cc)
            VALUES (%s, current_date, '9999-12-31', %s, %s, %s, %s)
            RETURNING pessoa_cc
        """, (cc, salario, premios, funcao, pessoa_cc))
        pessoa_cc_empregado = cursor.fetchone()[0]

        # Inserir dados na tabela médico
        cursor.execute("""
            INSERT INTO medico (numero_de_licensa, medical_staff_empregado_pessoa_cc)
            VALUES (%s, %s)
        """, (numero_de_licensa, pessoa_cc_empregado))

        # Inserir dados na tabela especializacao para cada especializacao do médico
        for especializacao in especializacoes:
            cursor.execute("""
                INSERT INTO especializacao (especializacao)
                VALUES (%s)
                ON CONFLICT (especializacao) DO NOTHING
            """, (especializacao,))

            # Obter o ID da especializacao inserida
            cursor.execute("""
                SELECT id FROM especializacao WHERE especializacao = %s
            """, (especializacao,))
            especializacao_id = cursor.fetchone()[0]

            # Relacionar o médico com a especializacao
            cursor.execute("""
                INSERT INTO medico_especializacao (medico_medical_staff_empregado_pessoa_cc, especializacao_id)
                VALUES (%s, %s)
            """, (pessoa_cc_empregado, especializacao_id))

        # Commit da transação
        conn.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Retornar resposta de sucesso
        return jsonify({'status': 'success', 'message': 'Doctor registered successfully'}), 200
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/dbproj/register/nurse', methods=['POST'])
def register_nurse():
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Extrair dados da solicitação
        data = request.json
        cc = data['cc']
        nif = data['nif']
        nome = data['nome']
        data_de_nascimento = data['data_de_nascimento']
        morada = data.get('morada')  # Use .get() para lidar com campos opcionais
        telefone = data.get('telefone')
        genero = data.get('genero')
        mail = data['mail']
        senha = data['senha']
        categoria = data['categoria']  # Categoria de enfermeiro (por exemplo: Enfermeiro Chefe, Enfermeiro de Clínica Geral, etc.)

        # Inserir dados na tabela pessoa
        cursor.execute("""
            INSERT INTO pessoa (cc, nif, nome, data_de_nascimento, morada, telefone, genero, mail, senha)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING cc
        """, (cc, nif, nome, data_de_nascimento, morada, telefone, genero, mail, senha))
        pessoa_cc = cursor.fetchone()[0]

        # Inserir dados na tabela empregado com valores padrão para salario, premios e funcao
        cursor.execute("""
            INSERT INTO empregado (numero_de_empregado, data_de_entreada, data_de_fim_de_contracto, salario, premios, funcao, pessoa_cc)
            VALUES (%s, current_date, '9999-12-31', %s, %s, %s, %s)
            RETURNING pessoa_cc
        """, (cc, 0, 0, 'Enfermeiro', pessoa_cc))  # Defina salário e prêmios como 0 e função como 'Enfermeiro' por padrão
        pessoa_cc_empregado = cursor.fetchone()[0]

        # Inserir dados na tabela enfermeiro
        cursor.execute("""
            INSERT INTO enfermeiro (categoria, medical_staff_empregado_pessoa_cc)
            VALUES (%s, %s)
        """, (categoria, pessoa_cc_empregado))

        # Commit da transação
        conn.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Retornar resposta de sucesso
        return jsonify({'status': 'success', 'message': 'Nurse registered successfully'}), 200
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/dbproj/add/assistant', methods=['POST'])
def add_assistant():
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Extrair dados da solicitação
        data = request.json
        cc = data['cc']
        nif = data['nif']
        nome = data['nome']
        data_de_nascimento = data['data_de_nascimento']
        morada = data.get('morada')  # Use .get() para lidar com campos opcionais
        telefone = data.get('telefone')
        genero = data.get('genero')
        mail = data['mail']
        senha = data['senha']

        # Inserir dados na tabela pessoa
        cursor.execute("""
            INSERT INTO pessoa (cc, nif, nome, data_de_nascimento, morada, telefone, genero, mail, senha)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING cc
        """, (cc, nif, nome, data_de_nascimento, morada, telefone, genero, mail, senha))
        pessoa_cc = cursor.fetchone()[0]

        # Inserir dados na tabela empregado com valores padrão para salario, premios e funcao
        cursor.execute("""
            INSERT INTO empregado (numero_de_empregado, data_de_entreada, data_de_fim_de_contracto, salario, premios, funcao, pessoa_cc)
            VALUES (%s, current_date, '9999-12-31', %s, %s, %s, %s)
            RETURNING pessoa_cc
        """, (cc, 0, 0, 'Assistente Médico', pessoa_cc))  # Defina salário e prêmios como 0 e função como 'Assistente Médico' por padrão
        pessoa_cc_empregado = cursor.fetchone()[0]

        # Inserir dados na tabela assistente
        cursor.execute("""
            INSERT INTO assistente (medical_staff_empregado_pessoa_cc)
            VALUES (%s)
        """, (pessoa_cc_empregado,))

        # Commit da transação
        conn.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Retornar resposta de sucesso
        return jsonify({'status': 'success', 'message': 'Assistant added successfully'}), 200
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/dbproj/user', methods=['PUT'])
def user_authentication():
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Extrair dados da solicitação
        data = request.json
        nome = data['nome']
        senha = data['senha']

        # Verificar as credenciais do usuário no banco de dados
        cursor.execute("SELECT cc FROM pessoa WHERE nome = %s AND senha = %s", (nome, senha))
        user_id = cursor.fetchone()

        if user_id:
            # Gerar o token JWT
            token = jwt.encode({'user_id': user_id[0],'nome': nome, "user_type": 'paciente'}, SECRET_KEY, algorithm='HS256')

            # Fechar o cursor e a conexão
            cursor.close()
            conn.close()

            # Retornar o token JWT como resposta
            return jsonify({'status': 200, 'errors': None, 'results': token})
        else:
            # Fechar o cursor e a conexão
            cursor.close()
            conn.close()

            # Retornar erro se as credenciais forem inválidas
            return jsonify({'status': 401, 'errors': 'Invalid username or password', 'results': None})
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()
        return jsonify({'status': 500, 'errors': str(e), 'results': None})


# Endpoint para agendar uma consulta
@app.route('/dbproj/appointment', methods=['POST'])
def schedule_appointment():
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Extrair dados da solicitação
        data = request.json
        medico_medical_staff_empregado_pessoa_cc = data['medico_medical_staff_empregado_pessoa_cc']
        assistente_medical_staff_empregado_pessoa_cc = data['assistente_medical_staff_empregado_pessoa_cc']
        paciente_pessoa_cc = data['paciente_pessoa_cc']
        data_consulta = data['data_consulta']

        # Verificar se id_fatura é fornecido na solicitação
        id_fatura = data.get('id_fatura')

        # Verificar o tipo de usuário usando o token JWT
        auth_token = request.headers.get('Authorization')
        decoded_token = jwt.decode(auth_token.encode('utf-8'), SECRET_KEY, algorithms=['HS256'])
        user_type = decoded_token.get('user_type')

        # Verificar se o usuário é assistente
        if user_type != 'assistente':
            return jsonify({'status': 'error', 'message': 'Only assistants can schedule appointments'}), 403

        # Verificar se o assistente existe
        cursor.execute("SELECT * FROM assistente WHERE medical_staff_empregado_pessoa_cc = %s", (assistente_medical_staff_empregado_pessoa_cc,))
        assistente = cursor.fetchone()
        if not assistente:
            return jsonify({'status': 'error', 'message': 'Assistant not found'}), 404

        # Verificar se o médico e o paciente existem
        cursor.execute("SELECT * FROM medico WHERE medical_staff_empregado_pessoa_cc = %s", (medico_medical_staff_empregado_pessoa_cc,))
        medico = cursor.fetchone()
        cursor.execute("SELECT * FROM paciente WHERE pessoa_cc = %s", (paciente_pessoa_cc,))
        paciente = cursor.fetchone()
        if not (medico and paciente):
            return jsonify({'status': 'error', 'message': 'doctor or paciente not found'}), 404

        # Inserir dados na tabela de consultas
        cursor.execute("""
            INSERT INTO consultas (data, assistente_medical_staff_empregado_pessoa_cc, medico_medical_staff_empregado_pessoa_cc, paciente_pessoa_cc, id_fatura)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING consulta_numero
        """, (data_consulta, assistente_medical_staff_empregado_pessoa_cc, medico_medical_staff_empregado_pessoa_cc, paciente_pessoa_cc, id_fatura))
        consulta_numero = cursor.fetchone()[0]

        # Commit da transação
        conn.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Retornar resposta de sucesso com o ID da consulta
        return jsonify({'status': 'success', 'message': 'Scheduled appointment successfully ', 'consulta_numero': consulta_numero}), 200
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/dbproj/appointments/<patient_user_id>', methods=['GET'])
def list_appointments(patient_user_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Verificar o tipo de usuário usando o token JWT
        auth_token = request.headers.get('Authorization')
        decoded_token = jwt.decode(auth_token.encode('utf-8'), SECRET_KEY, algorithms=['HS256'])
        user_type = decoded_token.get('user_type')
        user_id = decoded_token.get('user_id')

        # Verificar se o usuário é assistente ou o próprio paciente
        if user_type not in ['assistente', 'paciente']:
            return jsonify({'status': 'error', 'message': 'Access denied'}), 403

        if user_type == 'paciente' and user_id != patient_user_id:
            return jsonify({'status': 'error', 'message': 'Access denied'}), 403

        # Obter informações das consultas do paciente
        cursor.execute("""
            SELECT c.consulta_numero, c.data, c.medico_medical_staff_empregado_pessoa_cc, e.pessoa_cc AS doctor_id, p.nome AS doctor_name
            FROM consultas c
            JOIN medico m ON c.medico_medical_staff_empregado_pessoa_cc = m.medical_staff_empregado_pessoa_cc
            JOIN empregado e ON m.medical_staff_empregado_pessoa_cc = e.pessoa_cc
            JOIN pessoa p ON e.pessoa_cc = p.cc
            WHERE c.paciente_pessoa_cc = %s
        """, (patient_user_id,))
        appointments = cursor.fetchall()

        # Estruturar os resultados
        results = []
        for appointment in appointments:
            results.append({
                'id': appointment[0],
                'date': appointment[1],
                'doctor_id': appointment[3],
                'doctor_name': appointment[4]
            })

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Retornar resposta de sucesso com os dados das consultas
        return jsonify({'status': 'success', 'results': results}), 200
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/dbproj/surgery', methods=['POST'])
@app.route('/dbproj/surgery/<int:hospitalization_id>', methods=['POST'])
def schedule_surgery(hospitalization_id=None):
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Extrair dados da solicitação
        data = request.json
        patient_id = data['patient_id']
        doctor_id = data['doctor']
        nurses = data['nurses']
        date = data['date']
        room = data.get('room', None)
        bed = data.get('bed', None)
        discharge_date = data.get('discharge_date', None)
        assistant_id = data.get('assistant_id', None)
        preco = data['preco']
        parcelas = data.get('parcelas', None)
        data_limite = data.get('data_limite', None)
        data_de_emissao = date  # Presumindo que a data de emissão é a data da cirurgia

        # Verificar o tipo de usuário usando o token JWT
        auth_token = request.headers.get('Authorization')
        decoded_token = jwt.decode(auth_token.encode('utf-8'), SECRET_KEY, algorithms=['HS256'])
        user_type = decoded_token.get('user_type')

        # Verificar se o usuário é assistente
        if user_type != 'assistente':
            return jsonify({'status': 'error', 'message': 'Only assistants can schedule surgerys'}), 403

        # Verificar se o assistente existe
        user_id = decoded_token.get('user_id')
        cursor.execute("SELECT * FROM assistente WHERE medical_staff_empregado_pessoa_cc = %s", (user_id,))
        assistente = cursor.fetchone()
        if not assistente:
            return jsonify({'status': 'error', 'message': 'Assistant not found'}), 404

        # Verificar se o paciente, médico e enfermeiros existem
        cursor.execute("SELECT * FROM paciente WHERE pessoa_cc = %s", (patient_id,))
        patient = cursor.fetchone()
        cursor.execute("SELECT * FROM medico WHERE medical_staff_empregado_pessoa_cc = %s", (doctor_id,))
        doctor = cursor.fetchone()
        if not (patient and doctor):
            return jsonify({'status': 'error', 'message': 'Pacient or doctor not found'}), 404

        for nurse_id, role in nurses:
            cursor.execute("SELECT * FROM enfermeiro WHERE medical_staff_empregado_pessoa_cc = %s", (nurse_id,))
            nurse = cursor.fetchone()
            if not nurse:
                return jsonify({'status': 'error', 'message': f'Enfermeiro com ID {nurse_id} não encontrado'}), 404

        # Criar nova entrada na tabela facturacao
        cursor.execute("""
            INSERT INTO facturacao (data_de_emissao, data_limite, preco, parcelas, paciente_pessoa_cc)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_fatura
        """, (data_de_emissao, data_limite, preco, parcelas, patient_id))
        facturacao_id = cursor.fetchone()[0]

        # Se hospitalization_id não for fornecido, criar uma nova internação
        if not hospitalization_id:
            cursor.execute("""
                INSERT INTO internacao (maca, data_inicio, data_de_alta, quarto, facturacao_id_fatura, assistente_medical_staff_empregado_pessoa_cc, enfermeiro_medical_staff_empregado_pessoa_cc, paciente_pessoa_cc)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING internacao_numero
            """, (bed, date, discharge_date, room, facturacao_id, assistant_id, nurses[0][0], patient_id))
            hospitalization_id = cursor.fetchone()[0]

        # Inserir dados na tabela de cirurgias
        cursor.execute("""
            INSERT INTO cirurgia (data, sala, facturacao_id_fatura, medico_medical_staff_empregado_pessoa_cc, internacao_numero, paciente_pessoa_cc)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (date, room, facturacao_id, doctor_id, hospitalization_id, patient_id))
        surgery_id = cursor.fetchone()[0]

        # Inserir dados na tabela de enfermeiro_cirurgia para cada enfermeiro
        for nurse_id, role in nurses:
            cursor.execute("""
                INSERT INTO enfermeiro_cirurgia (enfermeiro_medical_staff_empregado_pessoa_cc, cirurgia_id)
                VALUES (%s, %s)
            """, (nurse_id, surgery_id))

        # Commit da transação
        conn.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Retornar resposta de sucesso com os IDs da cirurgia e da internação
        return jsonify({
            'status': 'success',
            'message': 'Surgery scheduled successfully',
            'results': {
                'hospitalization_id': hospitalization_id,
                'surgery_id': surgery_id,
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'date': date
            }
        }), 200
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500



@app.route('/dbproj/prescriptions/<person_id>', methods=['GET'])
def get_prescriptions(person_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Verificar o tipo de usuário usando o token JWT
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            return jsonify({'status': 'error', 'message': 'Token JWT não fornecido'}), 401

        try:
            decoded_token = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        except ExpiredSignatureError:
            return jsonify({'status': 'error', 'message': 'Token JWT expirado'}), 401
        except (InvalidTokenError, DecodeError):
            return jsonify({'status': 'error', 'message': 'Falha na verificação da token'}), 401

        user_type = decoded_token.get('user_type')
        user_id = decoded_token.get('user_id')

        # Verificar se o usuário é um funcionário autorizado ou o próprio paciente
        if user_type not in ['assistente', 'enfermeiro', 'medico', 'paciente']:
            return jsonify({'status': 'error', 'message': 'Acesso negado'}), 403

        if user_type == 'paciente' and user_id != person_id:
            return jsonify({'status': 'error', 'message': 'Acesso negado'}), 403

        # Obter as prescrições para o paciente específico
        cursor.execute("""
            SELECT p.id, p.data_prescricao, d.quantidade, d.medicamento_nome
            FROM prescricao p
            JOIN dosagem d ON p.id = d.receita_id
            WHERE p.paciente_pessoa_cc = %s
        """, (person_id,))
        prescriptions = cursor.fetchall()

        # Estruturar os resultados
        results = []
        for prescription in prescriptions:
            results.append({
                'id': prescription[0],
                'validity': prescription[1],
                'dose': prescription[2],
                'medicine_name': prescription[3]
            })

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Retornar resposta de sucesso com os detalhes das prescrições
        return jsonify({'status': 'success', 'results': results}), 200
    except Exception as e:
        # Em caso de erro, retornar uma mensagem de erro
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/dbproj/prescription', methods=['POST'])
def add_prescription():
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Extrair dados da solicitação
        data = request.json
        prescription_type = data['type']
        event_id = data['event_id']
        validity = data['validity']
        medicines = data['medicines']

        # Verificar o tipo de usuário usando o token JWT
        auth_token = request.headers.get('Authorization')
        decoded_token = jwt.decode(auth_token.encode('utf-8'), SECRET_KEY, algorithms=['HS256'])
        user_type = decoded_token.get('user_type')

        # Verificar se o usuário é médico
        if user_type != 'medico':
            return jsonify({'status': 'error', 'message': 'Only doctors can add prescriptions'}), 403

        # Verificar se o evento (consulta ou internação) existe
        if prescription_type == 'appointment':
            cursor.execute("SELECT paciente_pessoa_cc FROM consultas WHERE consulta_numero = %s", (event_id,))
        elif prescription_type == 'hospitalization':
            cursor.execute("SELECT paciente_pessoa_cc FROM internacao WHERE internacao_numero = %s", (event_id,))
        else:
            return jsonify({'status': 'error', 'message': 'invalid event type'}), 400

        event = cursor.fetchone()
        if not event:
            return jsonify({'status': 'error', 'message': 'Event not found'}), 404

        paciente_pessoa_cc = event[0]  # Corrigido para acessar o índice correto

        # Inserir prescrição
        cursor.execute("""
            INSERT INTO receita (inicio, data_fim, medico_medical_staff_empregado_pessoa_cc, paciente_pessoa_cc)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (validity, None, decoded_token['user_id'], paciente_pessoa_cc))
        prescription_id = cursor.fetchone()[0]

        # Inserir medicamentos na prescrição
        for medicine in medicines:
            medicine_name = medicine['medicine']
            posology_dose = medicine['posology_dose']
            posology_frequency = medicine['posology_frequency']
            cursor.execute("""
                INSERT INTO dosagem (quantidade, receita_id, medicamento_nome)
                VALUES (%s, %s, %s)
            """, (posology_dose, prescription_id, medicine_name))

        # Commit da transação
        conn.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Retornar resposta de sucesso
        return jsonify({'status': 'success', 'results': prescription_id}), 200
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500





# Endpoint para efetuar o pagamento de uma fatura
@app.route('/dbproj/bills/<int:bill_id>', methods=['POST'])
def make_payment(bill_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Verificar o tipo de usuário usando o token JWT
        auth_token = request.headers.get('Authorization')
        decoded_token = jwt.decode(auth_token.encode('utf-8'), SECRET_KEY, algorithms=['HS256'])
        user_type = decoded_token.get('user_type')
        user_id = decoded_token.get('user_id')

        # Verificar se o usuário é o paciente
        if user_type != 'paciente':
            return jsonify({'status': 'error', 'message': 'Only patients can pay their bills'}), 403

        # Extrair dados da solicitação
        data = request.json
        amount = data['amount']
        payment_method = data['payment_method']

        # Verificar se a fatura existe e pertence ao paciente
        cursor.execute("SELECT paciente_pessoa_cc, preco FROM facturacao WHERE id_fatura = %s", (bill_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'status': 'error', 'message': 'Bill not found'}), 404
        patient_id, bill_amount = result

        if patient_id != user_id:
            return jsonify({'status': 'error', 'message': 'You can only pay your own bills'}), 403

        # Verificar se o valor do pagamento é válido
        if amount < 0 or amount > bill_amount:
            return jsonify({'status': 'error', 'message': 'Invalid payment amount'}), 400

        # Registrar o pagamento na tabela de pagamentos
        cursor.execute("INSERT INTO pagamentos (data, quantia, facturacao_id_fatura) VALUES (current_date, %s, %s) RETURNING id", (amount, bill_id))
        payment_id = cursor.fetchone()[0]

        # Atualizar o status da fatura para "pago" se o valor total foi pago
        cursor.execute("SELECT SUM(quantia) FROM pagamentos WHERE facturacao_id_fatura = %s", (bill_id,))
        total_paid = cursor.fetchone()[0] or 0
        if total_paid >= bill_amount:
            cursor.execute("UPDATE facturacao SET status = 'paid' WHERE id_fatura = %s", (bill_id,))

        # Commit da transação
        conn.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        remaining_value = bill_amount - total_paid
        return jsonify({'status': 'success', 'message': 'Payment successful', 'remaining_value': remaining_value}), 200
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/dbproj/top3', methods=['GET'])
def list_top3_patients():
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Verificar o tipo de usuário usando o token JWT
        auth_token = request.headers.get('Authorization')
        try:
            decoded_token = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidTokenError, DecodeError):
            return jsonify({'status': 403, 'errors': 'Invalid or expired token', 'results': None}), 403

        user_type = decoded_token.get('user_type')

        # Verificar se o usuário é assistente
        if user_type != 'assistente':
            return jsonify({'status': 403, 'errors': 'Only assistants can access this endpoint', 'results': None}), 403

        # Consulta SQL para obter os top 3 pacientes e seus procedimentos
        query = """
        SELECT p.nome AS patient_name, SUM(f.preco) AS amount_spent,
               json_agg(json_build_object(
                   'id', pr.id,
                   'consulta_numero', pr.consulta_numero,
                   'cirurgia_id', pr.cirurgia_id,
                   'internacao_numero', pr.internacao_numero,
                   'medico_cc', pr.medico_cc,
                   'paciente_cc', pr.paciente_cc
               )) AS procedures
        FROM paciente pa
        JOIN pessoa p ON pa.pessoa_cc = p.cc
        JOIN facturacao f ON pa.pessoa_cc = f.paciente_pessoa_cc
        LEFT JOIN procedimentos pr ON pa.pessoa_cc = pr.paciente_cc
        WHERE DATE_TRUNC('month', f.data_de_emissao) = DATE_TRUNC('month', CURRENT_DATE)
        GROUP BY p.nome
        ORDER BY amount_spent DESC
        LIMIT 3;
        """

        cursor.execute(query)
        top_patients = cursor.fetchall()

        # Estrutura de resposta
        results = []
        for patient in top_patients:
            patient_name, amount_spent, procedures = patient
            results.append({
                'patient_name': patient_name,
                'amount_spent': amount_spent,
                'procedures': procedures
            })

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        return jsonify({'status': 200, 'errors': None, 'results': results})
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 500, 'errors': str(e), 'results': None})


@app.route('/dbproj/daily/<date>', methods=['GET'])
def daily_summary(date):
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Verificar o tipo de usuário usando o token JWT
        auth_token = request.headers.get('Authorization')
        try:
            decoded_token = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidTokenError, DecodeError):
            return jsonify({'status': 403, 'errors': 'Invalid or expired token', 'results': None}), 403

        user_type = decoded_token.get('user_type')

        # Verificar se o usuário é assistente
        if user_type != 'assistente':
            return jsonify({'status': 403, 'errors': 'Only assistants can access this endpoint', 'results': None}), 403

        # Validar o formato da data
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'status': 400, 'errors': 'Invalid date format, use YYYY-MM-DD', 'results': None}), 400

        # Consulta SQL para obter o resumo diário
        query = """
        SELECT 
            COALESCE(SUM(pag.quantia), 0) AS amount_spent,
            COALESCE(COUNT(DISTINCT cir.id), 0) AS surgeries_count,
            COALESCE(COUNT(DISTINCT pre.id), 0) AS prescriptions_count
        FROM 
            facturacao f
        LEFT JOIN pagamentos pag ON f.id_fatura = pag.facturacao_id_fatura AND pag.data = %s
        LEFT JOIN cirurgia cir ON f.id_fatura = cir.facturacao_id_fatura AND cir.data = %s
        LEFT JOIN prescricao pre ON f.paciente_pessoa_cc = pre.paciente_pessoa_cc AND pre.data_prescricao = %s
        WHERE 
            pag.data = %s OR cir.data = %s OR pre.data_prescricao = %s;
        """
        cursor.execute(query, (date, date, date, date, date, date))
        result = cursor.fetchone()

        amount_spent, surgeries_count, prescriptions_count = result

        response = {
            "amount_spent": amount_spent,
            "surgeries": surgeries_count,
            "prescriptions": prescriptions_count
        }

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        return jsonify({'status': 200, 'errors': None, 'results': response})
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 500, 'errors': str(e), 'results': None})


@app.route('/dbproj/report', methods=['GET'])
def monthly_report():
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Verificar o tipo de usuário usando o token JWT
        auth_token = request.headers.get('Authorization')
        try:
            decoded_token = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidTokenError, DecodeError):
            return jsonify({'status': 403, 'errors': 'Invalid or expired token', 'results': None}), 403

        user_type = decoded_token.get('user_type')

        # Verificar se o usuário é assistente
        if user_type != 'assistente':
            return jsonify({'status': 403, 'errors': 'Only assistants can access this endpoint', 'results': None}), 403

        # Consulta SQL para obter o relatório mensal dos médicos com mais cirurgias nos últimos 12 meses
        query = """
        SELECT 
            TO_CHAR(c.data, 'YYYY-MM') AS month,
            p.nome AS doctor,
            COUNT(c.id) AS total_surgeries
        FROM 
            cirurgia c
        JOIN medico m ON c.medico_medical_staff_empregado_pessoa_cc = m.medical_staff_empregado_pessoa_cc
        JOIN pessoa p ON m.medical_staff_empregado_pessoa_cc = p.cc
        WHERE 
            c.data >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY 
            month, doctor
        ORDER BY 
            month DESC, total_surgeries DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        results = []
        month_surgery_count = {}

        # Agrupar os resultados por mês, mantendo apenas o médico com mais cirurgias em cada mês
        for row in rows:
            month, doctor, total_surgeries = row
            if month not in month_surgery_count:
                month_surgery_count[month] = (doctor, total_surgeries)

        # Formatar os resultados
        for month, (doctor, total_surgeries) in month_surgery_count.items():
            results.append({
                "month": month,
                "doctor": doctor,
                "surgeries": total_surgeries
            })

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        return jsonify({'status': 200, 'errors': None, 'results': results})
    except Exception as e:
        # Em caso de erro, realizar o rollback e retornar uma mensagem de erro
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'status': 500, 'errors': str(e), 'results': None})


if __name__ == '__main__':
    app.run(debug=True)
