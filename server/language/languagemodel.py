# # -*- coding: utf-8 -*-
# """languageModel.ipynb

# Automatically generated by Colaboratory.

# Original file is located at
#     https://colab.research.google.com/drive/1xgjrXx9-EXOK3pnFnNxvZp81ALMrnQzc
# """

# # https://nlu.johnsnowlabs.com/docs/en/install
# # ! pip install nlu pyspark==3.0.1
# ! pip install nlu pyspark==3.0.1

# import nlu

# nlu.load('emotion').predict('wow that was easy')

# import pandas as pd
# import numpy as np
# import seaborn as sns
# from sklearn.metrics.pairwise import cosine_similarity
# import matplotlib.pyplot as plt

# max_rows = 20000

# # from movie set code
# df = pd.read_csv(
#     "movie_lines.tsv", 
#     encoding='utf-8-sig', 
#     sep='\t', 
#     error_bad_lines=True, 
#     header = None,
#     names = ['lineID', 'charID', 'movieID', 'charName', 'text'],
#     index_col=['lineID']
# )

# df = df.iloc[0:max_rows,:]
# df = df.rename(columns={"text":"Title"})


# hints = ['I want to get something Taiwanese to eat at Din Tai Fung', 
#          'Wanna grab a strong blend coffee at Starbucks?',
#          'Stay within limits today',
#          'I love extremes only',
#          'So tired and sleepy',
#          'Let\'s watch a movie and entertain ourselves',
#          'I want to keep watching the movie',
#          'I want some caffeine in my blood',
#          'Be adventurous and proceed into the cockpit',
#          'Go and take rest at your seat',
#          'Help the captain',
#          'Help the deputy take power from the captain',
#          'Get help to save everyone',
#          'None of your business'
#          ]

# for i in range(len(hints)):
#   df.loc[len(df.index)] = [f'u{i*5+1}', f'm{i+1}', 'KUNAL', hints[i]]
# # df.loc[len(df.index)] = ['u66', 'm5', 'KUNAL','I want to get something Taiwanese to eat at Din Tai Fung'] 
# # df.loc[len(df.index)] = ['u67', 'm5', 'CALVIN','Wanna grab a strong blend coffee at Starbucks?'] 
# # df.loc[len(df.index)] = ['u31', 'm6', 'MCKINLEY','Stay within limits today']
# # df.loc[len(df.index)] = ['u622', 'm6', 'CALVIN','I love extremes only']  
# # df.loc[len(df.index)] = ['u21', 'm13', 'SEBASTIAN','So tired and sleepy'] 
# # df.loc[len(df.index)] = ['u25', 'm12', 'FAITH','Let\'s watch a movie and entertain ourselves'] 
# # df.loc[len(df.index)] = ['u46', 'm10', 'PHIL','I want to keep watching the movie'] 
# # df.loc[len(df.index)] = ['u21', 'm13', 'SAM','I want some caffeine in my blood'] 
# # df.loc[len(df.index)] = ['u41', 'm16', 'JOEY','Be adventurous and proceed into the cockpit'] 
# # df.loc[len(df.index)] = ['u43', 'm56', 'JOHN','Go and take rest at your seat'] 
# # df.loc[len(df.index)] = ['u46', 'm15', 'TOM','Help the captain'] 
# # df.loc[len(df.index)] = ['u48', 'm11', 'CARLOS','Help the deputy take power from the captain'] 
# # df.loc[len(df.index)] = ['u84', 'm63', 'KATE','Get help to save everyone'] 
# # df.loc[len(df.index)] = ['u86', 'm65', 'CHANG','None of your business'] 
# df

# import nlu
# pipe = nlu.load('embed_sentence.bert')
# predictions = pipe.predict(df.Title, output_level='document')
# predictions

# ## Calculate distance between all pairs of sentences in DF 
# e_col = 'sentence_embedding_bert'

# def get_sim_df_for_iloc(sent_iloc, predictions=predictions,e_col=e_col, pipe=pipe):
#   # This function calculatse the distances for one sentences at  predictions[sent_iloc] to all other sentences in predictions using the embedding defined by e_col 
#   # put embeddings in matrix
#   embed_mat = np.array([x for x in predictions[e_col]])
#   # calculate distance between every embedding pair
#   sim_mat = cosine_similarity(embed_mat,embed_mat)
#   print("Similarities for Sentence : " + df.iloc[sent_iloc].Title)
#   # write sim scores to df
#   df['sim_score'] = sim_mat[sent_iloc]
#   return df 

