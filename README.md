# Steam Chatbot
##### Projeto desenvolvido para a disciplina | IF704 — Processamento de Linguagem Natural | Computer Science - UFPE

---

O SteamCB é um chatbot voltado para o dóminio de jogos do marketplace da steam. Conversando com o SteamDB o usuário **consegue** _comprar_, _buscar_ e _descobrir_ novos _jogos_, bem como também fazer _Q&A_ sobre os mais variados jogos de seu interesse. 
<br/><br/>
| **user** 	| **SteamCB** 	|
|:---:	|:---:	|
| _"yo, any good FPS games for windows released on 2012?"_ 	| "Yes, you may like Counter-Strike:Global Offense" 	|
| _"Hii, I wanna buy Hollow Knight"_ 	| "Fine, buying Hollow Knight, are you sure?" 	|
| _"who is the developer of Skyrim?"_ 	| "That's Bethesda, for sure!" 	|
| _"Sooo... What may I explore on Hollow Knight?"_ 	| "You can explore twisting caverns!!" 	|
| _"What can I do on Celeste?"_ 	| "You may Brave hundreds of hand-crafted challenges,  uncover devious secrets, and piece together the  mystery of the mountain." 	|
| _"When Frostpunk was released?"_ 	| "Frostpunk was released on 24 Apr, 2018" 	|

<br/><br/>

Segue a tabela com as intenções suportadas pelo SteamCB e bem como suas respectivas entidades. Logo depois temos o dialog-flow do bot. 

|    **Intenção**   	| **Descrição**                                        	| **Entidades**                                              	|
|:-----------------:	|------------------------------------------------------	|------------------------------------------------------------	|
|   **_BuyGame_**   	| _Comprar um jogo_                                    	| _game_title_                                               	|
| **_ReqShowGame_** 	| _Pedir sugestão de um jogo_                          	| _game_title, game_tag, release_date,  developer, platform_ 	|
| **_ReqGameInfo_** 	| _Q&A sobre informações textuais não estruturadas de um jogo_ 	| None                                                       	|
|    **_Affirm_**   	| _Confirmar uma intenção, ação ou informação_         	| None                                                       	|
|     **_Deny_**    	| _Negar uma intenção, ação ou informação_             	| None                                                       	|

![image](https://github.com/AmadeoNeto/steam_chatbot/assets/61971951/9475ca76-2dfa-436a-845f-6953c037f67b)

### Datasets
Usamos o [Steam Store Games dataset](https://www.kaggle.com/datasets/nikdavis/steam-store-games) como base de informação para os jogos vendidos na steam. Entretando, não achamos dados prontos para classificação de intenção e extração de entidade nesse domínio. Por isso, lançamos mão de vários LLMs para confecionar os datasets de intenção e de extração compostos por templates de dialogos que imitam os mais diversos perfis de usuários.

- [ChatGPT](https://chat.openai.com/)
- [GPT-4](https://chat.openai.com/)
- [Lamma2](https://llama.meta.com/)
- [Mixtral 8x7B](https://chat.mistral.ai/chat)

Devido a limitações requisições por parte das APIs dos LLMs e também por limitações de hardware tivemos ampliar o dataset replicando os dialogos de intenções enquanto alteravamos os _slots_ das entidades com dados extraidos do Steam Store Games Dataset. Usamos o AutoTokenizer do HuggingFace e o Tokenizer do Spacy para criar o tokens do dataset.

### Classificador e Extrator
Os notebooks para os modelos de extratores e classificadores estão em `/models/collabs/`. 

Quanto ao classificador fora utilizados Linear SVM, CNN, BI-LSTM e o DistilBERT (transformer). Porém, o melhor classificador foi o DIETClassifier do framework rasa. 

Já em relação ao extrator treinamos uma rede BI-LSTM e realizamos o fine-tunning to transformer BERT para a task de ner, porém o DIETClassifier do rasa ainda prevaleceu como a melhor opção.

### Q&A 
O usuário pode requisitar informações mais variadas sobre algum jogo que vão desde a data do lançamento até curiosidades à exemplo dos personagens principais ou do que pode ser feito no jogo. Para isso indentificamos a intenção de Q&A e realizamos um ranquamento por semelhança no nosso banco de dados pelo título do jogo. Após isso, usamos um Transformer refinado para task de Answering alimentado desse texto não estruturado (Descrição do jogo) para gerar a resposta para a pergunta do usuário.  

### Frameworks utilizadas
- Rasa
- Spacy 
- TensorFlow
- PyTorch
- SQLite3
- Hugginface Ecosystem (Transformers, Dataset, Tokenizer)
