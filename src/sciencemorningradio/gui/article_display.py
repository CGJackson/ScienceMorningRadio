import toga
from toga.style.pack import Pack

import sciencemorningradio.article as article

def display_article(article: article.Article):
    block = toga.Box(style=Pack(margin=10, background_color="white",direction="column"))
    block.add(toga.Label(f"title: {article.title}"))
    block.add(toga.Label(f"authors: {article.authors}"))
    block.add(toga.Label(f"arxiv id: {article.id}"))
    block.add(toga.Label(f"DOI: {article.doi}"))
    block.add(toga.Label(f"updated: {article.updated}"))
    return block