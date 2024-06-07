## Konfiguration

Um diese Anwendung lokal auszuführen, erstellen Sie eine `.streamlit/secrets.toml`-Datei im Stammverzeichnis des Projekts mit folgendem Inhalt:

```toml
[general]
anthropic_api_key = "your_anthropic_api_key_here"
```

## Konfiguration für Streamlit Cloud

Um diese Anwendung in St Cloud auszuführen, müssen Sie die API Keys in den Settings der Streamlit Cloud App unter 'Secrets' eintragen

Beispiel:
```
[openai]
api_key = "..."

[anthropic]
api_key = "..."

[google]
api_key = "..."
```
