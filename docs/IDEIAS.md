# Pilha de ideias

Tudo que já foi pensado para o app e ainda não saiu, para não se perder. A ordem é de prioridade aproximada.
Regra de ouro: tudo precisa continuar de graça (Firebase Spark, GitHub Pages e GitHub Actions em repositório público).

## Saiu na v4.8.0
- Simulado completo e por disciplina, com cronômetro; anotar acertos (com "erradas" na Cebraspe).
- Nível (XP), gráfico de evolução até a prova, meta de acerto e tendência.
- Resultado da prova de verdade e sugestão do próximo concurso.
- Revisão espaçada: pergunta ao concluir um assunto, pilha de revisões no Hoje.
- Lembrete diário: avisos do navegador e arquivo de calendário (.ics) com 30 dias.

## Próximas
1. **Banco de questões** (saiu na 4.9.0 para a PCPE, 180 questões autorais). Falta: conferência por uma pessoa (campo `rev`), Legislação Estadual de PE, Português/Informática/Raciocínio Lógico, bancos de outros concursos.
   - Questões autorais por disciplina e assunto, com gabarito, comentário e fonte exata (artigo de lei, súmula).
   - Geradas e conferidas em conversa com o Claude e entram no repositório por pull request, com selo "revisada" e botão "reportar erro". Nada de IA gerando questão ao vivo dentro do app (custo e risco de ensinar errado).
   - Nada copiado de provas reais nem de cursinhos. Rótulo "estilo Cebraspe", nunca "questão da Cebraspe".
   - Aba Questões com filtros (disciplina → assunto) e botão "Resolver questões deste assunto" no Hoje. O acerto alimenta o placar e os simulados.
   - Simulado montado a partir do banco, com correção automática (hoje o simulado é livre: a pessoa faz as questões fora do app e anota o resultado).
2. **Mais editais na vitrine** (PPPE, IFCE, IFRN, IFPE): mandar o PDF e rodar `tools/build_vitrine.py`.
3. **Revisões no calendário do app** e no aviso do sino.
4. **Tirar o recado pessoal do `index.html` público** e guardar na nuvem.

## Ideias soltas
- Simulado por assunto: sortear só entre os assuntos já concluídos.
- Mapa de calor de acertos por assunto.
- Modo prova: tela cheia, sem distração, relógio discreto.
- Compartilhar o resultado do simulado como imagem.
- Metas semanais (ex.: 3 simulados por semana) com selo.
- Cartões de memorização (tipo Anki) por assunto.
- Exportar o histórico de simulados em CSV.

## Limites conhecidos
- **Aviso com o app fechado**: um site instalado não consegue agendar notificação sozinho. Push de verdade pede servidor.
  Caminhos grátis estudados: (a) Firebase Cloud Messaging disparado por GitHub Actions: os agendamentos do Actions atrasam horas, então não serve para "às 19h em ponto"; (b) Cloud Functions: exige plano Blaze (cartão), fora de questão.
  Solução adotada: arquivo `.ics` para o calendário do celular, que alarma com o app fechado.
- iOS: avisos do navegador só funcionam no app instalado na tela inicial (iOS 16.4 ou mais) e com o app em uso.
