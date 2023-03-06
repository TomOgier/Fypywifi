# Fypywifi

Pour l'instant, il n'y a que deux Fipy qui tournent, une qui joue le role de l'AP et une autre qui joue le role de la STA, leur code d'éxécution sont implémenté dans leur dossier respectif

J'essaye en ce moment d'implémenter le mechanisme de downstream avec des pspoll, pour plus de details, il faut aller voir le code commenté dans STA/main.py et AP/main.py 



## Cahier de Doléances 

De manière générale, les Fipy sont très capricieuse dans l'utilisation que j'en fais car elles n'implémentent pas du tout le principe d'idempotence, si je prend un exemple sur une des lignes ou il y a le code d'éxécution 
`send_raw(Bufer=pspoll)`
Aléatoirement il peut y avoir une errenr système ou bien s'éxécuter (apres avoir fais des essais un peu trivial, ca peut arriver 1 fois sur 30)