prompt_templates = {
    "Default Template": "Zusammenfassung in 5 Wörtern!\n\n{text}",
    "Template A": "<input>{text}</input>\n\nCreate a short and memorable summary of the previous text input.\n1. One sentence summary\n2. One paragraph summary\n3. 5 important concepts or definitions or theories",
    "Template B": "Here is a text file: <text>{text}</text>\n\nPlease do the following:\n1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)\n2. Write the Methods section as a recipe from the Moosewood Cookbook. (In <moosewood_methods> tags.)\n\3. Compose a short poem epistolizing the results in the style of Homer. (In <homer_results> tags.)",
    "Template C": "Prompt text for template C",
    "Template D": "Prompt text for template D",
    "Template E": "Prompt text for template E",
    "Template GameStar": "Please carefully read the following text and extract the requested information from it:
<text>
{text}
</text>

Extract the following details:

- date_time: The date and time the article was published, if available. Format as 'DD.MM.YYYY | HH:MM'.
- author: The name of the article's author, if available. 
- title: The full title of the article.
- facts: A list of the key facts presented in the article. Each fact should be a separate item in the list.
- keywords: A list of important keywords from the article.
- genre_and_type: A list of objects, with each object containing:
  - game: The name of a game mentioned
  - genre: The genre of that game
  - type: The type of game - single player, multiplayer, or co-op
- summary: Provide a concise 2-3 sentence summary of the key points of the article.
- unusual_or_contradictory: Note anything unusual or contradictory stated in the article. If there is nothing unusual or contradictory, say 'Nichts Ungewöhnliches oder Widersprüchliches aufgefallen.'

Important: Only extract information that is explicitly stated in the provided text. Do not make assumptions or add any information that is not directly mentioned.

Please provide your full result inside <result> tags."
}
