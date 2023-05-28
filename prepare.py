import os
import gdown


if not os.path.exists('datasets_prep'):
    os.mkdir('datasets_prep')


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
