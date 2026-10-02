# Blue Team — checklist de endurecimento

## 1. Aplicação
- [ ] Remover segredo padrão do código.
- [ ] Definir SECRET_KEY forte por variável de ambiente.
- [ ] Garantir DEBUG desligado.
- [ ] Revisar mensagens de erro.
- [ ] Revisar cabeçalhos HTTP.
- [ ] Revisar CSP.
- [ ] Revisar limites de tamanho.

## 2. Autenticação
- [ ] Política de senha.
- [ ] Hash de senha.
- [ ] Rate limiting.
- [ ] Proteção contra enumeração de contas.
- [ ] Gestão segura da sessão.
- [ ] Logout por POST.
- [ ] Rotação/invalidação de sessão após login.

## 3. Autorização
- [ ] Testar usuário comum contra rotas administrativas.
- [ ] Testar acesso direto a recursos.
- [ ] Aplicar menor privilégio.
- [ ] Registrar violações.

## 4. Entrada e banco
- [ ] Validação server-side.
- [ ] ORM/queries parametrizadas.
- [ ] Limites de tamanho.
- [ ] Proteção contra XSS.
- [ ] Proteção CSRF.

## 5. Monitoramento
- [ ] Login bem-sucedido.
- [ ] Login falho.
- [ ] Tentativas de autorização.
- [ ] Criação de usuários.
- [ ] Comentários.
- [ ] Erros internos.
- [ ] IP/data/hora nos eventos relevantes.

## 6. Operação
- [ ] Backup.
- [ ] Restauração testada.
- [ ] Dependências atualizadas.
- [ ] Procedimento de resposta a incidente.
- [ ] Matriz de risco.

## 7. Evidências
A equipe deve apresentar:
- arquitetura;
- threat model;
- riscos encontrados;
- controles implementados;
- evidências antes/depois;
- logs;
- testes;
- plano de resposta a incidentes.
