# Red Team — regras do exercício

## Escopo permitido
Atacar somente:
- a aplicação SecureBoard;
- o endereço/IP fornecido pelo professor;
- as portas explicitamente autorizadas.

## Objetivos
Investigar:
1. autenticação;
2. autorização;
3. sessão;
4. validação de entradas;
5. XSS;
6. CSRF;
7. exposição de informações;
8. configuração HTTP;
9. rate limiting;
10. comportamento dos logs;
11. falhas de lógica.

## Restrições
- Não atacar sistemas externos.
- Não coletar credenciais reais.
- Não usar dados pessoais reais.
- Não realizar DoS/DDoS.
- Não persistir malware.
- Não tentar sair do laboratório.
- Não apagar evidências.
- Não destruir o banco.

## Relatório
Para cada achado:
- título;
- ativo afetado;
- pré-condição;
- passos reproduzíveis;
- evidência;
- impacto;
- severidade justificada;
- recomendação;
- como validar a correção.

O professor poderá pedir demonstração controlada de cada achado.
