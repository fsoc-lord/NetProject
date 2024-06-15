import os  # Module pour les fonctions liées au système d'exploitation
import zipfile  # Module pour la manipulation des fichiers au format ZIP
import sqlite3  # Module pour interagir avec des bases de données SQLite
from flask import (  # Importation des fonctionnalités de Flask pour la création d'application web
    Flask, request, flash, redirect, render_template, send_from_directory, url_for, session, send_file
)
from werkzeug.utils import secure_filename  # Utilitaire Werkzeug pour sécuriser les noms de fichiers téléchargés par l'utilisateur.
from werkzeug.security import generate_password_hash, check_password_hash  # Utilitaires Werkzeug pour le hachage sécurisé des mots de passe.
import hashlib  # Module pour l'utilisation de fonctions de hachage SHA256.
from functools import wraps  # Utilisation de la fonction wraps pour la décoration de fonctions.
import configparser  # Module pour la lecture des fichiers de configuration au format INI


# Configuration de l'application Flask
app = Flask(__name__)

# Chemin d'accès au fichier de configuration
CONFIG_FILE = "config.cfg"

# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Récupération des informations sensibles , username et password de l'admin.
AUTHORIZED_ACCOUNT = config.get("ADMIN", "USERNAME")
AUTHORIZED_PASSWORD = config.get("ADMIN", "PASSWORD")
AUTHORIZED_PASSWORD_HASH = hashlib.sha256(AUTHORIZED_PASSWORD.encode()).hexdigest()

# Récupération des chemins des dossiers depuis le fichier de configuration
ALL_USER = config.get("SETTINGS", "ALL_USER")
FILES_USER = config.get("SETTINGS", "FILES_USER")
FOLDER_USER = config.get("SETTINGS", "FOLDER_USER")

app.config["SECRET_KEY"] = os.urandom(24)

app.config["ALL_USER"] = ALL_USER
app.config["FILES_USER"] = FILES_USER
app.config["FOLDER_USER"] = FOLDER_USER

# Extensions de fichiers autorisées pour le téléchargement
allowed_extensions = config.get("SETTINGS", "ALLOWED_EXTENSIONS")
ALLOWED_EXTENSIONS = set(allowed_extensions.split(','))

# Vérifie si l'utilisateur est administrateur
def is_admin(username, password):
    if username == AUTHORIZED_ACCOUNT and hashlib.sha256(password.encode()).hexdigest() == AUTHORIZED_PASSWORD_HASH:
        print(f"User {username} is authenticated as admin.")
        return True
    else:
        print(f"User {username} is not authenticated as admin.")
        return False

def requires_authorization(f):
    # Définition de la fonction décorée, utilisant wraps pour préserver les métadonnées de la fonction d'origine f
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si l'utilisateur est authentifié en vérifiant la session
        if session.get("username") != AUTHORIZED_ACCOUNT:
            # Si l'utilisateur n'est pas autorisé, affiche un message d'erreur et redirige vers la page d'accueil
            flash("Vous n'êtes pas autorisé à accéder à cette page.", "error")
            return redirect(url_for("home"))  
        
        # Si l'utilisateur est autorisé, exécute la fonction d'origine f avec les arguments et les mots-clés reçus
        return f(*args, **kwargs)
    
    # Retourne la fonction décorée, prête à être utilisée comme décorateur
    return decorated_function

# Route principale pour la page d'accueil
@app.route("/")
def home():
    """
    home() : Méthode qui return la page d'acceuil.
    """
    return render_template("home.html")

@app.route("/nav")
def nav():
    """
    nav() : Méthode qui permet la redirection de la navbar.
    """
    return render_template("navbar.html")

@app.route("/download/<filename>")
def download_file(filename):
    """
    download_file() : Méthode qui permet de télécharge un fichier.
    """
    folder_name = session.get("folder")
    user_folder_path = os.path.join(app.config["ALL_USER"], folder_name)
    return send_from_directory(user_folder_path, filename, as_attachment=True)

