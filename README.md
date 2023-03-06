# Fipywifi

Pour l'instant, il n'y a que deux Fipy qui tournent, une qui joue le role de l'AP et une autre qui joue le role de la STA, leur code d'éxécution sont implémenté dans leur dossier respectif

J'essaye en ce moment d'implémenter le mechanisme de downstream avec des pspoll, pour plus de details, il faut aller voir le code commenté dans STA/main.py et AP/main.py 



## Cahier de Doléances 

 - De manière générale, les Fipy sont très capricieuse dans l'utilisation que j'en fais car elles n'implémentent pas du tout le principe d'idempotence, si je prend un exemple sur une des lignes ou il y a le code d'éxécution `send_raw(Bufer=pspoll)`
 Aléatoirement il peut y avoir une erreur systèm ou bien s'éxécuter (apres avoir fais des essais un peu trivial, ca peut arriver 1 fois sur 30)

 - Lorsque la fonction `send_raw()` envoie des trames et ne se met pas en erreur système, la trame est sytématiquement envoyé sur le medium radio sur le cannal 1 en 2,4GHz sur la bande des 20MHz. Lorsque la trame est bien forgé (c'est dire qu'il y a la bonne adresse MAC destination) la carte wifi destination recoit bien la trame et envoie un ACK. (preuve à l'appuis à l'aide de WIRESHARK en mode monitor). Même si les trames sont toujours recues coté Hardware (puisqu'il y a ACK), elles ne sont pas toujours réçu par le code qui s'éxécutent sur la Fipy de destination.

 - Le seul moyen de récupérer les trames envoyées est de mettre la machine en mode promiscueus, elle va écouter sur le medium radio et récuperer seulement les trames qui ont comme adresse MAC destination celle de la Fipy (Fait auniveau du code). Malheureusment c'est fait dans des fonctions de callback et cela met en erreur la fonction `machine.sleep(1)` qui permet à la Fipy de s'endormir (Doze state) pendant une miliseconde (erreur non systematique).

 - Ce qui rend le debogguage compliqué est la manière aléatoire des erreurs. 
 
 - Pour l'instant, lorsque je fais mes tests, je mets une seconde d'endormissement pour la station lorsqu'elle rentre dans le doze state, mais la fipy ne va pas éxécuter de manière iterative le block d'instructions.
 Par exemple j'ai remarqué que lorsque nous avons ces deux instructions :
  `machine.sleep(1000)`
  `print("je me reveille")`
 Il va d'abord m'affiché je me reveille, puis s'endormir pendant une seconde 

 - Lorsque je regade les trames que j'envoie sur le medium radio, elle s'affiches en malformed data sur Wireshark ( je suis en discussion avec Johann pour comprendre ce problème). J'ai récuperer des données de Wireshark afin de visualiser l'erreur Malformed packet

 