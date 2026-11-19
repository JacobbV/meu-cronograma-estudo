# Meu Cronograma de Estudo

Cronograma de estudos para concursos, feito para usar no celular: mostra o que estudar em cada dia, deixa marcar o que já foi estudado e acompanha o progresso até a prova. Pode ser instalado na tela inicial do iPhone ou do Android (PWA) e funciona sem internet.

O primeiro cronograma pronto é o do **IBGE 2027 – Recenseador (REC)** do 12º Censo Agropecuário, Florestal e Aquícola (Fundação Cesgranrio, prova em 31/01/2027).

**Acesse:** https://jacobbv.github.io/meu-cronograma-estudo/

## Funcionalidades

- **Perfis sem senha:** quem vai estudar escolhe o próprio nome ao abrir o app (ex.: Beatriz), com foto opcional. A foto é reduzida e salva só no aparelho, nunca no repositório.
- **Vários concursos por perfil:** o IBGE já vem montado, e dá para cadastrar outros com data, local e lista de assuntos.
- **Hoje:** o que estudar no dia, com caixinha para marcar. O que não foi feito nos dias anteriores aparece no dia seguinte como "atrasada", até ser marcado.
- **Calendário:** visão por **semana** ou por **mês**, com bolinhas coloridas por matéria em cada dia; tocando no dia, aparecem as tarefas.
- **Edital:** gráfico de rosca com quanto do edital já foi concluído, por matéria (Português em azul, Matemática em laranja, Conhecimentos Técnicos em verde), e a lista de todos os assuntos com a aula do Gran ou as páginas da apostila de cada um.
- **Prova:** data, horário, cargo, nível, local, banca, quantas questões tem cada matéria, nota mínima para passar, datas importantes do edital e o que levar no dia.
- **Dias de estudo ajustáveis:** liga e desliga dias da semana, escolhe a data de início e folga nos feriados.
- **Pausas:** marca um período sem estudo (viagem, feriado da cidade) e o conteúdo é empurrado para os dias seguintes, sem perder o que já foi marcado.
- **Revisões variadas:** quando o conteúdo acaba, as revisões alternam entre questões, flashcards, releitura dos resumos e dos trechos marcados da apostila.
- **Reta final automática:** a última semana antes da prova é só revisão, com lembrete do cartão de confirmação e simulado completo.
- **Avisos de prazo:** lembra no Hoje quando falta uma semana ou menos para um prazo do edital.
- **Card de compartilhamento:** ao mandar o link no WhatsApp ou em outras redes, aparece um card com título, descrição e imagem (Open Graph), e a aba do navegador mostra o ícone do app.
- **Cópia de segurança:** gera um código com todo o progresso para guardar e restaurar depois.

## Como instalar no celular

1. Abra o link acima no **Safari** (iPhone) ou no **Chrome** (Android).
2. iPhone: toque em Compartilhar → **Adicionar à Tela de Início**. Android: menu ⋮ → **Instalar app**.
3. O ícone verde aparece na tela inicial e o app abre em tela cheia.

## Onde os dados ficam

Tudo fica salvo só no próprio aparelho (`localStorage`), sem servidor e sem login. Se trocar de celular ou limpar os dados do navegador, use a **Cópia de segurança** na aba Prova para levar o progresso junto.

## Tecnologias

- HTML, CSS e JavaScript puro, sem framework e sem etapa de build
- PWA: Web App Manifest e Service Worker (cache para uso offline)
- `localStorage` para salvar o progresso
- GitHub Pages para hospedagem

## Estrutura

```
index.html            # o app inteiro (HTML, CSS e JS)
manifest.webmanifest  # nome, cores e ícones do app instalado
sw.js                 # service worker (cache offline)
icon-180.png          # ícone do iPhone
icon-192.png          # ícone do Android
icon-512.png          # ícone grande / splash
favicon-32.png        # ícone da aba do navegador
og-image.png          # imagem do card de compartilhamento (1200×630)
```

## Créditos e referências

- **Fonte Barlow e Barlow Condensed:** Jeremy Tribby, via [Google Fonts](https://fonts.google.com/specimen/Barlow). Licença [SIL Open Font License 1.1](https://openfontlicense.org).
- **Conteúdo do cronograma:** baseado no Edital IBGE nº 03/2026 (com a retificação de 16/11/2026) e na apostila *Conhecimentos básicos para o Censo Agropecuário, Florestal e Aquícola* (IBGE/ENCE), publicados pela [Fundação Cesgranrio](https://www.cesgranrio.org.br) para o processo seletivo do [IBGE](https://www.ibge.gov.br).
- **Nomes das aulas:** citados apenas como referência do curso que a pessoa usa para estudar ([Gran](https://www.grancursosonline.com.br)). Este projeto não tem relação com o Gran, a Cesgranrio ou o IBGE.
- Ícones do app e da interface desenhados no próprio projeto.

## Versões

- **v2.1.0** (19/11/2026): card de compartilhamento (Open Graph), ícone na aba do navegador e foto de perfil salva só no aparelho.

- **v2.0.0** (19/11/2026): calendário mensal, tarefas atrasadas passam para o dia seguinte, gráfico de andamento do edital por matéria, pausas por período, assuntos conferidos com o edital e a apostila (com a aula do Gran ou as páginas de cada um), revisões variadas, datas do edital, regras do dia da prova e tela de créditos.

- **v1.0.0** (19/11/2026): primeira versão, com perfis, cronograma do IBGE 2027, abas Hoje, Semana, Conteúdo e Prova, dias de estudo ajustáveis, PWA e cópia de segurança.

## Autor

Feito por **Jacó** ([@JacobbV](https://github.com/JacobbV)) · QyuDev.
