#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
from nltk.tokenize import wordpunct_tokenize
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

NOTES = [
    ("crushing chest pain radiating to left arm, sweating and nausea", "urgent"),
    ("mild ankle sprain after fall, able to bear weight", "routine"),
    ("severe shortness of breath and oxygen saturation dropping", "urgent"),
    ("sore throat for two days, eating and drinking fine", "routine"),
    ("confused with high fever and low blood pressure", "urgent"),
    ("minor wrist discomfort after gym, no swelling", "routine"),
    ("tachypnoea, rigors and possible sepsis", "urgent"),
    ("small finger cut, bleeding controlled, stable", "routine"),
    ("new chest tightness with dizziness", "urgent"),
    ("mild headache, no red flag symptoms", "routine"),
    ("persistent vomiting with abdominal guarding", "urgent"),
    ("old knee pain flare, walking independently", "routine"),
]

STOPWORDS = {
    "the", "a", "an", "and", "or", "with", "to", "of", "for", "on", "in", "no", "after", "is", "are",
    "was", "were", "be", "been", "being", "at", "by", "from", "as", "it", "this", "that"
}


def preprocess(text):
    tokens = [t.lower() for t in wordpunct_tokenize(text)]
    return [t for t in tokens if t.isalpha() and t not in STOPWORDS]


def run_nltk_analysis(save_path='task3_token_chart.png'):
    urgent_tokens = []
    routine_tokens = []

    for text, label in NOTES:
        cleaned = preprocess(text)
        if label == 'urgent':
            urgent_tokens.extend(cleaned)
        else:
            routine_tokens.extend(cleaned)

    urgent_count = Counter(urgent_tokens)
    routine_count = Counter(routine_tokens)

    top_urgent = urgent_count.most_common(8)
    top_routine = routine_count.most_common(8)

    print('Top urgent tokens:', top_urgent)
    print('Top routine tokens:', top_routine)

    labels = sorted(set([w for w, _ in top_urgent] + [w for w, _ in top_routine]))
    u_vals = [urgent_count.get(w, 0) for w in labels]
    r_vals = [routine_count.get(w, 0) for w in labels]

    x = range(len(labels))
    plt.figure(figsize=(12, 5))
    plt.bar([i - 0.2 for i in x], u_vals, width=0.4, color='crimson', label='Urgent')
    plt.bar([i + 0.2 for i in x], r_vals, width=0.4, color='royalblue', label='Routine')
    plt.xticks(list(x), labels, rotation=45, ha='right')
    plt.ylabel('Token count')
    plt.title('Token counts after NLTK preprocessing')
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=180)
    plt.close()


def run_sklearn_classifier():
    texts = [t for t, _ in NOTES]
    y = [1 if label == 'urgent' else 0 for _, label in NOTES]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, y, test_size=0.25, random_state=42, stratify=y
    )

    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ('clf', LogisticRegression(max_iter=300, random_state=42))
    ])

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    print('Accuracy:', round(accuracy_score(y_test, pred), 3))
    print('Confusion matrix:\\n', confusion_matrix(y_test, pred))
    print('Classification report:\\n', classification_report(
        y_test, pred, target_names=['routine', 'urgent'], digits=3
    ))

    new_note = 'patient with crushing chest pain and sweating'
    new_pred = model.predict([new_note])[0]
    print('New note prediction:', 'urgent' if new_pred == 1 else 'routine')


if __name__ == '__main__':
    run_nltk_analysis('task3_token_chart.png')
    run_sklearn_classifier()