@app.route("/download_folder/<foldername>")
def download_folder(foldername):
    """
    download_folder() : Méthode qui permet de télécharger un dossier entier sous forme de fichier ZIP
    """
    user_folder_path = os.path.join(app.config["ALL_USER"], session.get("folder"), foldername)
    if not os.path.isdir(user_folder_path):
        flash("Le dossier spécifié n'existe pas.", "error")
        return redirect(url_for("user_home"))

    zip_filename = f"{foldername}.zip"
    zip_path = os.path.join(app.config["FOLDER_USER"], zip_filename)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(user_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, user_folder_path)
                zipf.write(file_path, relative_path)

    return send_file(zip_path, as_attachment=True)

@app.route("/download_folder_from_folder/<path:folderpath>")
def download_folder_from_folder(folderpath):
    """
    download_folder_from_folder() : Méthode qui permet de télécharger un dossier à partir d'un chemin de dossier complet
    """
    user_folder_path = os.path.join(app.config["ALL_USER"], folderpath)
    if os.path.isdir(user_folder_path):
        zip_filename = f"{os.path.basename(folderpath)}.zip"
        zip_path = os.path.join(app.config["FOLDER_USER"], zip_filename)
        
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(user_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, user_folder_path)
                    zipf.write(file_path, relative_path)
        
        return send_file(zip_path, as_attachment=True)
    else:
        flash("Le dossier spécifié n'existe pas.", "error")
        return redirect(url_for("user_home"))

@app.route("/download_subfolder/<path:folderpath>")
def download_subfolder(folderpath):
    """
    download_subfolder() : Méthode qui permet de télécharger un sous-dossier d'un chemin de dossier complet
    """
    user_folder_path = os.path.join(app.config["ALL_USER"], folderpath)
    if os.path.isdir(user_folder_path):
        zip_filename = f"{os.path.basename(folderpath)}.zip"
        zip_path = os.path.join(app.config["FOLDER_USER"], zip_filename)
        
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(user_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, user_folder_path)
                    zipf.write(file_path, relative_path)
        
        return send_file(zip_path, as_attachment=True)
    else:
        flash("Le sous-dossier spécifié n'existe pas.", "error")
        return redirect(url_for("user_home"))

@app.route("/view_folder/<path:path>")
def view_folder_contents(path):
    """
    view_folder_contents() : Méthode qui permet d'afficher le contenu d'un dossier.
    """
    full_path = os.path.join(ALL_USER, path)
    if os.path.isdir(full_path):
        contents = os.listdir(full_path)
        subfolders = [f for f in contents if os.path.isdir(os.path.join(full_path, f))]
        files = [f for f in contents if os.path.isfile(os.path.join(full_path, f))]

        return render_template("folder_content.html", folder_name=path, subfolders=subfolders, files=files)
    else:
        flash("Le chemin spécifié n'est pas un dossier.", "error")
        return redirect(url_for("user_home"))

@app.route("/view_folder/download/<path:filepath>")
def download_file_from_folder(filepath):
    """
    download_file_from_folder() : Méthode qui permet de télécharger un fichier à partir d'un dossier spécifié.
    
    """
    user_file_path = os.path.join(app.config["ALL_USER"], filepath)
    if os.path.isfile(user_file_path):
        return send_file(user_file_path, as_attachment=True)
    else:
        flash("Le fichier spécifié n'existe pas.", "error")
        return redirect(url_for("user_home"))

