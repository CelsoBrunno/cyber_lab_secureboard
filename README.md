# Cyber Lab — SecureBoard

Aplicação web educacional para competição Blue Team x Red Team.

## Stack
- Python 3
- Flask
- SQLite
- SQLAlchemy
- Flask-WTF / CSRF
- Werkzeug password hashing
- Flask-Limiter
- Security headers
- Audit logging

## Objetivo da semana 1 — Blue Team
A equipe deve:
1. Instalar e executar a aplicação.
2. Fazer threat modeling.
3. Revisar autenticação/autorização.
4. Revisar validação de entradas.
5. Implementar/fortalecer controles de segurança.
6. Configurar logs e monitoramento.
7. Criar backup e procedimento de recuperação.
8. Produzir relatório de riscos e evidências.

## Objetivo da semana 2 — Red Team
Somente no ambiente disponibilizado pelo professor:
- identificar superfície de ataque;
- testar autenticação e autorização;
- testar validação de entradas;
- testar controles de sessão;
- procurar exposição de informações;
- analisar comportamento do sistema;
- documentar evidências, impacto e recomendação.

Não usar a aplicação para atacar terceiros ou infraestrutura externa.

## Execução

Windows:
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python seed.py
    python app.py

Linux/macOS:
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python seed.py
    python app.py

Abra:
    http://127.0.0.1:5000

Contas do laboratório:
- admin@secureboard.local / TroqueEssaSenha!2026
- aluno@secureboard.local / TroqueEssaSenha!2026

IMPORTANTE: são contas fictícias do laboratório. Troque-as antes de qualquer uso fora do laboratório.

## Regras sugeridas
- Red Team só pode atacar os IPs/portas definidos pelo professor.
- Nenhuma técnica deve sair do ambiente de laboratório.
- Blue Team deve manter evidências das alterações.
- Red Team deve preservar disponibilidade do serviço.
- O professor pode restaurar o banco entre rodadas.

## Variáveis de ambiente
SECRET_KEY deve ser definido em ambiente real.

Exemplo:
Linux:
    export SECRET_KEY="uma-chave-grande-e-aleatoria"

Windows PowerShell:
    $env:SECRET_KEY="uma-chave-grande-e-aleatoria"

