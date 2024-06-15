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
  
5.   **Utilisation:**

   - Lancer l'application :
     
     ```python
     flask run
     python3 apptk.py
     python  apptk.py
     
  - Accédez à l'application :

    Ouvrez un navigateur et accèder avec l'adresse ip que votre application tkinter affiche pour utiliser l'application -> ex. 192.168.1.10:5000 
    
6. **Contribution:**
   
   Les contributions au projet sont les bienvenues. Pour des suggestions d'amélioration, veuillez ouvrir une issue pour discuter des changements proposés.
