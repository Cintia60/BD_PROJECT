

-- Tabela Pessoa
CREATE TABLE pessoa (
    cc                  VARCHAR(512) PRIMARY KEY,
    nif                 INTEGER UNIQUE,
    nome                VARCHAR(512) NOT NULL,
    data_de_nascimento  DATE,
    morada              VARCHAR(512),
    telefone            INTEGER,
    genero              TEXT,
    mail                VARCHAR(512) UNIQUE,
    senha               VARCHAR(255) NOT NULL
);

-- Tabela Paciente
CREATE TABLE paciente (
    contacto_emergencia INTEGER,
    nome_ce             VARCHAR(512),
    grau_de_parentesco  VARCHAR(512),
    grupo_sanguineo     VARCHAR(512),
    pessoa_cc           VARCHAR(512) PRIMARY KEY,
    FOREIGN KEY (pessoa_cc) REFERENCES pessoa(cc)
);

-- Tabela Empregado
CREATE TABLE empregado (
    numero_de_empregado         INTEGER NOT NULL,
    data_de_entreada           DATE NOT NULL,
    data_de_fim_de_contracto   DATE NOT NULL,
    salario                    DOUBLE PRECISION NOT NULL,
    premios                    DOUBLE PRECISION,
    funcao                     VARCHAR(512),
    pessoa_cc                  VARCHAR(512) PRIMARY KEY,
    FOREIGN KEY (pessoa_cc) REFERENCES pessoa(cc)
);

-- Tabela Médico
CREATE TABLE medico (
    numero_de_licensa                  INTEGER,
    medical_staff_empregado_pessoa_cc  VARCHAR(512) PRIMARY KEY,
    FOREIGN KEY (medical_staff_empregado_pessoa_cc) REFERENCES empregado(pessoa_cc)
);

-- Tabela Enfermeiro
CREATE TABLE enfermeiro (
    categoria                            VARCHAR(512) NOT NULL,
    medical_staff_empregado_pessoa_cc   VARCHAR(512) PRIMARY KEY,
    FOREIGN KEY (medical_staff_empregado_pessoa_cc) REFERENCES empregado(pessoa_cc)
);

-- Tabela Assistente
CREATE TABLE assistente (
    medical_staff_empregado_pessoa_cc VARCHAR(512) PRIMARY KEY,
    FOREIGN KEY (medical_staff_empregado_pessoa_cc) REFERENCES empregado(pessoa_cc)
);

