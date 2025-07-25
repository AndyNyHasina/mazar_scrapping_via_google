import os
from langchain_openai import  ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser



from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)

class GPT_ask:
    PROMPTS = {
"assistant": """
Tu es un assistant expert en extraction de profils LinkedIn.

Règle absolue :
- La sortie doit être **uniquement un objet JSON valide** (sans balises, sans texte avant ou après).
- Si la personne est **actuellement** CEO ou CFO de l’entreprise `compagnie`, tu retournes l’objet JSON structuré suivant (en remplissant les champs disponibles, les autres restent null).
- Si la personne **n’est pas** CEO ou CFO, retourne exactement : {{ "content": "vide" }}.

{{
  content : 
{{
  "informations_personnelles": {{
    "nom": null,
    "titre": null,
    "localisation": null,
    "coordonnees": null
  }},
  "reseau": {{
    "abonnes": null,
    "relations": null
  }},
  "experiences": [
    {{
      "poste": null,
      "entreprise": null,
      "date_debut": null,
      "date_fin": null,
      "duree": null,
      "lieu": null,
      "description": null
    }}
  ],
  "formations": [
    {{
      "diplome": null,
      "etablissement": null,
      "date_debut": null,
      "date_fin": null,
      "details": null
    }}
  ],
  "langues": [
    {{
      "langue": null,
      "niveau": null
    }}
  ],
  "autres": null
}}
    }}





Ne jamais ajouter de balises ```json ou tout autre texte hors JSON.
"""

    }
    
    
    def __init__(self, prompt_type: str = "assistant", custom_prompt: str = None):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("❌ OPENAI_API_KEY non trouvée dans les variables d'environnement")
        
        # Choisir le prompt
        if custom_prompt:
            self.system_prompt = custom_prompt
        elif prompt_type in self.PROMPTS:
            self.system_prompt = self.PROMPTS[prompt_type]
        else:
            self.system_prompt = self.PROMPTS["assistant"]
        
        # Configuration LLM
        self.llm = ChatOpenAI(
            temperature=0.8,
            openai_api_key=self.openai_api_key,
            model="gpt-4o"  # GPT-4.1 officiel OpenAI (juillet 2025)
        )


        
        self.prompt_type = prompt_type

        self._setup_chain()
    
    def _setup_chain(self):
        """Configure la chaîne LangChain moderne"""
        system_message = SystemMessagePromptTemplate.from_template(self.system_prompt)
        human_message = HumanMessagePromptTemplate.from_template("{input}")
        self.prompt_template = ChatPromptTemplate.from_messages([system_message, human_message])
        self.output_parser = StrOutputParser()
        self.chain = self.prompt_template | self.llm | self.output_parser
    
    def conversation(self, user_input ) -> str:
        """Génère une réponse selon le mode"""
        try:
            result = self.chain.invoke({"input": user_input})
            return result.strip() if isinstance(result, str) else str(result).strip()
        except Exception as e:
            return f"❌ Erreur lors de la génération : {str(e)}\n💡 Vérifiez votre clé API OpenAI"

    

    
    def change_role(self, prompt_type: str):
        """Change le rôle/prompt en cours"""
        if prompt_type in self.PROMPTS:
            self.prompt_type = prompt_type
            self.system_prompt = self.PROMPTS[prompt_type]
            self._setup_chain()
            print(f"✅ Rôle changé vers : {prompt_type}")
        else:
            print(f"❌ Rôle '{prompt_type}' non reconnu. Rôles disponibles : {list(self.PROMPTS.keys())}")
    
    def reset_conversation(self):
        """Reset la configuration"""
        print("✅ Configuration réinitialisée")
        self._setup_chain()
        


