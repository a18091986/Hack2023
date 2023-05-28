import os
import gdown
import pickle as pkl
import pandas as pd

from recommendations_top import my_popularity_recommendation

if not os.path.exists('datasets_prep'):
    os.mkdir('datasets_prep')


if not os.path.exists('serialize'):
    os.mkdir('serialize')


gdown.download('https://drive.google.com/file/d/17YGTNHJFy6Z68NcorNF7IOFs1CTvcAbX/view?usp=sharing',
               output='datasets_prep/dict.csv', fuzzy=True, quiet=True)

gdown.download('https://drive.google.com/file/d/15eqbFGDZGXTxUVwhqQVs4GWsIbcjNwL4/view?usp=sharing',
               output='datasets_prep/groups_with_coords.csv', fuzzy=True, quiet=True)

gdown.download('https://drive.google.com/file/d/1cQihEHARXDghjULFKr3dAdMjSxamfSyG/view?usp=sharing',
               output='datasets_prep/recs_data_names.csv', fuzzy=True, quiet=True)

gdown.download('https://drive.google.com/file/d/1TzAunyOq5bjt7RnRSXFZeaSYNzK8g5IL/view?usp=sharing',
               output='datasets_prep/result_df_with_dist.csv', fuzzy=True, quiet=True)

gdown.download('https://drive.google.com/file/d/10qTIN9-ihmexpnb7s8HLTJy6h7zuEQDx/view?usp=sharing',
               output='datasets_prep/result.csv', fuzzy=True, quiet=True)

gdown.download('https://drive.google.com/file/d/1dbFDPJjqdo4O_gp3aqheE19UoH-h4Xg7/view?usp=sharing',
               output='datasets_prep/users_with_coords.csv', fuzzy=True, quiet=True)

gdown.download('https://drive.google.com/file/d/1VHetyqSWZvDD-bq5ZMN0j509Rh7NNPkU/view?usp=sharing',
               output='datasets_prep/users.csv', fuzzy=True, quiet=True)


top_recs = []
df = pd.read_csv('datasets_prep/result.csv')
list_rec = my_popularity_recommendation(df)
for i in list_rec:
    top_recs.append(df['line_3'][df['id_level3'] == i].head(1).reset_index().values.tolist()[0][1])
with open('serialize/top_recs.pkl', 'wb') as f:
    pkl.dump(top_recs, f)