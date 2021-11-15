# Proof of Legacy Identity

```

def download_identity():
  # get basic hard facts
  ssn_html = interactive_session('https://ssn.gov')
  name, bday, last4SsnDigits = extract(ssn_html)

  # get Google data
  google_data.zip = interactive_session('goo.gl/account')
 
  # get YT history
  list[html] vid_descriptions = interactive_session('yt.com/history')

  # get Spotify data
  list[html] fav_artists = interactive_session('spotify.com/favorites')
  pca(bert_embeddings())

  # get FB data
  list[html] chat_msgs = interactive_session('fb.com/chats')
  
  id_data =to_json(name, bday, ..., chatmsg)
  signatures = sign_fields(id_data)
  offer_json_download(id_data, signatures)
  


def create_user():
   

def prove_identity(address, id_data, signatures): 
  
  


# Prove that embeddings + name, etc history is close to previous one
# compare to enclave-signed web data stored on users devices / cloud
# encrypted by password, massively duplicated
# 

 
```
