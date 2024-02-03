from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from torch.utils.data import Dataset, DataLoader
import torch
import numpy as np


class CustomDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=30):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        tokens = self.tokenizer.encode(item, max_length=self.max_length, truncation=True)
        return {"input_ids": torch.tensor(tokens)}


easy_data = [
    "Écrivez une fonction pour additionner deux nombres.",
    "Créez une liste de nombres pairs jusqu'à 10.",
    "Inverser une chaîne de caractères.",
    # Ajoutez d'autres prompts d'exercices faciles
]

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
easy_dataset = CustomDataset(data=easy_data, tokenizer=tokenizer)

# Configuration du modèle GPT-2
config = GPT2Config.from_pretrained("gpt2")
easy_model = GPT2LMHeadModel.from_pretrained("gpt2", config=config)

# Entraînement du modèle avec les données factices (remplacez par un véritable ensemble de données)
easy_dataloader = DataLoader(easy_dataset, batch_size=1, shuffle=True)

optimizer = torch.optim.AdamW(easy_model.parameters(), lr=5e-5)

# Boucle d'entraînement factice (remplacez par un véritable entraînement)
for epoch in range(3):
    for batch in easy_dataloader:
        input_ids = batch["input_ids"].to(
            torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )
        labels = input_ids.clone()

        outputs = easy_model(input_ids, labels=labels)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# Sauvegarde du modèle (remplacez par un véritable chemin)
easy_model.save_pretrained("easy_model")
tokenizer.save_pretrained("easy_model")

# Exemple d'utilisation du modèle entraîné
prompt = "Écrivez une fonction pour trouver la somme des éléments d'une liste."
input_ids = tokenizer.encode(prompt, return_tensors="pt")
output = easy_model.generate(input_ids, max_length=50, num_return_sequences=1, temperature=0.7)
response = tokenizer.decode(output[0], skip_special_tokens=True)

print(f"Prompt: {prompt}")
print(f"Réponse générée: {response}")
