from sklearn.metrics.pairwise import cosine_similarity

def evaluate(explainer, test_data):
    correct = 0
    total = 0

    for item in test_data:
        result = explainer.retrieve(
            item["error_message"],
            item.get("buggy_code", ""),
            item["language"]
        )

        if not result or len(result) != 2:
            continue

        retrieved, _ = result
        if not retrieved:
            continue

        total += 1

        true_vec = explainer.model.encode([item["explanation"]])
        pred_vec = explainer.model.encode([retrieved["explanation"]])

        sim = cosine_similarity(true_vec, pred_vec)[0][0]

        if sim > 0.6:
            correct += 1

    return round((correct / total) * 100, 2) if total else 0