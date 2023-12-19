# Database (cloud Firestore)

This is a very simple rough draft of the database structure. It is subject to change.

Collections :

## Questions

### Doc structure (question_id)

```json
{
    "title": "Question title",
    "body": "Question body",
    "tags": ["tag1", "tag2", "tag3"],
    "difficulty": 1, // 1, 2, 3
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "metadata": {
        "source": "Question source" // e.g., website, interview
    },
    "answers": [
        {
            "answer_id": "answer_id1",
            "preview": "Short preview of the answer"
        },
        // More answers
    ]
}

```

## Answers

### Doc structure (answer_id)

```json
{
    "question_ref": "Reference to Question Document", // Firestore's `Reference` data type to create a direct link to the corresponding question. This makes querying more efficient.
    "body": "Full Answer body",
    "author": "Answer author", // e.g., LLM model, human
    "score": 0.5, // 0.0 - 1.0
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "similarities": {
        "answer_id1": 0.5,
        "answer_id2": 0.3,
        // More similarities
    },
    "metadata": {
        "source": "Answer source" // e.g., website, generated
    }
}

```
