1) Crée un nouveau dossier "ppe-boite_a_son"

2) Clone le projet dans le dossier créé avec git : `git clone https://git.enib.fr/a7brusco/ppe-boite_a_son.git`

3) installe Heroku CLI : `brew tap heroku/brew && brew install heroku` sur mac et `sudo snap install --classic heroku` sur ubuntu (site : https://devcenter.heroku.com/articles/heroku-cli)

4) Place toi dans le dossier "ppe-boite_a_son/ppe_boite_a_son-master/boite_a_son/" 

5) Connecte toi sur Heroku par cette commande dans le terminal : `heroku login`

6) Crée une application heroku avec cette commande : `heroku create vlm-boite-a-son`

7) Ajoute dans le fichier settings.py à la ligne 37 (Allowed Hosts) le nom de domaine : "vlm-boite-a-son.herokuapp.com"
8) Initialise le répertoire git : `git init`
9) ajoute la branche git : `heroku git:remote -a vlm-boite-a-son` 
10) Ajoute les fichiers : `git add .`
11) Commit : `git commit -m 'deploy'`
12) Enlève les collecstatic : `heroku config:set DISABLE_COLLECTSTATIC=1`
13) Deploie sur heroku : `git push heroku master`
14) Il faut ensuite se rendre sur le site d'heroku et se connecter
15) Clique sur le projet "vlm_Boite_a_Son" puis sur "Heroku Postgres" dans l'onglet overview puis rend toi dans les settings
DATABASE : "d8c3p9t36vhhsr"  //EXEMPLE DE DATABASE
HOST : "ec2-54-89-49-242.compute-1.amazonaws.com" //EXEMPLE DE HOST
USER : "gvrpufyouutzhl" //EXEMPLE DE USE
PORT : 5432 //EXEMPLE DE PORT
PASSWORD : "3dd7ee5f1febb78497f1c895df0b7a8ea434d87ba995216090908c18fbd45fd1" //EXEMPLE DE PASSWORD
17) Va dans le settings.py qui se trouve dans le répertoire boite_a_son du projet à la ligne 100 (DATABASES). Remplace les éléments "NAME" (correspond à l'attribut DATABASE), "HOST", "PORT", "USER" et "PASSWORD" avec ce que tu as sur le site.
18) add, commit et push la nouvelle version.
19) Reviens sur le site et clique sur "More" en haut à droite et clique sur "Run console"
20) Tape "bash" puis lorsque la console est prête tape `python manage.py migrate`.
21) Sur la même console créer un super utilisateur : `python manage.py createsuperuser`
22) configurer les variables d'environnements AWS : `heroku config:set AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=yyy` où xxx et yyy sont les variables associées au compte AWS S3 
23) Autoriser l'AWS à communiquer avec cette nouvelle application.
24) Pour passer la database en version payante : https://devcenter.heroku.com/articles/upgrading-heroku-postgres-databases#upgrade-with-pg-copy-default (on n'a pas pu le tester)