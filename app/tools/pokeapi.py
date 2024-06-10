from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
import requests 
from pydantic import BaseModel,Field

class PokedexInput(BaseModel):
    pokemon_name: str = Field(description="Name of a Pokemon")

class PokedexTool(BaseTool):
    name = "pokedex"
    description = "Retrieves data about a Pokemon, such as name, height, weight, abilities, types."
    args_schema: Type[BaseModel] = PokedexInput

    def _run(self, pokemon_name: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Retrieve information about a Pokemon."""
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url)
        
        if response.status_code == 200:
            pokemon_data = response.json()
            pokemon_info = {
                "name": pokemon_data["name"],
                "height": pokemon_data["height"],
                "weight": pokemon_data["weight"],
                "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]],
                "types": [type_data["type"]["name"] for type_data in pokemon_data["types"]]
            }
            return f"La información sobre el pokemon {pokemon_name} es: {pokemon_info}"
        else:
            return None

    async def _arun(
        self, pokemon_name: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Pokedex does not support async")
