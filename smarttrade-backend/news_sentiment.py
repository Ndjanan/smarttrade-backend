import requests
import time

# CONFIGURATION
OPENAI_API_KEY = "VOTRE_CLE_API_OPENAI"        # Remplace par ta clé OpenAI
DEEPSEEK_API_KEY = "VOTRE_CLE_API_DEEPSEEK"    # Remplace par ta clé DeepSeek

## openai.api_key = OPENAI_API_KEY  # Commenté pour retirer l'analyse GPT

# 1. Récupérer les dernières actualités Google News

def fetch_google_news(query="forex", lang="fr", max_results=10):
    url = f"https://newsapi.org/v2/everything?q={query}&language={lang}&pageSize={max_results}&apiKey={GOOGLE_NEWS_API}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["articles"]


# 3. Analyse de sentiment avec DeepSeek

def analyze_with_deepseek(article):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": f"Voici une actualité financière : {article['title']}\n{article['description']}\nAnalyse le sentiment (positif, négatif, neutre) et donne une recommandation de trading (acheter, vendre, attendre)."}
        ]
    }
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

# 4. Fonction principale pour tout automatiser

def get_news_sentiment_and_decision():
    articles = fetch_google_news()
    results = []
    for article in articles:
        try:
            deepseek_result = analyze_with_deepseek(article)
            results.append({
                "title": article["title"],
                "deepseek": deepseek_result
            })
            time.sleep(1)  # Pour éviter le spam API
        except Exception as e:
            results.append({"title": article["title"], "error": str(e)})
    return results

def get_deepseek_recommendation_for_bot():
    decisions = get_news_sentiment_and_decision()
    # On cherche la première recommandation actionable
    for d in decisions:
        if "deepseek" in d and d["deepseek"]:
            # Extrait la recommandation de la réponse DeepSeek
            rec = d["deepseek"].lower()
            if "acheter" in rec:
                return "buy"
            elif "vendre" in rec:
                return "sell"
            elif "attendre" in rec or "neutre" in rec:
                return "hold"
    return "hold"

if __name__ == "__main__":
    decisions = get_news_sentiment_and_decision()
    for d in decisions:
        print("Actualité:", d["title"])
        print("Analyse DeepSeek:", d.get("deepseek"))
        print("---")
