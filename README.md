# Adaptateur de CV

Une application web responsive qui permet d'adapter un CV en format Word à une description de poste dans une annonce d'emploi et de télécharger un CV personnalisé.

## Fonctionnalités

- Téléchargement d'un CV au format Word (.docx)
- Analyse de la description du poste pour identifier les mots-clés importants
- Adaptation du CV en mettant en évidence les compétences pertinentes
- Téléchargement du CV adapté au format Word

## Démonstration

![Capture d'écran de l'application](https://example.com/screenshot.png)

## Technologies utilisées

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Traitement de documents**: python-docx, docx2txt
- **Déploiement**: Render.com, GitHub

## Installation locale

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- virtualenv (recommandé)

### Étapes d'installation

1. Clonez le dépôt GitHub :
   ```bash
   git clone https://github.com/votre-utilisateur/cv-adapter.git
   cd cv-adapter
   ```

2. Créez et activez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Configurez les variables d'environnement :
   ```bash
   cp .env.example .env
   # Modifiez le fichier .env selon vos besoins
   ```

5. Lancez l'application :
   ```bash
   python app.py
   ```

6. Accédez à l'application dans votre navigateur à l'adresse `http://localhost:5000`

## Déploiement sur Render.com

### Prérequis

- Un compte Render.com
- Un dépôt GitHub contenant le code de l'application

### Étapes de déploiement

1. Connectez-vous à votre compte Render.com

2. Cliquez sur "New" puis sélectionnez "Web Service"

3. Connectez votre dépôt GitHub et sélectionnez le dépôt cv-adapter

4. Configurez le service :
   - **Name**: cv-adapter (ou le nom de votre choix)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. Cliquez sur "Create Web Service"

6. Votre application sera déployée et accessible à l'URL fournie par Render

## Structure du projet

```
cv-adapter/
├── app.py                 # Application Flask principale
├── cv_adapter.py          # Classe pour l'adaptation de CV
├── requirements.txt       # Dépendances Python
├── Procfile               # Configuration pour Render.com
├── .env                   # Variables d'environnement
├── static/                # Fichiers statiques (CSS, JS)
│   └── css/
│       └── style.css      # Styles de l'application
├── templates/             # Templates HTML
│   ├── index.html         # Page d'accueil
│   ├── download.html      # Page de téléchargement
│   ├── 404.html           # Page d'erreur 404
│   └── 500.html           # Page d'erreur 500
├── uploads/               # Dossier pour les CV téléchargés
└── downloads/             # Dossier pour les CV adaptés
```

## Utilisation

1. Accédez à l'application via votre navigateur

2. Téléchargez votre CV au format Word (.docx)

3. Copiez-collez la description complète du poste dans le champ de texte

4. Cliquez sur "Adapter mon CV"

5. Téléchargez votre CV adapté depuis la page de résultats

## Fonctionnement technique

L'application utilise un algorithme d'analyse de texte pour :

1. Extraire les mots-clés importants de la description du poste
2. Identifier les compétences techniques requises
3. Mettre en évidence (en gras) les termes correspondants dans votre CV
4. Générer une version adaptée du document

## Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.
