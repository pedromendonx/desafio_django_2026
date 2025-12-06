DROP TABLE IF EXISTS matriculas_matricula CASCADE;
DROP TABLE IF EXISTS cursos_curso CASCADE;
DROP TABLE IF EXISTS alunos_aluno CASCADE;

CREATE TABLE alunos_aluno (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    cpf CHAR(11) NOT NULL UNIQUE,     
    data_ingresso DATE NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT now(),
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE OR REPLACE FUNCTION alunos_atualiza_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.atualizado_em = now();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_alunos_timestamp
BEFORE UPDATE ON alunos_aluno
FOR EACH ROW
EXECUTE PROCEDURE alunos_atualiza_timestamp();

CREATE TABLE cursos_curso (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    carga_horaria INTEGER NOT NULL CHECK (carga_horaria >= 0),
    valor_inscricao NUMERIC(10,2) NOT NULL CHECK (valor_inscricao >= 0),
    status BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT now(),
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE OR REPLACE FUNCTION cursos_atualiza_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.atualizado_em = now();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_cursos_timestamp
BEFORE UPDATE ON cursos_curso
FOR EACH ROW
EXECUTE PROCEDURE cursos_atualiza_timestamp();

CREATE TABLE matriculas_matricula (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL REFERENCES alunos_aluno(id) ON DELETE CASCADE,
    curso_id INTEGER NOT NULL REFERENCES cursos_curso(id) ON DELETE CASCADE,
    data_matricula DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(10) NOT NULL CHECK (status IN ('pago','pendente')),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT now(),
    CONSTRAINT matricula_aluno_curso_unique UNIQUE (aluno_id, curso_id)
);

CREATE INDEX idx_matriculas_aluno ON matriculas_matricula(aluno_id);
CREATE INDEX idx_matriculas_curso ON matriculas_matricula(curso_id);
CREATE INDEX idx_matriculas_status ON matriculas_matricula(status);

INSERT INTO alunos_aluno (nome, email, cpf, data_ingresso)
VALUES
('Ana Souza', 'ana.souza@example.com', '12345678901', '2024-03-01'),
('Bruno Lima', 'bruno.lima@example.com', '23456789012', '2025-02-15'),
('Carla Ramos', 'carla.ramos@example.com', '34567890123', '2025-09-01');

INSERT INTO cursos_curso (nome, carga_horaria, valor_inscricao, status)
VALUES
('Python Básico', 40, 150.00, TRUE),
('Django Avançado', 60, 300.00, TRUE),
('Data Science', 80, 600.00, FALSE);

INSERT INTO matriculas_matricula (aluno_id, curso_id, data_matricula, status)
VALUES
(1, 1, '2024-03-05', 'pago'),
(1, 2, '2024-04-10', 'pendente'),
(2, 1, '2025-02-20', 'pendente'),
(2, 3, '2025-03-01', 'pago'),
(3, 2, '2025-09-10', 'pendente');

SELECT
  c.id AS curso_id,
  c.nome AS curso_nome,
  COUNT(m.id) AS total_matriculas
FROM cursos_curso c
LEFT JOIN matriculas_matricula m ON m.curso_id = c.id
GROUP BY c.id, c.nome
ORDER BY total_matriculas DESC;

SELECT
  a.id AS aluno_id,
  a.nome AS aluno_nome,
  COALESCE(SUM(c.valor_inscricao), 0) AS total_devido
FROM alunos_aluno a
LEFT JOIN matriculas_matricula m ON m.aluno_id = a.id AND m.status = 'pendente'
LEFT JOIN cursos_curso c ON m.curso_id = c.id
GROUP BY a.id, a.nome
ORDER BY total_devido DESC;

SELECT
  a.id AS aluno_id,
  a.nome AS aluno_nome,
  COALESCE(SUM(c.valor_inscricao), 0) AS total_pago
FROM alunos_aluno a
LEFT JOIN matriculas_matricula m ON m.aluno_id = a.id AND m.status = 'pago'
LEFT JOIN cursos_curso c ON m.curso_id = c.id
GROUP BY a.id, a.nome
ORDER BY total_pago DESC;

SELECT
  (SELECT COUNT(*) FROM alunos_aluno) AS total_alunos,
  (SELECT COUNT(*) FROM cursos_curso WHERE status = TRUE) AS cursos_ativos,
  (SELECT COUNT(*) FROM matriculas_matricula WHERE status = 'pago') AS matriculas_pagas,
  (SELECT COUNT(*) FROM matriculas_matricula WHERE status = 'pendente') AS matriculas_pendentes;

CREATE OR REPLACE VIEW resumo_financeiro_por_aluno AS
SELECT
  a.id AS aluno_id,
  a.nome AS aluno_nome,
  COALESCE(SUM(CASE WHEN m.status = 'pago' THEN c.valor_inscricao ELSE 0 END), 0) AS total_pago,
  COALESCE(SUM(CASE WHEN m.status = 'pendente' THEN c.valor_inscricao ELSE 0 END), 0) AS total_devido,
  COALESCE(COUNT(m.id), 0) AS total_matriculas
FROM alunos_aluno a
LEFT JOIN matriculas_matricula m ON m.aluno_id = a.id
LEFT JOIN cursos_curso c ON m.curso_id = c.id
GROUP BY a.id, a.nome
ORDER BY total_devido DESC;