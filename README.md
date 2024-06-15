# Projet NetProject

NetProject est un projet conçu pour faciliter l'accès et la gestion de ressources au sein de réseaux locaux, offrant des fonctionnalités telles que :

- Permet aux utilisateurs de partager des ressources sans accès à Internet, favorisant ainsi la collaboration locale.
- Outil idéal pour les structures éducatives ou les enseignants pour gérer efficacement leurs classes et partager des documents.
- Intègre des fonctionnalités avancées telles que le téléchargement et le partage de fichiers, la gestion de dossiers, et la sécurisation des accès via une interface web conviviale.

Le projet est développé avec Python et utilise Flask pour la création de l'application web, ainsi que Tkinter pour une interface utilisateur graphique (GUI) locale.

## Fonctionnalités

- **Authentification** : Connexion sécurisée avec vérification des utilisateurs et gestion des sessions.
- **Gestion de fichiers** : Téléchargement et visualisation de fichiers.
- **Compression de dossiers** : Téléchargement de dossiers entiers sous forme de fichiers ZIP.
- **Interface graphique** : Interface tkinter pour démarrer et arrêter l'application Flask.


## Installation

1. **Clonez le dépôt:**
   ```bash
   git clone https://github.com/fsoc-lord/netproject.git
   cd netproject
2. **Installer les dépendances:**
   ```python
   pip install -r requirements.txt
3. **Fichier de configuration:**
   - Vous devez configurer les 3 chemins auquels les dossiers , les fichiers et les data all user. [SETTINGS] 
   - Mots de passe et Username de l'admin par défault est admin admin -> vous pouvez seulement le mots de passe. [ADMIN]
   - Ajouter ou modifier les extensions autoriser pour les uploads de fichier -> [SETTINGS] = ALLOWED_EXTENSIONS
       ```ini
       [ADMIN]
      USERNAME = admin
      PASSWORD = admin

      [SETTINGS]
      ALLOWED_EXTENSIONS = pdf,py,jpg,jpeg,gif,png,html,css,js,mp4
       
      [SETTINGS]
     ALL_USER = /chemin/vers/dossier/utilisateurs
     FILES_USER = /chemin/vers/dossier/fichiers
      FOLDER_USER = /chemin/vers/dossier/dossiers
3. **OPTIONNEL**
   Pour toutes utilisateurs souhaitant rendre cet application web en application exécutable sur son bureau, il suffit:

   - Installer pyinstaller :
     
        ```python
           pip install pyinstaller
   -  Lancer pyinstaller pour rendre l'application web en application executable :
     
      ```python
       pyinstaller --onefile "app.py" --name "NetProjectV1.0"
   -  Sortez le fichier NetProjectV1.0 du dossier /dist vers /Netprojet
     
   -  Cliquer sur l'exécutable et le tour est joué !
  
## **Utilisation:**

   - Lancer l'application :
     
     ```python
     flask run
     python3 apptk.py
     python  apptk.py
     
  - Accédez à l'application :

    Ouvrez un navigateur et accèder avec l'adresse ip que votre application tkinter affiche pour utiliser l'application -> ex. 192.168.1.10:5000 

## **Contribution:**
   
   Les contributions au projet sont les bienvenues. Pour des suggestions d'amélioration, veuillez ouvrir une issue pour discuter des changements proposés.
