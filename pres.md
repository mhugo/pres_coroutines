# Python
## Générateurs et co-routines

Hugo Mercier

*Meetup Python, Nantes, 27 janvier 2015*

Note:
La fenêtre du speaker peut être ouverte avec la touche 's'
Pour noircir la fenêtre, presser 'b'

---

## who am i

- Dev C++/Python @ oslandia
- Disclaimer : pas expert sur les co-routines !

---

## Sommaire

- Itérateurs
- Générateurs
- Co-routines

---

## Itérateurs

- Généralise le concept de séquence
- Permet une évaluation "paresseuse"
- Peut être utilisé dans la syntaxe `for ... in`

```python
container.__iter__( self ):
        # returns an iterator object

iterator.__iter__( self ):
        return self
iterator.next( self ):
        # next
        # raise StopIteration
```

---

## Itérateurs

Exemple

```python
class yrange:
      def __init__(self, n):
          self.i = 0
          self.n = n
      def __iter__(self):
          return self
      def next( self ):
          if self.i < self.n:
             i = self.i
             self.i += 1
             return i
          else:
             raise StopIteration()
```

---

## Générateurs

Nouveau mot clé `yield`

```python
def yrange(n):
    i = 0
    while i < n:
          yield i # <--
          i += 1
```

---

## Générateurs

Drôle de fonction !

- `yrange(15)` ne fait rien
- il faut appeler `next()`

Note:
type(yrange(15))
it=yrange(15)
it.next()


---

## yield

- une fonction qui utilise `yield` est un *générateur*
- `yield` rend la main à l'appelant
  * en portant éventuellement une valeur
- lors du prochain appel à `next()`, l'exécution reprend au précédent `yield` !
- à la fin de l'exécution, StopIteration est levée

---

## Generator expression

- `(2*x for x in a)`
- renvoie un itérateur
- `sum(2*x for x in a)`

Note:
parenthèses au lieu des crochets pour les list expressions

---

## Générateurs récursifs

```python
def postorder(tree):
    if not tree:
        return

    for x in postorder(tree['left']):
        yield x

    for x in postorder(tree['right']):
        yield x

    yield tree['value']
```

---

## Une couche meta

Enchaîner deux itérateurs

```python
def iter_chain( it1, it2 ):
    for i in it1:
        yield i
    for i in it2:
        yield i
```

---

## Une couche meta

Zipper deux itérateurs

```python
def iter_zip( it1, it2 ):
    while True:
        a = it1.next()
        b = it2.next()
        yield a,b
```

- s'arrête tout seul quand le plus court des deux est atteint

---

## Générateurs - outils

module `itertools`

- `chain`
- `izip`
- `islice`
- `imap`, `ifilter`

Séquences infinies :

- `count`
- `repeat`
- `cycle`

---

## Générateurs - outils

Ex:
```python
from itertools import *
list(islice(cycle(islice(count(),5)), 10))
```

---

## Factorisation

```python
def generator():
    for i in range(10):
        yield i
    for j in range(10, 20):
        yield j
```

Et si on veut découper en deux cette "fonction" ?

---

## Factorisation

```python
def generator2():
    for i in range(10):
        yield i
def generator3():
    for j in range(10, 20):
        yield j
def generator():
    for i in generator2():
        yield i
    for j in generator3():
        yield j
```

---

## Applications pratiques

- Evaluation paresseuse
  - limiter l'allocation mémoire
- Vision "flux" de données
- Analogie au pipe des commandes Unix
  - `tail | grep | print`
- Progression (remplace callback)
  - `yield` as `print`
- Asynchrone écrit de manière synchrone
- Rendre plus lisible une machine à état

---

## Pipeline

- Exemple de pipeline
- `tail -f | grep`
- cf pipeline.py

---

# Co-routines

- Généralisation des sous-routines
- `yield` peut être utilisée dans une expression
- Nouvelle méthode `send(v)`
  - équivalent à `next()` en passant une valeur
  - ... récupérée par le yield en tant qu'expression

---

## Exemple

- copipeline.py
- decorator.py
- copipeline2.py

---

## Co-routines

- Vision inversée
- Générateurs :
  - on itère et on **tire** les données
- Co-routines :
  - on **pousse** les données

---

## Co-routines

On peut envoyer à plusieurs co-routines !

cf cobroadcast.py

---

## Co-routines

Aller-retour yield et send

- possible
- non conseillé (?)

cf coroutine.py

---

## Application : code asynchrone

- callbacks : efficace, mais illisible
- idée : fonctions asynchrones lisibles comme synchrones
- les fonctions d'I/O sont des coroutines
- une boucle évenementielle ordonnance les coroutines

---

## Avec callbacks

Télécharger 1 fichier, attendre 1 s et télécharger un autre

```python
def mydownload(files,cont):
    def on_download1():
        def on_timeout():
            api.download_file(files[1], cont)
        api.set_timeout(1000, on_timeout)
    api.download_file(files[0], on_download1)
```

---

## Ce qu'on aimerait

```python
def mydownload(files):
    api.download_file(files[0])
    api.timeout(1000)
    api.download_file(files[1])
```

---

## Solution

```python
def mydownload(files):
    yield from api.download_file(files[0]):
    yield from api.timeout(1000)
    yield from api.download_file(files[1])
```

- on préfixe les appels de fonction par yield from (python 3)
- suppose l'existence de fonctions d'I/O sous forme de co-routines
- et une boucle évenementielle intelligente

---

## Trampolines

- cf PEP 342
- cf frameworks web (tornado)
- => asyncio dans python 3.3

---

## Références

- Articles
  - A Curious Course on Coroutines and Concurrency, David Beazley
  - PEP 380 - Syntax for Delegating to a Subgenerator
  - Co-routines as an alternative to state machines
  - Bouncing Python's Generators With a Trampoline 
- Projets
  - weightless
  - eventlet
  - gevent
  - SimPy
  - Stackless Python
  - tornado
  - tulip -> asyncio