![plot](https://github.com/LucieTp/14Nov2025/blob/main/maps/GitHub.png)


J'ai codé un petit jeu pour ton anniversaire 

Si tout fonctionne, ça te prendra ~30 mins de setup tout ça (déso l'installation est un peu relou j'avoue, j'ai pas eu le temps de rendre le truc plus user friendly)

Si ça te dit, il te faudra: 

> (1) Télécharger tout le contenu de ce repo github (le bouton vert "code" > "download zip" tout en bas du menu déroulant

> (2) Installer pycharm, un IDE python (ça prend 20 minutes, mais c'est le plus simple pour ouvrir le projet)
https://www.jetbrains.com/pycharm/data-science/?var=anaconda 

> (3) Ouvrir le projet dans Pycharm (clique ouvrir > navigue vers la localisation de ton fichier dézippé - probablement *"download/14Nov2025-main/"* puis clique "ouvrir") - ça devrait t'ouvrir toute l'arborescence du projet)

La section un peu galère mtn - setup ton environnement et installe les modules:

> (4) Sélectionne un interpreteur python: dans *file > settings > Python > Interpreter* clique sur "add interpreter" - une fenetre doit s'ouvrir. La dedans clique "generate new" et choisis la version python qu'il te propose, python 3.12 ou 3.13 normalement (nov 2025). Clique okay, ça devrait te créer un fichier .venv dans ton arborescence 

> (5) Toujours dans pycharm, vas dans la section "terminal" (dans les boutons du menu vertical en bas à gauche) - ou alt + F12.

Du coup, tu devrais avoir un powershell prompt qui s'affiche du style 

`(.venv) PS C:\Users\xxx\xxx\14Nov2025\>`  ## Si tu n'as pas le .venv qui s'affiche devant ton path, il y a un pb, essaies de faire "\.venv\Scripts\activate.ps1". Sinon demande à chatgpt aha

(j'espere que tu es tjrs sur windows pcq sinon jsp, faudra que tu te débrouilles)


Une fois que tu es bien situé dans ton environement, execute `pip install -r 'requirements.txt'`

Si ça marche pas, installe manuellement les modules dans le terminal avec "pip install pygame", "pip install pytmx", "pip install pyscroll", pareil pour numpy, pandas et seaborn

ça aussi ça prend un peu de temps

> (7) normalement tout est prêt! 
> Ouvre le script *"/main.py"* et click sur la flèche verte en haut de la fenetre (run)

Je te laisse te débrouiller pour le reste xx 

Hopefully ça marche and you enjoy