# sentence_to_compare=33
# sim_df_for_one_sent = get_sim_df_for_iloc(sentence_to_compare,predictions,e_col)
# sim_df_for_one_sent.sort_values('sim_score', ascending = False)

# def viz_sim_df_for_one_sent( sent_iloc=0, N = 40, sim_df_for_one_sent=sim_df_for_one_sent):
#   # Plots the N most similar sentences in our dataframe for sentence at position sent_iloc
#   sim_df_for_one_sent = get_sim_df_for_iloc(sent_iloc)
  
#   sim_df_for_one_sent.index = sim_df_for_one_sent.Title
#   sent = sim_df_for_one_sent.iloc[sent_iloc].Title
#   ax = sim_df_for_one_sent.sort_values('sim_score', ascending = False).iloc[:N].sim_score.plot.barh(title=f'The {N} most similar sentences in our dataset for the sentence \n"{sent}"', figsize=(20,14))
#   ax.set_xlim(0.8, 1)

# # Just put in any number and get the plot for similarities of the sentence at df.iloc[i]
# viz_sim_df_for_one_sent(0)

# def get_sim_df_total( predictions,string_to_embed, e_col=e_col ,pipe=pipe):

#   # This function calculates the distances between every sentence pair. Creates for ever sentence a new column with the name equal to the sentence it comparse to 
#   # put embeddings in matrix
#   embed_mat = np.array([x for x in predictions[e_col]])
#   # calculate distance between every embedding pair
#   sim_mat = cosine_similarity(embed_mat,embed_mat)
#   # for i,v in enumerate(sim_mat): predictions[str(i)+'_sim'] = sim_mat[i]
#   for i,v in enumerate(sim_mat): 
#     s = predictions.iloc[i].document
#     predictions[s] = sim_mat[i]

#   return predictions 

# sim_matrix_df = get_sim_df_total(predictions, string_to_embed='get starbucks' )
# sim_matrix_df

# non_sim_columns  = ['text','document',e_col]

# def viz_sim_matrix_first_n(num_sentences=20, sim_df = sim_matrix_df):
#   # Plot heatmap for the first num_sentences
#   fig, ax = plt.subplots(figsize=(20,14)) 
#   sim_df.index = sim_df.document
#   sim_columns = list(sim_df.columns)
#   for b in non_sim_columns : sim_columns.remove(b)
#   # sim_matrix_df[sim_columns]
#   ax = sns.heatmap(sim_df.iloc[:num_sentences][sim_columns[:num_sentences]]) 

#   ax.axes.set_title(f"Similarity matrix for the first {num_sentences} in the dataset",)

# viz_sim_matrix_first_n()

# def viz_sim_matrix_from_to(start_iloc,end_iloc, sim_df = sim_matrix_df):
#   # Plot heatmatrix for sentences at df.iloc[start:end]   
#   fig, ax = plt.subplots(figsize=(25,14)) 
#   sim_df.index = sim_df.document
#   sim_columns = list(sim_df.columns)
#   for b in non_sim_columns : sim_columns.remove(b)


#   ax = sns.heatmap(sim_df.iloc[start_iloc:end_iloc][sim_columns[start_iloc:end_iloc]]) # +2 because first 2 cols are not sim_scores

#   ax.axes.set_title(f"Similarity matrix for the sentences at positions df.iloc[{start_iloc}:{end_iloc}] in the dataset",)

# viz_sim_matrix_from_to(750,800)

# def get_sim_df_for_string(predictions,e_col, string_to_embed,pipe=pipe):
#   # Creates a Dataframe which has a sim_score column which describes the similarity with the string_to_embed variable

#   # put predictions vectors in matrix
#   embed_mat = np.array([x for x in predictions[e_col]])

#   # embed string input string
#   embedding = pipe.predict(string_to_embed).iloc[0][e_col]

#   # Replicate embedding for input string 
#   m = np.array([embedding,]*len(df))
#   sim_mat = cosine_similarity(m,embed_mat)

#   #write sim score
#   df['sim_score'] = sim_mat[0]


#   return df


# question = 'How to get coffee' 
# sim_df = get_sim_df_for_string(predictions,e_col, question )
# ax = sim_df.sort_values('sim_score', ascending = False).iloc[:20][['sim_score','Title']].plot.barh(title = f"Most similar Sentences for sentence\n'{question}'", figsize=(20,16))
# ax.set_xlim(0.8, 1)

