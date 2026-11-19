# Meu Cronograma de Estudo

Cronograma de estudos para concursos, feito para usar no celular e no tablet: mostra o que estudar em cada dia, se reorganiza sozinho conforme o ritmo de quem estuda, traz a apostila oficial para ler dentro do app e acompanha o progresso até a prova. Pode ser instalado na tela inicial (PWA) e funciona sem internet.

O primeiro cronograma pronto é o do **IBGE 2027 – Recenseador (REC)** do 12º Censo Agropecuário, Florestal e Aquícola (Fundação Cesgranrio, prova em 31/01/2027).

**Acesse:** https://jacobbv.github.io/meu-cronograma-estudo/

## Funcionalidades

- **Primeiro acesso:** o app pergunta o nome e, se quiser, um PIN de 4 dígitos. Cada pessoa cria o próprio perfil, com foto opcional.
- **Cronograma em fila:** os assuntos formam uma fila, com as matérias intercaladas e Conhecimentos Técnicos com mais peso. Se a pessoa adianta ou deixa algo para depois, os próximos dias se reorganizam sozinhos, sem acumular tarefas atrasadas.
- **Ritmo por dia da semana:** escolhe quantos assuntos estudar em cada dia (por exemplo, 1 de segunda a sexta e 3 no sábado). O app mostra a data em que o conteúdo termina e avisa se não couber até a reta final.
- **Etapas por lugar:** cada assunto tem etapas separadas. Leitura e questões aparecem em "dá no trabalho"; videoaulas, em "em casa". O assunto só conta como concluído quando todas as etapas estão marcadas.
- **Adiantar:** um botão puxa o próximo assunto da fila para hoje.
- **Apostila no app:** a apostila oficial do IBGE (68 páginas) abre dentro do app, com sumário, zoom, tela cheia (ideal no tablet), troca de página deslizando o dedo e lembrança da página onde parou. As tarefas de leitura têm o botão "Abrir na p. X".
- **Barra do topo:** o foguinho com a sequência, o sininho de avisos e a foto do perfil ficam no cabeçalho verde.
- **Sequência de dias (foguinho):** conta os dias seguidos de estudo. Tocando no foguinho, abre um calendário das últimas 4 semanas com os dias estudados, a sequência atual, o recorde e uma mensagem do dia. Folgas, feriados e pausas não apagam o fogo. Se a sequência apagar há até 3 dias, dá para reacender estudando um assunto a mais no dia.
- **Placar de questões:** depois das questões, anota quantas acertou. O app mostra o percentual de acerto por matéria, aponta o ponto fraco e começa a reta final por ele.
- **Calendário:** visão por semana ou por mês, com bolinhas coloridas por matéria.
- **Edital:** gráfico de rosca com o andamento por matéria e a lista de todos os assuntos com a aula do Gran ou as páginas da apostila.
- **Prova:** data, horário, local, banca, questões por matéria, nota mínima, datas importantes do edital e o que levar no dia.
- **Pausas:** marca um período sem estudo (viagem, feriado da cidade) e a fila espera.
- **Avisos:** os prazos do edital aparecem no Hoje com um X para fechar (voltam ao reabrir o app) e ficam guardados no sininho, com contador de não lidos.
- **Tema:** automático, claro ou noite. O "Modo noturno" também fica no menu do perfil (toque na foto no topo).
- **Visual:** cinza neutro com laranja de destaque e cada matéria com sua cor (Português azul, Matemática laranja, Conhecimentos Técnicos verde, Questões roxo).
- **Cópia de segurança:** gera um código com todo o progresso para guardar e restaurar depois.
- **Card de compartilhamento:** ao mandar o link, aparece um card com título, descrição e imagem (Open Graph).

## Como instalar

1. Abra o link acima no **Safari** (iPhone/iPad) ou no **Chrome** (Android e tablets Android).
2. iPhone/iPad: Compartilhar → **Adicionar à Tela de Início**. Android: menu ⋮ → **Instalar app** (ou "Adicionar à tela inicial").
3. Abra uma vez com internet: o app e a apostila ficam salvos e passam a funcionar offline.

