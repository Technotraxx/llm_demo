prompt_templates = {
    "Default Template": "Zusammenfassung in 5 Wörtern!\n\n{text}",
    "Template A": "<input>{text}</input>\n\nCreate a short and memorable summary of the previous text input.\n1. One sentence summary\n2. One paragraph summary\n3. 5 important concepts or definitions or theories",
    "Template B": "Here is a text file: <text>{text}</text>\n\nPlease do the following:\n1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)\n2. Write the Methods section as a recipe from the Moosewood Cookbook. (In <moosewood_methods> tags.)\n\3. Compose a short poem epistolizing the results in the style of Homer. (In <homer_results> tags.)",
    "Template C": "Prompt text for template C",
    "Template D": "Prompt text for template D",
    "Template E": "Prompt text for template E",
    "Template for Gaming Article Fact Extraction": (
        "Please carefully read the following text and extract the requested information from it:\n"
        "<text>\n"
        "{text}\n"
        "</text>\n\n"
        "Extract the following details:\n\n"
        "- date_time: The date and time the article was published, if available. Format as 'DD.MM.YYYY | HH:MM'.\n"
        "- author: The name of the article's author, if available.\n"
        "- title: The full title of the article.\n"
        "- facts: A list of the key facts presented in the article. Each fact should be a separate item in the list.\n"
        "- keywords: A list of important keywords from the article.\n"
        "- genre_and_type: A list of objects, with each object containing:\n"
        "  - game: The name of a game mentioned\n"
        "  - genre: The genre of that game\n"
        "  - type: The type of game - single player, multiplayer, or co-op\n"
        "- summary: Provide a concise 2-3 sentence summary of the key points of the article.\n"
        "- unusual_or_contradictory: Note anything unusual or contradictory stated in the article. If there is nothing unusual or contradictory, say 'Nichts Ungewöhnliches oder Widersprüchliches aufgefallen.'\n\n"
        "Important: Only extract information that is explicitly stated in the provided text. Do not make assumptions or add any information that is not directly mentioned.\n\n"
        "Please provide your full result as markdown text with headlines, subheadings, bulletpoints, text or lists."
    )
}
