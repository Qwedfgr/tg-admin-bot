import json
import os

import dialogflow_v2 as dialogflow


def create_intent(display_name, training_phrases_parts, message_texts, parameters_parts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(PROJECT_ID)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.types.Intent.Message.Text(text=[message_texts])
    message = dialogflow.types.Intent.Message(text=text)

    parameters = []
    for parameter in parameters_parts:
        parameter_df = dialogflow.types.Intent.Parameter(
            display_name=parameter['name'],
            prompts=[parameter['prompts']],
            mandatory=True,
            entity_type_display_name=parameter['entity']
        )
        parameters.append(parameter_df)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
        parameters=parameters)

    intents_client.create_intent(parent, intent)


def train():
    with open("questions.json", "r", encoding='utf-8') as my_file:
        training_data = json.load(my_file)
    for intent_name, intent in training_data.items():
        create_intent(intent_name, intent['questions'], intent['answer'], intent['parameters'])


def get_answer(session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(PROJECT_ID, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

    return response.query_result.fulfillment_text, response.query_result.intent


def create_entity_type(project_id, display_name, kind):
    """Create an entity type with the given display name."""
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)
    entity_type = dialogflow.types.EntityType(
        display_name=display_name, kind=kind)

    response = entity_types_client.create_entity_type(parent, entity_type)

    print('Entity type created: \n{}'.format(response))
