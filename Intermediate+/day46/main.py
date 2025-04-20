import os,requests,time
from googleapiclient.discovery import build
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
from tokenizer import authenticate_youtube

######################################################pesquisar musicas na Billboard
def search_songs_on_billboard(year):
    ano = datetime(year=year, month=1, day=1).strftime("%Y-%m-%d")
    url = f"https://www.billboard.com/charts/hot-100/{ano}"

    billboard_header = {"User-Agent": os.getenv('BROWSER_HEADER')}

    response = requests.get(url=url, headers=billboard_header)
    response.raise_for_status()

    page = BeautifulSoup(response.text, 'html.parser')
    song_names_spans = page.select("li ul li h3")
    song_names = [song.getText().strip() for song in song_names_spans]

    return song_names

###########################################################cria uma playlist no YouTube
def create_youtube_playlist(access_token, playlist_title):
    # auth
    youtube = build('youtube', 'v3', credentials=Credentials(token=access_token))

    # estrutura da playlist
    playlist_request = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': playlist_title,
                'description': 'Playlist criada via API com as 100 mais populares do Ano pela Billboard.',
                'tags': ['Billboard', 'Top 100']
            },
            'status': {
                'privacyStatus': 'unlisted'  # playlist nao listada
            }
        }
    )

    try:
        playlist_response = playlist_request.execute()
        playlist_id = playlist_response['id']  ################ID da playlist
        return playlist_id
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None

################################adiciona 66 musicas na playlist do YouTube (max de 10k quota per day)
def add_songs_to_playlist(access_token, playlist_id, song_titles):
    youtube = build('youtube', 'v3', credentials=Credentials(token=access_token))

    for song_title in song_titles:
        # busca no youtube
        search_request = youtube.search().list(
            part="snippet",
            q=song_title,  # nome da musica
            type="video"
        )

        try:
            search_response = search_request.execute()

            # pega ID do video
            if search_response['items']:
                video_id = search_response['items'][0]['id']['videoId']

                # Adiciona vídeo na playlist
                playlist_item_request = youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        'snippet': {
                            'playlistId': playlist_id,
                            'resourceId': {
                                'kind': 'youtube#video',
                                'videoId': video_id
                            }
                        }
                    }
                )

                try:
                    playlist_item_request.execute()
                    print(f"Adicionado {song_title} à playlist.")
                except HttpError as e:
                    print(f"Erro ao adicionar {song_title} à playlist: {e}")
            else:
                print(f"Resultado não encontrado para: {song_title}")
        except HttpError as e:
            print(f"Erro na busca por {song_title}: {e}")

##########################loop principal
def main():

    creds = authenticate_youtube()
    if not creds:
        print("Falha na autenticação.")
        return

    ano = int(input("Para qual ano você deseja viajar?\n"))
    while ano>datetime.today().year-1 or ano<1958:
        print('Ano sem registros. Tente de novo')
        ano = int(input("Para qual ano você deseja viajar?\n"))
    song_titles = search_songs_on_billboard(ano)

    playlist_title = f"Billboard {ano} Hits"
    playlist_id = create_youtube_playlist(creds, playlist_title)
    if not playlist_id:
        print("Falha ao criar a playlist.")
        return
    print(f"Playlist criada com o ID: {playlist_id}")

    add_songs_to_playlist(creds, playlist_id, song_titles)
    time.sleep(3)
if __name__ == '__main__':
    main()