import re

def convert_link_to_iframe_youtube(user):
        # Tenta buscar o ID do vídeo no link do YouTube
        match = re.search(r'v=([^&]+)', user)    
        if match:
            # Extrai o ID do vídeo
            newLink = match.group(1)
            # Gera o URL do iframe com autoplay, mute e loop
            iframe_url = f"https://www.youtube.com/embed/{newLink}?autoplay=1&mute=1&loop=1&start=20&rel=0&showinfo=0&enablejsapi=1"
            return iframe_url
        else:
            return None