## Onde os dados ficam

Tudo fica salvo só no próprio aparelho (`localStorage`), sem servidor. Quem abre o link em outro aparelho vê o app vazio. O PIN só impede que outra pessoa abra o perfil no mesmo aparelho; ele não é uma senha de conta. Para trocar de aparelho, use a **Cópia de segurança**.

## Tecnologias

- HTML, CSS e JavaScript puro, sem framework e sem etapa de build
- PWA: Web App Manifest e Service Worker (cache para uso offline, inclusive da apostila)
- PDF.js para ler a apostila dentro do app
- `localStorage` para salvar o progresso
- GitHub Pages para hospedagem

## Estrutura

```
index.html              # o app inteiro (HTML, CSS e JS)
manifest.webmanifest    # nome, cores e ícones do app instalado
sw.js                   # service worker (cache offline)
apostila.pdf            # apostila oficial do 12º Censo Agro (IBGE), sem alterações
vendor/pdf.min.js       # PDF.js 3.11.174 (Mozilla)
vendor/pdf.worker.min.js
icon-180.png            # ícone do iPhone
icon-192.png            # ícone do Android
icon-512.png            # ícone grande / splash
favicon-32.png          # ícone da aba do navegador
og-image.png            # imagem do card de compartilhamento (1200×630)
```

## Créditos e referências

- **Fontes Barlow e Barlow Condensed:** Jeremy Tribby, via [Google Fonts](https://fonts.google.com/specimen/Barlow). Licença [SIL Open Font License 1.1](https://openfontlicense.org).
- **PDF.js 3.11.174:** [Mozilla](https://mozilla.github.io/pdf.js/). Licença [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).
- **Apostila:** *Conhecimentos básicos para o Censo Agropecuário, Florestal e Aquícola*, do [IBGE](https://www.ibge.gov.br) (ENCE / CTA), distribuída sem alterações, como publicada pela [Fundação Cesgranrio](https://www.cesgranrio.org.br) para o processo seletivo.
- **Conteúdo do cronograma:** baseado no Edital IBGE nº 03/2026 e na retificação de 16/11/2026.
- **Nomes das aulas:** citados apenas como referência do curso que a pessoa usa para estudar ([Gran](https://www.grancursosonline.com.br)). Este projeto não tem relação com o Gran, a Cesgranrio ou o IBGE.
- Ícones do app e da interface desenhados no próprio projeto.

## Versões

- **v3.2.0** (19/11/2026): novo visual com fundo neutro e laranja de destaque, etiquetas coloridas por matéria, menu do perfil com Modo noturno, novos ícones e imagem de compartilhamento.

- **v3.1.0** (19/11/2026): foguinho, sininho de avisos e foto do perfil no cabeçalho; painel da sequência com calendário de 4 semanas e mensagem do dia; avisos com X e central de avisos; apostila em tela cheia.

- **v3.0.0** (19/11/2026): cronograma em fila com ritmo por dia da semana e previsão de término, etapas por lugar (trabalho e casa), botão Adiantar, apostila dentro do app, sequência de dias com recuperação, placar de questões com ponto fraco, tema claro e noite, primeiro acesso com nome e PIN opcional.
- **v2.1.0** (19/11/2026): card de compartilhamento (Open Graph), ícone na aba do navegador e foto de perfil salva só no aparelho.
- **v2.0.0** (19/11/2026): calendário mensal, tarefas atrasadas passam para o dia seguinte, gráfico de andamento do edital por matéria, pausas por período, assuntos conferidos com o edital e a apostila, revisões variadas, datas do edital, regras do dia da prova e tela de créditos.
- **v1.0.0** (19/11/2026): primeira versão, com perfis, cronograma do IBGE 2027, abas Hoje, Semana, Conteúdo e Prova, dias de estudo ajustáveis, PWA e cópia de segurança.

## Autor

Feito por **Jacó** ([@JacobbV](https://github.com/JacobbV)) · QyuDev.