def allowed_file(filename):
    """
    allowed_file(filename) : Méthode , utilitaire utilisée pour vérifier si le type de fichier d'un fichier téléchargé est autorisé, en se basant sur son extension de fichier. 
    
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/transfer", methods=["GET", "POST"])
def transfer_ff():
    """
    transfer_ff() : Méthode  qui permet de transferer un  dossier et de le compressé en format .zip et de l'enregistrer dans un dossier.
    
    """
    if "username" not in session:
        flash("Vous devez être connecté pour accéder à cette page.")
        return redirect(url_for("login"))

    if request.method == "POST":
        if "file" not in request.files:
            flash("Pas de fichier")
            return redirect(request.url)

        files = request.files.getlist("file")

        if not files or files[0].filename == "":
            flash("Aucun fichier n'est sélectionné")
            return redirect(request.url)

        username = session["username"]
        user_folder_path = os.path.join(app.config["FOLDER_USER"], username)

        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)

        selected_folder = os.path.basename(os.path.dirname(files[0].filename))

        zip_filename = f"{selected_folder}.zip"
        zip_path = os.path.join(user_folder_path, zip_filename)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(selected_folder, filename)
                    zipf.writestr(file_path, file.read())

        flash("Le dossier a été compressé avec succès.", "success")
        return redirect(url_for("user_home"))

    return render_template("transfer.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """
    upload_file() : Méthode qui permet de upload un fichier , de transferer un fichier et de l'enregistrer dans un dossier.
    """
    if "username" not in session:
        flash("Vous devez être connecté pour accéder à cette page.")
        return redirect(url_for("login"))

    if "file" not in request.files:
        flash("Aucun fichier n'a été envoyé.")
        return redirect(request.url)

    files = request.files.getlist("file")

    if not files or all(file.filename == "" for file in files):
        flash("Aucun fichier n'a été sélectionné.")
        return redirect(request.url)

    user_folder_name = session.get("folder")
    user_folder_path = os.path.join(app.config["FILES_USER"], user_folder_name)

    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(user_folder_path, filename)
            file.save(file_path)
        else:
            flash("Un fichier téléchargé n'est pas autorisé.")

    flash("Les fichiers ont été téléchargés avec succès.", "success")
    return redirect(url_for("user_home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    login() ; Méthode qui permet de se connecter à un compte utilisateur.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Vérification du username et du mots de passe de l'admin.
        if is_admin(username, password):
            session["username"] = username
            flash("Connexion réussie en tant qu'administrateur", "success")
            return redirect(url_for("login"))
        
        # Interaction avec la base de données 
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        # vérification et check du username,password hashé et du folder de l'utilisateur.
        if user and check_password_hash(user[2], password):
            session["username"] = user[1]
            session["folder"] = user[3]
            flash("Connexion réussie", "success")
            return redirect(url_for("user_home"))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect", "error")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
@requires_authorization
def register():
    """
    register() : Méthode qui permet de créer un compte utilisateur.
    """
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        folder = request.form["folder"]
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            flash("Ce nom d'utilisateur existe déjà.", "error")
            return redirect(url_for("register"))

        cursor.execute("SELECT * FROM users WHERE folder=?", (folder,))
        if cursor.fetchone():
            flash("Ce nom de dossier est déjà utilisé. Veuillez en choisir un autre.", "error")
            return redirect(url_for("register"))

        try:
            cursor.execute("INSERT INTO users (username, password, folder) VALUES (?, ?, ?)", (username, hashed_password, folder))
            conn.commit()
            conn.close()

            user_folder_path = os.path.join(app.config["ALL_USER"], folder)
            if not os.path.exists(user_folder_path):
                os.makedirs(user_folder_path)

            flash("Inscription réussie, vous pouvez vous connecter.", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Erreur lors de l'inscription. Veuillez réessayer.", "error")

    return render_template("register.html")

@app.route("/logout")
def logout():
    """
    logout() : Méthode qui permet de se déconnecter
    """
    session.clear()
    flash("Vous êtes maintenant déconnecté.", "success")
    return redirect(url_for("home"))

@app.route("/user_home")
def user_home():
    """
    user_home() : Méthode qui permet d'afficher , de lister les fichiers , les sous dossiers du compte utilsiateur.
    """
    if "username" not in session:
        flash("Vous devez être connecté pour accéder à cette page.")
        return redirect(url_for("login"))

    folder_name = session.get("folder")

    if not folder_name:
        return redirect(url_for("home"))

    folder_path = os.path.join(app.config["ALL_USER"], folder_name)

    if os.path.exists(folder_path):
        contents = os.listdir(folder_path)
        subfolders = [c for c in contents if os.path.isdir(os.path.join(folder_path, c))]
        files = [c for c in contents if os.path.isfile(os.path.join(folder_path, c))]
        zip_filename = f"{folder_name}.zip"
        
        return render_template("user_home.html", subfolders=subfolders, files=files, folder_name=folder_name, zip_filename=zip_filename)
    else:
        return redirect(url_for("home"))

@app.route("/support")
def support():
    """
    support() : Méthode qui permet en cas de problème de pouvoir contacter l'administrateur. 
    """
    return render_template("support.html")

if __name__ == "__main__":
    app.run(debug=True)