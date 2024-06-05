prompt_templates = {
    "Default Template": """Here is an academic paper: <paper>{text}</paper>

    Please do the following:
    1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)
    2. Write the Methods section as a recipe from the Moosewood Cookbook. (In <moosewood_methods> tags.)
    3. Compose a short poem epistolizing the results in the style of Homer. (In <homer_results> tags.)
    """,
    "Template A": "<input>{text}</input>\n\nCreate a short and memorable summary of the previous text input.\n1. One sentence summary\n2. One paragraph summary\n3. 5 important concepts or definitions or theories",
    "Template B": "Here is an academic paper: <paper>{text}</paper>\n\nPlease do the following:\n1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)\n2. Write the Methods section as a recipe from the Moosewood Cookbook. (In <moosewood_methods> tags.)\n\3. Compose a short poem epistolizing the results in the style of Homer. (In <homer_results> tags.)",
    "Template C": "Prompt text for template C",
    "Template D": "Prompt text for template D",
    "Template E": "Prompt text for template E"
}