-- Tabela Consultas
CREATE TABLE consultas (
    consulta_numero                   INTEGER PRIMARY KEY,
    data                               TIMESTAMP,
    assistente_medical_staff_empregado_pessoa_cc VARCHAR(512) NOT NULL,
    medico_medical_staff_empregado_pessoa_cc   VARCHAR(512) NOT NULL,
    paciente_pessoa_cc                 VARCHAR(512) NOT NULL,
    FOREIGN KEY (assistente_medical_staff_empregado_pessoa_cc) REFERENCES assistente(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (medico_medical_staff_empregado_pessoa_cc) REFERENCES medico(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (paciente_pessoa_cc) REFERENCES paciente(pessoa_cc)
);

-- Tabela Medicamento
CREATE TABLE medicamento (
    nome         VARCHAR(512) PRIMARY KEY,
    id           SERIAL,
    validade     DATE NOT NULL
);

-- Tabela Efeito Secundário
CREATE TABLE efeito_secundario (
    id     SERIAL PRIMARY KEY,
    efeito VARCHAR(512) UNIQUE
);

-- Tabela Efeito Medicamento
CREATE TABLE efeito_medicamento (
    intensidade           VARCHAR(512) NOT NULL,
    efeito_secundario_id INTEGER,
    medicamento_nome      VARCHAR(512),
    PRIMARY KEY(efeito_secundario_id, medicamento_nome),
    FOREIGN KEY (efeito_secundario_id) REFERENCES efeito_secundario(id),
    FOREIGN KEY (medicamento_nome) REFERENCES medicamento(nome)
);

-- Tabela Cirurgia
CREATE TABLE cirurgia (
    data                                        DATE NOT NULL,
    sala                                        VARCHAR(512),
    id                                          SERIAL PRIMARY KEY,
    facturacao_id_fatura                        INTEGER NOT NULL,
    medico_medical_staff_empregado_pessoa_cc    VARCHAR(512) NOT NULL,
    internacao_numero                           INTEGER NOT NULL,
    paciente_pessoa_cc                          VARCHAR(512) NOT NULL,
    FOREIGN KEY (facturacao_id_fatura) REFERENCES facturacao(id_fatura),
    FOREIGN KEY (medico_medical_staff_empregado_pessoa_cc) REFERENCES medico(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (internacao_numero) REFERENCES internacao(internacao_numero),
    FOREIGN KEY (paciente_pessoa_cc) REFERENCES paciente(pessoa_cc)
);

-- Tabela Internação
CREATE TABLE internacao (
    maca                                        INTEGER NOT NULL,
    data_inicio                                 TIMESTAMP NOT NULL,
    data_de_alta                                DATE,
    quarto                                      NUMERIC(8,2) NOT NULL,
    internacao_numero                           SERIAL PRIMARY KEY,
    facturacao_id_fatura                        INTEGER NOT NULL,
    assistente_medical_staff_empregado_pessoa_cc VARCHAR(512) NOT NULL,
    enfermeiro_medical_staff_empregado_pessoa_cc VARCHAR(512) NOT NULL,
    paciente_pessoa_cc                          VARCHAR(512) NOT NULL,
    FOREIGN KEY (facturacao_id_fatura) REFERENCES facturacao(id_fatura),
    FOREIGN KEY (assistente_medical_staff_empregado_pessoa_cc) REFERENCES assistente(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (enfermeiro_medical_staff_empregado_pessoa_cc) REFERENCES enfermeiro(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (paciente_pessoa_cc) REFERENCES paciente(pessoa_cc)
);

-- Tabela Facturação
CREATE TABLE facturacao (
    data_de_emissao DATE NOT NULL,
    data_limite     DATE,
    preco           INTEGER NOT NULL,
    parcelas        INTEGER,
    id_fatura       SERIAL PRIMARY KEY,
    paciente_pessoa_cc VARCHAR(512) NOT NULL,
    FOREIGN KEY (paciente_pessoa_cc) REFERENCES paciente(pessoa_cc)
);

-- Tabela Receita
CREATE TABLE receita (
    inicio                                    DATE NOT NULL,
    data_fim                                  DATE,
    id                                        SERIAL PRIMARY KEY,
    medico_medical_staff_empregado_pessoa_cc VARCHAR(512) NOT NULL,
    paciente_pessoa_cc                        VARCHAR(512) NOT NULL,
    FOREIGN KEY (medico_medical_staff_empregado_pessoa_cc) REFERENCES medico(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (paciente_pessoa_cc) REFERENCES paciente(pessoa_cc)
);

-- Tabela Efeito Medicamento (continuação)
CREATE TABLE efeito_medicamento (
    intensidade           VARCHAR(512) NOT NULL,
    efeito_secundario_id INTEGER,
    medicamento_nome      VARCHAR(512),
    PRIMARY KEY(efeito_secundario_id, medicamento_nome),
    FOREIGN KEY (efeito_secundario_id) REFERENCES efeito_secundario(id),
    FOREIGN KEY (medicamento_nome) REFERENCES medicamento(nome)
);

-- Tabela Pagamentos
CREATE TABLE pagamentos (
    id                  SERIAL PRIMARY KEY,
    data                DATE NOT NULL,
    quantia             FLOAT(8) NOT NULL,
    facturacao_id_fatura INTEGER NOT NULL,
    FOREIGN KEY (facturacao_id_fatura) REFERENCES facturacao(id_fatura)
);





-- Tabela Dosagem
CREATE TABLE dosagem (
    quantidade       VARCHAR(512) NOT NULL,
    receita_id       SERIAL,
    medicamento_nome VARCHAR(512),
    PRIMARY KEY(receita_id, medicamento_nome),
    FOREIGN KEY (receita_id) REFERENCES receita(id),
    FOREIGN KEY (medicamento_nome) REFERENCES medicamento(nome)
);

-- Tabela Medical Staff
CREATE TABLE medical_staff (
    empregado_pessoa_cc VARCHAR(512) PRIMARY KEY,
    FOREIGN KEY (empregado_pessoa_cc) REFERENCES empregado(pessoa_cc)
);

-- Tabela None Medical Staff
CREATE TABLE none_medical_staff (
    empregado_pessoa_cc VARCHAR(512) PRIMARY KEY,
    FOREIGN KEY (empregado_pessoa_cc) REFERENCES empregado(pessoa_cc)
);

-- Tabela Receita Internação
CREATE TABLE receita_internacao (
    internacao_numero INTEGER NOT NULL,
    receita_id        SERIAL,
    PRIMARY KEY(receita_id),
    FOREIGN KEY (internacao_numero) REFERENCES internacao(internacao_numero),
    FOREIGN KEY (receita_id) REFERENCES receita(id)
);

-- Tabela Receita Consulta
CREATE TABLE receita_consulta (
    consulta_numero INTEGER NOT NULL,
    receita_id      SERIAL,
    PRIMARY KEY(consulta_numero, receita_id),
    FOREIGN KEY (consulta_numero) REFERENCES consultas(consulta_numero),
    FOREIGN KEY (receita_id) REFERENCES receita(id)
);

-- Tabela Especializacao
CREATE TABLE especializacao (
    id             SERIAL PRIMARY KEY,
    especializacao VARCHAR(512) UNIQUE,
    superior       CHAR(255)
);

-- Tabela Medico_Especializacao
CREATE TABLE medico_especializacao (
    medico_medical_staff_empregado_pessoa_cc VARCHAR(512),
    especializacao_id                SERIAL,
    PRIMARY KEY(medico_medical_staff_empregado_pessoa_cc, especializacao_id),
    FOREIGN KEY (medico_medical_staff_empregado_pessoa_cc) REFERENCES medico(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (especializacao_id) REFERENCES especializacao(id)
);

-- Tabela Enfermeiro_Cirurgia
CREATE TABLE enfermeiro_cirurgia (
    enfermeiro_medical_staff_empregado_pessoa_cc VARCHAR(512),
    cirurgia_id                                 SERIAL,
    PRIMARY KEY(enfermeiro_medical_staff_empregado_pessoa_cc, cirurgia_id),
    FOREIGN KEY (enfermeiro_medical_staff_empregado_pessoa_cc) REFERENCES enfermeiro(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (cirurgia_id) REFERENCES cirurgia(id)
);

-- Tabela Enfermeiro_Consultas
CREATE TABLE enfermeiro_consultas (
    enfermeiro_medical_staff_empregado_pessoa_cc VARCHAR(512),
    consulta_numero                             SERIAL,
    PRIMARY KEY(enfermeiro_medical_staff_empregado_pessoa_cc, consulta_numero),
    FOREIGN KEY (enfermeiro_medical_staff_empregado_pessoa_cc) REFERENCES enfermeiro(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (consulta_numero) REFERENCES consultas(consulta_numero)
);

-- Tabela Medico_Paciente
CREATE TABLE medico_paciente (
    medico_medical_staff_empregado_pessoa_cc VARCHAR(512),
    paciente_pessoa_cc                       VARCHAR(512),
    PRIMARY KEY(medico_medical_staff_empregado_pessoa_cc, paciente_pessoa_cc),
    FOREIGN KEY (medico_medical_staff_empregado_pessoa_cc) REFERENCES medico(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (paciente_pessoa_cc) REFERENCES paciente(pessoa_cc)
);



CREATE TABLE prescricao (
    id SERIAL PRIMARY KEY,
    data_prescricao DATE NOT NULL,
    medico_medical_staff_empregado_pessoa_cc VARCHAR(512) NOT NULL,
    paciente_pessoa_cc VARCHAR(512) NOT NULL,
    FOREIGN KEY (medico_medical_staff_empregado_pessoa_cc) REFERENCES medico(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (paciente_pessoa_cc) REFERENCES paciente(pessoa_cc)
);


-- Tabela Procedimentos
CREATE TABLE procedimentos (
    id                   SERIAL PRIMARY KEY,
    consulta_numero      INTEGER,
    cirurgia_id          INTEGER,
    internacao_numero    INTEGER,
    medico_cc            VARCHAR(512),
    paciente_cc          VARCHAR(512),
    FOREIGN KEY (consulta_numero) REFERENCES consultas(consulta_numero),
    FOREIGN KEY (cirurgia_id) REFERENCES cirurgia(id),
    FOREIGN KEY (internacao_numero) REFERENCES internacao(internacao_numero),
    FOREIGN KEY (medico_cc) REFERENCES medico(medical_staff_empregado_pessoa_cc),
    FOREIGN KEY (paciente_cc) REFERENCES paciente(pessoa_cc)
);

-- Índice na tabela pessoa
CREATE INDEX idx_pessoa_nome ON pessoa (nome);
CREATE INDEX idx_pessoa_data_nascimento ON pessoa (data_de_nascimento);

-- Índice na tabela paciente
CREATE INDEX idx_paciente_grupo_sanguineo ON paciente (grupo_sanguineo);

-- Índice na tabela empregado
CREATE INDEX idx_empregado_funcao ON empregado (funcao);

-- Índice na tabela medico
CREATE INDEX idx_medico_numero_licensa ON medico (numero_de_licensa);

-- Índice na tabela enfermeiro
CREATE INDEX idx_enfermeiro_categoria ON enfermeiro (categoria);

-- Índice na tabela consultas
CREATE INDEX idx_consultas_data ON consultas (data);

-- Índice na tabela medicamento
CREATE INDEX idx_medicamento_validade ON medicamento (validade);

-- Índice na tabela cirurgia
CREATE INDEX idx_cirurgia_data ON cirurgia (data);

-- Índice na tabela internancao
CREATE INDEX idx_internancao_data_inicio ON internacao (data_inicio);

-- Índice na tabela facturacao
CREATE INDEX idx_facturacao_data_emissao ON facturacao (data_de_emissao);






-- Trigger para Atualizar Fatura após qualquer Agendamento
CREATE OR REPLACE FUNCTION atualizar_fatura_agendamento()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza a fatura associada ao agendamento
    UPDATE facturacao
    SET data_de_emissao = current_date
    WHERE id_fatura = NEW.facturacao_id_fatura;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER atualizar_fatura_trigger
AFTER INSERT ON consultas
FOR EACH ROW
EXECUTE FUNCTION atualizar_fatura_agendamento();