# def viz_sim_df_for_one_sent( question='How to install linux dualboot', e_col='embed_sentence_bert_embeddings', N = 40, sim_df_for_one_sent=sim_df_for_one_sent):
#   # Plots the N most similar sentences in our dataframe for sentence at position sent_iloc
#   sim_df = get_sim_df_for_string(predictions,e_col,question )
#   sim_df.index = sim_df.Title
#   sim_df.sort_values('sim_score', ascending = False).iloc[:N][['sim_score','Title']].plot.barh(title = f"Most similar Sentences for sentence\n'{question}'", figsize=(20,14))
#   ax.set_xlim(0.8, 1)

# question = 'It\'s cold outside'
# viz_sim_df_for_one_sent(question,e_col)

# multi_pipe = nlu.load('use en.embed_sentence.electra embed_sentence.bert')
# multi_embeddings = multi_pipe.predict(df.Title,output_level='document')
# # multi_embeddings = multi_pipe.predict(df.Title)

# multi_embeddings

# def get_sim_df_for_string_multi(predictions,embed_col_names, string_to_embed,pipe=multi_pipe):
#   # Creates a Dataframe which has a sim_score column which describes the similarity with the string_to_embed variable
#   # This accumulates the distances of all embeddings in embed_col_names and normalizes it by dividing by len(embed_col_names)
#   #make empty simmilarity matrix which will store the aggregated simmilarities between different embeddings
#   predictions.dropna(inplace=True)
#   cum_sim = np.zeros((len(predictions),len(predictions)))

#   # embed with all embedders currently loaded in pipeline
#   embeddings = pipe.predict(string_to_embed).iloc[0]

#   #loop over all embeddings columns and accumulate the pairwise distances with string_to_embed into cum_sim
#   for e_col in embed_col_names:
#     # get the current embedding for input string
#     embedding = embeddings[e_col]  
#     # stack embedding vector for input string
#     m = np.array([embedding,]*len(predictions)) 
#     # put df vectors in np matrix
#     embed_mat = np.array([x for x in predictions[e_col]]) 
#     # calculate new similarities
#     sim_mat = cosine_similarity(m,embed_mat) 
#   # accumulate new simmilarities in cum_sum
#     cum_sim += sim_mat  

#   predictions['sim_score'] = cum_sim[0]/len(embed_col_names) 
#   return predictions

# question = 'I want to eat at Din Tai Fung'
# electra_col = 'sentence_embedding_electra'
# use_col = 'sentence_embedding_use'
# bert_col = 'sentence_embedding_bert'
# col_names = [electra_col,use_col, bert_col]

# sim_df = get_sim_df_for_string_multi(multi_embeddings,col_names, question )
# sim_df.index = sim_df.document
# sim_df.sort_values('sim_score', ascending = False).iloc[:15][['sim_score','document']].plot.barh(title = f"Most similar Sentences for sentence\n'{question}'", figsize=(20,14))

# def viz_sim_df_for_one_sent_multi_embed( question='Let\'s get coffee', e_cols=col_names, N = 40, multi_embeddings=multi_embeddings):
#   # Plots the N most similar sentences in our dataframe for sentence at position sent_iloc
#   sim_df = get_sim_df_for_string_multi(multi_embeddings,col_names, question )
#   sim_df.index = sim_df.document
#   return sim_df.sort_values('sim_score', ascending = False)
#   # sim_df.sort_values('sim_score', ascending = False).iloc[:N][['sim_score','document']].plot.barh(title = f"Most similar Sentences for sentence\n'{question}'",figsize=(20,14))

#   ax.set_xlim(0.8, 1)

# all_hints = []
# i = 0
# for i in range(len(hints)):
#   print(i)
#   col_names = [electra_col,use_col, bert_col]
#   ordered_hints = viz_sim_df_for_one_sent_multi_embed(hints[i], col_names)
  
#   ordered_hints['id'] = range(i*100, i*100+len(ordered_hints))
#   ordered_hints = ordered_hints.iloc[0:100, :][['id','document','sim_score']]
#   ordered_hints
#   all_hints = all_hints + ordered_hints.values.tolist()

# print(all_hints)

# df = pd.DataFrame(all_hints,columns=['id','hint','sim_score'])
# df

# # from google.colab import drive
# # drive.mount('drive')

# df.to_csv('hints.csv')
# !cp hints.csv "drive/My Drive/"
