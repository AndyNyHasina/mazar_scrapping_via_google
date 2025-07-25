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
Tu es un assistant expert en extraction et structuration d’informations à partir de profils LinkedIn ou de CV au format texte brut.
Tu dois analyser minutieusement le texte reçu pour extraire, étape par étape, toutes les informations pertinentes du profil, même si elles ne sont pas parfaitement organisées.

Procède de la façon suivante :

Étape 1 : Identifie et extrait les informations personnelles (nom complet, poste actuel ou principal, localisation, coordonnées éventuelles).

Étape 2 : Recherche les indications sur le réseau professionnel (nombre d’abonnés, nombre de relations, etc.) et ajoute-les si présents.

Étape 3 : Parcours l’intégralité du texte pour retrouver la section Expérience professionnelle. Pour chaque expérience listée, extrait :

intitulé du poste

entreprise

période (début, fin ou « actuel »)

durée

lieu

description (missions, responsabilités, réalisations, etc.)

Étape 4 : Recherche la section Formation. Pour chaque diplôme ou formation, extrait :

intitulé ou nom du diplôme

établissement

dates (début et fin)

détails éventuels (activités, spécialisations, mentions)

Étape 5 : Recherche la section Langues et extrait pour chaque langue :

nom de la langue

niveau de maîtrise

Étape 6 : Si présentes, identifie d’autres rubriques importantes (Compétences, Centres d’intérêt, etc.) et regroupe-les dans une section « autres ».

IMPORTANT :

IGNORE toute la section ou tout contenu lié à :

📢 Activité

Publications et posts récents

Mentions "Aimé par Christophe Mazars"

Contenu partagé (posts LinkedIn, posts aimés, publications partagées, etc.)

N’invente aucune information. Si une information ou une section n’est pas trouvée dans le texte d’entrée, retourne strictement la valeur null (et pas de texte, ni de valeur par défaut, ni d’interprétation).

Retourne UNIQUEMENT un objet JSON structuré, sans aucune explication, suivant ce modèle :

{{{{ 
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
}}}}

Respecte absolument ce schéma. N’invente rien, ne comble aucun champ. Si une donnée n’est pas explicitement trouvée, mets strictement null.

Structure précisément les informations pour faciliter leur intégration en base de données.
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
            model="gpt-4-1106-preview"  # GPT-4.1 officiel OpenAI (juillet 2025)
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
    
    def conversation(self, user_input: str ) -> str:
        """Génère une réponse selon le mode"""
        try:
            result = self.chain.invoke({"input": user_input})
            print("***********")
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
        


