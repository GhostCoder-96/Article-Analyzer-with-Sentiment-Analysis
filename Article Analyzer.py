import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article

# Download required NLTK data
nltk.download('punkt')

def summarize():
    url = utext.get("1.0", "end").strip()

    if not url:
        return
    
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
    except Exception:
        summary.config(state='normal')
        summary.delete('1.0', 'end')
        summary.insert('1.0', "Error retrieving article.")
        summary.config(state='disabled')
        return

    # Enable text fields for editing
    for widget in (title, author, publish, summary, sentiment):
        widget.config(state='normal')

    # Insert extracted data
    title.delete('1.0', 'end')
    title.insert('1.0', article.title)

    author.delete('1.0', 'end')
    author.insert('1.0', ', '.join(article.authors) if article.authors else "Unknown")

    publish.delete('1.0', 'end')
    publish.insert('1.0', str(article.publish_date) if article.publish_date else "Unknown")

    summary.delete('1.0', 'end')
    summary.insert('1.0', article.summary)

    # Sentiment Analysis
    analysis = TextBlob(article.text)
    sentiment_score = analysis.polarity
    sentiment_text = "POSITIVE" if sentiment_score > 0 else "NEGATIVE" if sentiment_score < 0 else "NEUTRAL"

    sentiment.delete('1.0', 'end')
    sentiment.insert('1.0', f'Sentiment: {sentiment_text}')

    # Disable fields after inserting text
    for widget in (title, author, publish, summary, sentiment):
        widget.config(state='disabled')

# GUI Setup
root = tk.Tk()
root.title("News Summarizer")
root.geometry('1200x600')

# Labels and Text Fields
tk.Label(root, text='Title').pack()
title = tk.Text(root, height=1, width=140, state='disabled', bg='#dddddd')
title.pack()

tk.Label(root, text='Author').pack()
author = tk.Text(root, height=1, width=140, state='disabled', bg='#dddddd')
author.pack()

tk.Label(root, text='Publishing Date').pack()
publish = tk.Text(root, height=1, width=140, state='disabled', bg='#dddddd')
publish.pack()

tk.Label(root, text='Summary').pack()
summary = tk.Text(root, height=20, width=140, state='disabled', bg='#dddddd')
summary.pack()

tk.Label(root, text='Sentiment Analysis').pack()
sentiment = tk.Text(root, height=1, width=140, state='disabled', bg='#dddddd')
sentiment.pack()

tk.Label(root, text='URL').pack()
utext = tk.Text(root, height=1, width=140)
utext.pack()

# Summarize Button
btn = tk.Button(root, text='Summarize', command=summarize)
btn.pack()

root.mainloop()
