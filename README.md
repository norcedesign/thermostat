# MGL849

**Laboratoire # 1**

## Thermostat numérique

Multitasking program simulating the functionality of a digital thermostat. This app uses the sensors of a Sense Hat board, connected to a Raspberry Pi 4 Model B.


## Installation

Suivez le [guide](https://ena.etsmtl.ca/pluginfile.php/1068342/mod_resource/content/7/MGL849H2021-Labl1Spec_detailsV2.pdf) du laboratoire pour les instructions.

## Utilisation en simulation

 - Lancez le programme d'affichage en prenant soin de configure le port désiré.

    ```shell
    java -jar path/to/Lab1Afficheur.jar
    ```

 - Dans le fichier `app.py` , configurez les variables `host` et `port` avec les valeurs de votre environnement.
    Ensuite, exécutez le ficher `app.py`.

    |     Variable     |     Valeur par défaut     |
    |------------------|---------------------------|
    | host | localhost ou 127.0.0.1
    | port | 1234

    ```shell
    python path/to/app.py
    ```

#### Remarques
    Le lancement du programme peut se faire différemment selon l'environnement.
