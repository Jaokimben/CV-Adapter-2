import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from cv_adapter import CVAdapter
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['ALLOWED_EXTENSIONS'] = {'docx'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16 Mo pour les téléchargements
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_testing')

# Assurer que les dossiers existent
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Initialiser l'adaptateur de CV
cv_adapter = CVAdapter(app.config['UPLOAD_FOLDER'], app.config['DOWNLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'cv_file' not in request.files:
            flash('Aucun fichier sélectionné', 'error')
            return redirect(request.url)
        
        file = request.files['cv_file']
        job_description = request.form['job_description']
        
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'error')
            return redirect(request.url)
        
        if not job_description:
            flash('Veuillez entrer une description de poste', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            logger.info(f"Fichier CV téléchargé: {filename}")
            logger.info(f"Longueur de la description de poste: {len(job_description)} caractères")
            
            # Adapter le CV avec la classe CVAdapter
            adapted_cv_filename = cv_adapter.adapt_cv(file_path, job_description)
            logger.info(f"CV adapté créé: {adapted_cv_filename}")
            
            # Rediriger vers la page de téléchargement
            return redirect(url_for('download_file', filename=adapted_cv_filename))
        else:
            flash('Format de fichier non autorisé. Veuillez télécharger un fichier .docx', 'error')
            return redirect(request.url)
    
    except Exception as e:
        logger.error(f"Erreur lors du traitement du CV: {str(e)}")
        flash(f"Une erreur s'est produite lors du traitement de votre CV: {str(e)}", 'error')
        return redirect(request.url)

@app.route('/download/<filename>')
def download_file(filename):
    # Vérifier que le fichier existe
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        flash('Le fichier demandé n\'existe pas', 'error')
        return redirect(url_for('index'))
    
    return render_template('download.html', filename=filename)

@app.route('/get_file/<filename>')
def get_file(filename):
    try:
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement du fichier: {str(e)}")
        flash('Erreur lors du téléchargement du fichier', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('Le fichier est trop volumineux. La taille maximale est de 16 Mo.', 'error')
    return redirect(url_for('index')), 413

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

# Nettoyage périodique des fichiers temporaires (à implémenter avec un planificateur de tâches)
def cleanup_temp_files():
    """Supprime les fichiers temporaires plus anciens que 24 heures"""
    import time
    current_time = time.time()
    for folder in [app.config['UPLOAD_FOLDER'], app.config['DOWNLOAD_FOLDER']]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                # Supprimer les fichiers plus anciens que 24 heures
                if os.stat(file_path).st_mtime < current_time - 86400:
                    os.remove(file_path)
                    logger.info(f"Fichier temporaire supprimé: {file_path}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
