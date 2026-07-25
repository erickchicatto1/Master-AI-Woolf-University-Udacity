# Define our initial prompt
# No changes needed in this cell

initial_prompt = """
Analyze the following recipe and determine whether it satisfies each dietary restriction in the list.
For each restriction, classify it as "satisfied", "not satisfied", or "undeterminable" based on the recipe information.

Recipe: {{ recipe_name }}

Ingredients:
{{ recipe_ingredients }}

Instructions:
{{ recipe_instructions }}

Dietary Restrictions to Check:
{{ dietary_restrictions }}

Please provide your response in JSON format.
"""


def format_prompt(recipe, prompt):
    ingredients_str = "\n".join(
        ["- " + ingredient for ingredient in recipe["ingredients"]]
    )
    instructions_str = "\n".join(
        [
            f"{i + 1}. {instruction}"
            for i, instruction in enumerate(recipe["instructions"])
        ]
    )
    restrictions_str = ", ".join(dietary_restrictions)

    return jinja2.Template(prompt).render(
        recipe_name=recipe["name"],
        recipe_ingredients=ingredients_str,
        recipe_instructions=instructions_str,
        dietary_restrictions=restrictions_str,
    )
