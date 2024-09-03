from .utils import create_openai_client, create_system_message, update_conversation_memory, get_relevant_memory


def generate_response_stream(messages, conversation_memory):
    client = create_openai_client()

    system_message = create_system_message()

    # Extraire les informations pertinentes de la mémoire
    relevant_memory = get_relevant_memory(conversation_memory, [message['content'] for message in messages])

    # Ajouter les informations pertinentes au contexte
    memory_context = "Informations précédentes : " + ", ".join([f"{k}: {v}" for k, v in relevant_memory.items()])
    context_message = {"role": "system", "content": memory_context}

    # Ajouter une instruction pour des réponses plus naturelles
    natural_instruction = {"role": "system",
                           "content": "Répondez de manière naturelle et conversationnelle, en évitant les listes à puces et les formats trop structurés. Intégrez les informations de manière fluide dans votre discours."}

    full_messages = [system_message, context_message, natural_instruction] + messages

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=full_messages,
        max_tokens=10000,
        temperature=0.7,  # Augmenter légèrement la température pour plus de créativité
        stream=True
    )

    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            yield content

    # Mettre à jour la mémoire de la conversation
    new_info = extract_important_info(full_response)
    update_conversation_memory(conversation_memory, new_info)

def extract_important_info(response):
    # Fonction pour extraire les informations importantes de la réponse
    # Cette fonction pourrait être améliorée avec du NLP pour une extraction plus précise
    important_info = {}
    if "prix" in response.lower():
        # Extraction basique du prix (à améliorer)
        price_index = response.lower().index("prix")
        price_end = response.find("€", price_index)
        if price_end != -1:
            price = response[price_index:price_end].split()[-1]
            important_info["dernier_prix_mentionné"] = price + "€"

    # Ajouter d'autres extractions d'informations importantes ici

    return important_info