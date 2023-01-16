# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib import request
import json

t_count = 1
t_total_pages = 1
t_df_list = []
while t_count <= t_total_pages:
    print(t_count)
    m_api_url = 'https://api.dexie.space/v1/offers?offered=col1z0ef7w5n4vq9qkue67y8jnwumd9799sm50t8fyle73c70ly4z0ws0p2rhl&status=0&sort=date_found&compact=true&page_size=100&page=' + str(t_count)

    r_source = request.urlopen(m_api_url).read()
    rare_soup = BeautifulSoup(r_source, 'html.parser')
    t_json = json.loads(rare_soup.prettify())
    t_total_count = int(t_json['count'])
    t_total_pages =  np.ceil(t_total_count / 100)
    
    m_xch_friends_df = pd.json_normalize(t_json,record_path = ['offers'])
    m_xch_friends_df = m_xch_friends_df[m_xch_friends_df.loc[:,'offered'].apply(lambda x: len(x) == 1)]

    
    m_xch_friends_df.loc[:,'offered_nft_id'] = m_xch_friends_df.loc[:,'offered'].apply(lambda x: x[0]['name'])
    m_xch_friends_df.loc[:,'price'] = m_xch_friends_df.loc[:,'requested'].apply(lambda x: x[0]['amount'] if x[0]['name'] == 'Chia' else np.nan)
    
    m_xch_friends_df.loc[:,'offered_nft_id'] = m_xch_friends_df.loc[:,'offered_nft_id'].apply(lambda x: int(x.split('#')[1]))
    m_xch_friends_df = m_xch_friends_df.loc[:,['offered_nft_id','price']]
    
    m_xch_friends_df = m_xch_friends_df.set_index('offered_nft_id')
    t_df_list.append(m_xch_friends_df)
    
    t_count = t_count + 1

t_all_friends_df = pd.concat(t_df_list)
t_all_friends_df_sort = t_all_friends_df.sort_values('price')
t_all_friends_df_unique = t_all_friends_df_sort[~t_all_friends_df_sort.index.duplicated(keep='first')]
