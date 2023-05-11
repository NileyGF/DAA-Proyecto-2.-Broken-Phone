# DAA Proyecto 2. Broken Phone

Autores:

Niley González Ferrales C411    [@NileyGF](https://github.com/NileyGF)

Arian Pazo Valido C311          [@ArPaVa](https://github.com/ArPaVa)

El segundo proyecto de la asignatura Diseño y Análisis de Algoritmos corresponde a la temática de Teoría de Grafos. El problema que nos corresponde analizar sufrió cambios en el proceso, por ello primero se ve un análisis de la [**Orientación 1.0**](#Orientación-1.0:) dónde se evidenciarán, relativamente, nuestros avances hasta el momento de la [**Orientación 2.0**](#Orientación-2.0:) . Por último se analiza el problema modificado.

# Orientación 1.0:

Kevin estaba leyendo un libro sobre Diseño y Análisis de Algoritmos cuando se topó con un problema que llamó su atención. El texto era el siguiente:

Se tiene un grafo bipartito $G$ con $U$ nodos en el la primera parte y $V$ nodos en la segunda parte. Un subgrafo de $G$ está $k-cubierto$ si todos sus nodos tienen al menos grado $k$. Un subgrafo $k-cubierto$ es mínimo si su cantidad de **vértices** es la mínima posible. Encuentre el mínimo grafo $k-cubierto$ para todo $k$ entre $0$ y $MinDegree$ (grado mínimo del grafo $G$).
Luego de entender el problema, automáticamente pensó dos cosas:

* Quiero resolver este problema.
* ¿A los profesores se les habrá acabado la imaginación para los textos de los proyectos?

## Convirtiendo el problema 

No hay mucha transformación que hacer sobre el problema, pero lo intentamos.

Dado un grafo no dirigido, bipartito $G = ((U \cup\ V) , E )$, con $U$ nodos en el la primera parte, $V$ nodos en la segunda parte y E aristas. Se quiere encontrar el subgrafo de $G$ con la menor cantidad de **vértices** tal que todos los vértices tienen grado mayor o igual que $k$; para $k \in\ [0, MinDegree(G)]$. $MinDegree(G)= min(degree(u) : u \in\ (U \cup\ V))$

## Herramientas y Bibliotecas utilizadas

### Networkx
La biblioteca más empleada es networkx, aprovechando la estructura de grafos que definen, que permite diseñar grafos bipartitos y guardar la bipartición, graficar comodamente grafos, así como soporte para grafos no dirigidos y dirigidos.

### Generador
En el archivo Generator.py hay dos funciones: 
```
    def Gen_Bipartite_Graph(min_nodes, max_nodes) -> nx.Graph:
        ...
    def bipartition(G:nx.Graph) -> Tuple[List]:
        ...
```
La primera genera un grafo no dirigido biparito con $n$ vértices y $m$ aristas. Con $$n \in\ [min nodes, max nodes]$$ $$m \in\ [min(n+3, len(U) * len(V) ), max edges]$$ El valor de $m$ se debe a que para el problema son más interesantes los grafos moderadamente densos y los densos, ya que si hay vértices aislados, $MinDegree(G) = 0$ y solo se comprueba $k=0$, que además es un caso trival.
La segunda, dado un grafo, generado por el método anterior, devuelve las 2 particiones.

### Tester
El archivo Tester.py tiene 2 funciones para graficar grafos, utilizando fundamentalmente funcionalidades de networkx. Además está: ``` Generate_and_Save_Test_Cases(test_cases, min_n, max_n) ```.

Genera x grafos (x=test_cases) aleatorios con la función descrita en la sección anterior y los guarda en una lista en un archivo binario: 'test_cases.bin'.

Por último está ```Solve_and_Compare(solver:str, read_from:str, save_to:str, compare:bool, compare_to:str)```  que dependiendo de los parámetros con que se invoque además de resolver los casos de prueba, comprara su solución con otra específicada.

Para lograr esto fue diseñado un formato de soluciones que consiste en un diccionario que tiene como llaves, los valores válidos de k para el grafo en cuestión ( de 0 a $MinDegree$), y como valores una tupla con el subgrafo mínimo y la cantidad mínima (de vértices o aristas). Este último es el que se compara, ya que un grafo puede tener más de un subgrafo mínimo para el mismo valor de k.

## Ideas a cerca del problema

En primer lugar: el subgrafo con la menor cantidad de vértices donde todos tienen grado mayor o igual a k, es un subgrafo de una de las componentes conexas de G. O en otras palabras, no existe una solución que tenga más de una componente conexa. 

Supongamos que la hubiese, entonces todos los nodos tienen grado mayor o igual que k y hay más de una componente conexa, quitemoslas todas menos una ($CC_1$). Al quitar el resto de componentes no se modificó ninguna arista o vértice de $CC_1$. Entonces si los vértices de $CC_1$ tenían grado al menos k antes, ahora siguen teniendolo. Luego en $CC_1$ todos los vértices tienen grado  mayor o igual que k y es menor que la solución propuesta. Entonces esa solución no era mínima. Por lo que podemos concluir que no existe una solución que tenga más de una componente conexa. 

Nuestra idea de solución fue (para un k específico) obtener todas las componentes conexas e iterar sobre ellas obteniendo el subgrafo con menor cantidad de vértices con grado mayor o igual a k, si el resultado es mejor que el mínimo actual se actualiza. Al terminar todas las componentes conexas conocemos el mínimo subgrafo para k.

Hasta ahí todo muy bien, pero no encontramos ninguna forma que no fuese hacer backtrack, para dado una componente conexa y un k, devolver el subgrafo $k-cubierto$ con la menor cantidad de vértices.

Sin embargo concebimos una poda que acelera mucho el algoritmo en todos los casos donde se alcance la mínima cantidad de nodos, o sea, k*2. Ese es el mínimo porque como el grafo es bipartito para que algún vértice tenga grado k, tiene que estar conectado con k nodos del otro lado de la bipartición. Entonces la menor cantidad de nodos tal que todos tienen grado al menos k, es k nodos en U y k nodos en V.



# Orientación 2.0:

Kevin estaba leyendo un libro sobre Diseño y Análisis de Algoritmos cuando se topó con un problema que llamó su atención. El texto era el siguiente:

Se tiene un grafo bipartito $G$ con $U$ nodos en el la primera parte y $V$ nodos en la segunda parte. Un subgrafo de $G$ está $k-cubierto$ si todos sus nodos tienen al menos grado $k$. Un subgrafo $k-cubierto$ es mínimo si su cantidad de **aristas** es la mínima posible. Encuentre el mínimo grafo $k-cubierto$ para todo $k$ entre $0$ y $MinDegree$ (grado mínimo del grafo $G$).
    
Luego de entender el problema, automáticamente pensó dos cosas:

* Quiero resolver este problema.
* ¿A los profesores se les habrá acabado la imaginación para los textos de los proyectos?

La diferencia significativa (y tanto), es el criterio para que un grafo $k-cubierto$ sea mínimo en la Orientación 1.0 era la mínima cantidad de **vértices** posible, mientras que en la Orientación 2.0 es la mínima cantidad de **aristas** posible. 

## Convirtiendo el problema 

Dado un grafo no dirigido, bipartito $G = ((U \cup\ V) , E )$, con $U$ nodos en el la primera parte, $V$ nodos en la segunda parte y E aristas. Se quiere encontrar el subgrafo de $G$ con la menor cantidad de **aristas** tal que todos los vértices tienen grado mayor o igual que $k$; para $k \in\ [0, MinDegree(G)]$. $MinDegree(G)= min(degree(u) : u \in\ (U \cup\ V))$

## Definiciones y demostraciones relevantes al problema:

1. Sean G y H grafos. Se dice que H es un **subgrafo incorporado** de G si tienen los mismos vértices. O sea, H sería el resultado de quitar 0 o más aristas de G.

2. Para todo grafo G, La sumatoria de los grados de los vértices es igual a 2 veces la cantidad de aristas.

    Demostración:

    Como el grado de un vértice consta de la cantidad de aristas que inciden en él, al sumar todos los grados en un grafo se tienen en cuenta todas las aristas. Como cada arista incide en 2 vértices se suman las aristas exactamante 2 veces. Luego, la suma de los grados es 2 veces la cantidad de aristas (2*m).

<!-- 2. Un grafo G es regular de grado k si todos los vértices tienen grado k -->
Sobre grafos bipartitos:

1. Un grafo $G(V,E)$ es bipartito si V es la unión de dos conjuntos independientes disjuntos A y B. Ningún vértice de A es adyacente a otro de A y análogo para B.

2. Un grafo G es bipartito si y solo si no tiene ciclos de longitud impar.

3. Un grafo G es **bipartito completo** si es bipartito y cada vértice de uno de los 2 conjuntos es adyacente a todos los vértices del otro conjunto.

4. El grafo bipartito completo con $n_1$ vértices en un conjunto y $n_2$ en el otro se denota $K_{n_1 , n_2}$. Tiene $n_1 * n_2$ aristas.

5. Un grafo bipartito $G = ((U \cup\ V) , E )$ donde $|U| = |V|$ decimos que el grafo bipartito G es **balanceado**.

6. Si todos los vértices del mismo lado de la bipartición tienen el mismo grado, entonces G es llamado grafo **birregular**.

7. Un grafo bipartito $G = ((U \cup\ V) , E )$ tiene a lo sumo $|U| * |V|$ aristas. 

    Demostración:

    Si es bipartito completo, tiene $|U| * |V|$ aristas. Si no, entonces tiene menos aristas que el bipartito completo para los mismos conjuntos de vértices, ya que no puede haber más aristas que todos los del conjunto U enlazados con todos los del conjunto V y seguir siendo bipartito.

8. Todos los subgrafos de un grafo bipartito son bipartitos.

    Demostración:

    Supongamos que G es bipartito y un subgrafo de G, H, no lo es. Entonces H contiene algún ciclo de longitud impar. Sea ese ciclo $C = { v_1, v_2, v_3, ...,v_1}$
    Como H es el resultado de quitar vértices o aristas de G, los vértices de H son subconjunto de los vértices de G y las aristas de H son subconjunto de las aristas de G. Entonces, todas las aristas de $C$ están en G; luego $C$ está en G. Sin embargo G no puede contener un ciclo de longitud impar porque es bipartito. Entonces hay una contradicción y por reducción al absurdo H no puede tener ciclos de longitud impar. Si H no tiene ciclos de longitud impar entonces H es bipartito.
    Luego todo subgrafo de un grafo bipartito es bipartito.



### **Definiciones particulares del problema**

1. El grado del vértice con mayor grado en un grafo bipartito está acotado por la cantidad de vértices en la otra bipartición. Luego, $MaxDegree(G) \leq\ Max(|U|, |V|) $.

2. En un grafo donde todos los vértices tienen grado k, $n =|U| + |V|$, la sumatoria de los grados de los vértices del grafo es $n*k$. Por el teorema anterior  $n*k  = 2*m$. Luego, en un grafo donde todos los vértices tienen grado k, hay  $n*k \over 2 $ aristas.

3. En un grafo $k-cubierto$ la cantidad de aristas es $ \geq\ $ $ n*k \over 2 $.

Esta cota de la mínima cantidad de aristas que se necesitan para ser $k-cubierto$, puede ajustarse más en el caso de los grafos bipartitos.

4. Dado un grafo bipartito $G = ((U \cup\ V) , E )$, la mínima cantidad de aristas que puede tener un subgrafo $k-cubierto$, es:  $Max(|U|, |V|)*k$.

    Demostración:
    
    El subgrafo $k-cubierto$ H tiene como mínimo $ n*k \over 2 $ aristas.

    Si el grafo G es balanceado entonces $n=2*|U| = 2*|V|$, por lo que H tiene al menos $ 2*|U|*k \over 2 $ $ = |U| * k$   aristas. Como $|U| = |V|$,  $|U| * k = Max(|U|, |V|)*k$; luego, queda demostrado para el caso donde G es balanceado.

    Si G no es balanceado, sin pérdida de generalidad $|U| > |V|$. Si todos los nodos de U tienen al menos grado k entones de ellos salen $\geq\ |U| * k$ aristas, ya que de cada uno deben salir al menos k. Luego, en el grafo hay al menos $|U| * k =  Max(|U|, |V|)*k$ aristas.

5. Si un grafo bipartito es $k-cubierto$ mínimo y no es balanceado, existen vértices de la partición de menor tamaño que tienen grado mayor estricto que k.

    Demostración:
    
    Como el grafo G no es balanceado, sin pérdida de generalidad $|U| > |V|$. Sabemos por el punto anterior que la cantidad de aristas del grafo es al menos $|U|*k$. 

    Supongamos que todos los vértices de V tienen grado exactamente k: entonces a ellos llegan k aristas por cada uno, o sea $|V|*k$. Todas las aristas que salen de U llegan a V por definición de grafo bipartito. Pero la cantidad de aristas que salen de los vértices de U, es mayor que la cantidad que llegan a vértices de V. Por lo que no todas las aristas que salen de U llegan a V. Luego  por contradicción, o el grafo no es bipartito o existe al menos un vértice en V con grado mayor que k.

## **Soluciones al problema:**

Diseñamos dos algoritmos que utilizando backtrack encuentran el mínimo subgrafo $k-cubierto$. Uno lo hace quitando aristas del grafo original (top_down) y la otra poniendo las aristas del grafo a partir del subgrafo constituido solo por vértices (bottom_up). Además realizamos un acercamiento utilizando un algoritmo de flujo. 

## **Solución backtrack top-down**

Dado el grafo G original y un valor k (entre 0 y $MinDegree$) el algoritmo comprueba cuántos nodos en G tienen grado mayor que k. Ya que si quedan por quitar aristas, serían entre esos nodos. Luego, se hace una lista de todas las aristas que están entre nodos con grado mayor que k. Si la lista es vacía significa que es una solución minimal, o sea, un caso base de la recursividad, y retorna el grafo recibido. Por otro lado, si se pueden quitar aristas se hace un llamado recursivo por cada una, para obtener el mínimo si se quitara esa arista en este momento. Si algún llamado recursivo mejora el mínimo del grafo recibido como parámetro o de alguna arista anterior, se actualiza el mínimo. 

Además el algoritmo recibe como parámetro ``prune_min`` que es igual al $Max(|U|, |V|)$ y se utiliza para podar la recursividad ya que si la cantidad de aristas mínimas en algún punto es igual a $Max(|U|, |V|)*k=$ prune_min $*k$, nunca se va a mejorar esa solución. 

```
def backtrack_top_down_recursive(G:nx.Graph, k:int, prune_min:int):
    min_graph = G
    min_n_edges = G.number_of_edges()    
    k_cover, greater_k = K_cover(G,k)
    
    removable_edges = edges_between_greater_k(G,greater_k)
    if len(removable_edges) == 0 or min_n_edges == (G.number_of_nodes()/2)*k:
        # base case
        return min_graph, min_n_edges
    
    for edge in removable_edges:
        G_p = G.copy()
        G_p.remove_edge(*edge)
        e_min_gr, e_min_n_e = backtrack_top_down_recursive(G_p,k,prune_min)
        if e_min_n_e < min_n_edges:
            min_graph = e_min_gr
            min_n_edges = e_min_n_e
        if min_n_edges == (prune_min)*k:
            return min_graph, min_n_edges
        
    return min_graph, min_n_edges
```

En esta implementación se mantiene la invariante de que el grafo siempre es $k-cubierto$, ya que solo se quitan aristas 'seguras' (o sea, entre vértices con grado mayor estricto que k). 

## **Solución backtrack bottom-up**

Con un subgrafo sin aristas, del grafo original, una lista con todas las aristas y el valor de k comienza este algoritmo. En cada iteración de la recursividad se comprueba si el grafo es $k-cubierto$, si lo es se retorna a la llamada anterior. Si no, se obtiene la lista de nodos con grado menor que k, o sea, a los que les faltan aristas para que la solución sea factible. Posteriormente se obtienen las aristas que están entre nodos con grado menor que k (que estén en la lista de aristas que recibe el algoritmo). Por cada una, se realiza un llamado recursivo poniendola en el grafo. Si algún llamado recursivo mejora el mínimo del grafo recibido como parámetro o de alguna arista anterior, se actualiza el mínimo. Aquí proponemos la misma poda de que si se alcanza durante el for, en alguna de las soluciones de poner una arista el mínimo posible, $Max(|U|, |V|)*k=$, entonces no es necesario seguir iterando.  

```
def backtrack_bottom_up_recursive(G:nx.Graph, k:int, edges:list, prune_min:int):
    min_graph = G
    min_n_edges = G.number_of_edges()
    
    k_cover, lesser_k = K_cover(G,k,True)
    if k_cover:
        return min_graph, min_n_edges
    add_edges = edges_between_lesser_k(G,edges,lesser_k)
    min_n_edges = float('inf')
    for edge in add_edges:
        G_p = G.copy()
        G_p.add_edge(*edge)
        E_p = edges.copy()
        E_p.remove(edge)
        e_min_gr, e_min_n_e = backtrack_bottom_up_recursive(G_p,k,E_p,prune_min)
        if e_min_n_e < min_n_edges:
            min_graph = e_min_gr
            min_n_edges = e_min_n_e
        if min_n_edges == (prune_min)*k:
            return min_graph, min_n_edges
    return min_graph, min_n_edges
```

## **Solución backtrack mix-solver**

A pesar de ser soluciones de backtrack, se puede notar que en general nunca comprueban todos los casos. Si el subgrafo mínimo tiene $Max(|U|, |V|)*k=$ aristas, entonces cuando se encuentre el primero que con dicha cantidad de aristas, se deja de invocar nuevas recursiones. Además en ambos casos solo se prueban modificaciones útiles, quitando o poniendo aristas que puedan mejorar la solución solamente. 

Sin embargo, quisimos mejorarlo aún más combinando los dos métodos en uno. Utilizamos el acercamiento bottom-up para $k < 3$ y para el resto, el top-down. Sacando lo mejor de ambos, y mostrando un comportamiento mejor que ellos por separados. 


## **Solución de emparejamientos con subestructura óptima**

Esta tercera solución se basa en que si el problema tiene sub-estructura óptima, el mínimo subgrafo $(i)-cubierto$ es subconjunto de un mínimo subgrafo $(i+1)-cubierto$. Por ello el algoritmo encuentra un subgrafo $1-cubierto$ mínimo, crea $G'$ como una copia de G, pero quitando las aristas del subgrafo $1-cubierto$ y realiza la próxima iteración sobre $G'$. 

¿ Cómo se encuentran los subgrafos $1-cubiertos$ mínimos ?

Para encontrar estos subgrafos se busca un emparejamiento máximo (utilizando un algoritmo de encontrar el flujo máximo). Y luego, para los vértices que no fueron emparejados, se selecciona una arista por cada uno, para garantizar que tengan grado 1.

La solución para $k=0$ siempre es el subgrafo incorporado de G que no tiene aristas, ya que todos los vértices tienen grado k y hay la menor cantidad de aristas posibles: 0.

El algoritmo en particular guarda la solución para $k=0$ y después hace un ```for``` entre 1 y $MinDegree(G)$. En el ```for``` se crea un grafo dirigido con capacidad 1 en todas las aristas, un nodo artificial ```s``` conectado a la primera partición, luego las aristas originales se transforman en dirigidas desde la primera partición a la segunda, y estás se conectan a otro nodo artificial ```t```. Luego se realiza el algoritmo de flujo máximo utilizando la idea de Edmonds_Karp, lo que devuelve el grafo residual al encontrar un flujo máximo. Posteriormente se obtienen las aristas saturadas del flujo, que estaban en el grafo original, en una lista; y los vértices que no fueron emparejados en otra lista. Por último, una función asigna una arista a los vértices sin emparejar y actualiza ```G_k``` añadiendo las aristas saturadas y estas últimas, y ```G_p``` quitando esas aristas de él.


```
def Solver_deprecate(G:nx.Graph) -> List[Tuple[nx.Graph,int]]:
    min_degree = get_min_degree(G)
    solution = {k:(None,0) for k in range(min_degree + 1)}
    G_k = G.copy()
    G_k.clear_edges()
    G_p = G.copy()
    solution[0] = (G_k.copy(), 0)
    for i in range(1, min_degree + 1):
        DiG = create_the_flow_graph(G_p,1)
        Flow = Edmonds_Karp(DiG)
        satured, outliers = get_matching_and_outliers(G_p, Flow)
        G_p, G_k, n_edges = arbitrary_get_all_to_k(G_p, G_k, satured, outliers)        
        solution[i] = (G_k.copy(), n_edges)
    return solution
```

### **Complejidad temporal**

Sea el grafo original $G = ((U \cup\ V) , E )$. Con $MinDegree(G) = k$.

- El algoritmo obtiene el valor de k en $O (|U|+|V|) = O(n)$.

- Crea el diccionario a devolver en $O(k)$, pero k < n-1.

- Copia el grafo varias veces, pero cada una debe ser $O(|U|+|V|+|E|)=O(n+m)$.

- El ```for``` ocurre k veces.

    - Crear el grafo dirigido es $ O(n+m)$

    - El algoritmo de hallar el flujo máximo consiste en:

        - Crea la red residual y la inicializa con flujo 0 en $ O(n+m)$

        - Luego, busca caminos aumentativos entre ```s``` y ```t```, con bfs hasta que no quede ninguno. El tiempo del ciclo de Edmonds Karp es $O(n * m^2)$

    - Obtener las aristas saturadas, o sea el emparejamiento, es solamente recorrer el grafo residual buscando las aristas que el valor del flujo sea igual a la capacidad y questaban en el grafo original, esto es $O(n+m)$. Los vértices no emparejados se obtienen en $O(n)$.

    - La última función añade una  arista a los vértices no emparejados tal que tengan grado 1 y el subgrafo sea $1-cubierto$ en $O(n)$. Por último se actualizan G_k y G_p añadiendo y removiendo las aristas del subgrafo $1-cubierto$ anterior respectivamente. Estas operaciones son $O(m)$, ya que en el caso peor puede que el subgrafo sea exactamente igua a G. Contar la cantidad de aristas de G_k también es $O(m)$.

    - Copiar G_k para el diccionario solución es $O(n+m)$.

La complejidad temporal del algoritmo se puede representar como: ``T(n,m,k) = Costo_antes_del_for + Costo_del_for``

``Costo_antes_del_for = O(n) + O(k) + O(n+m)``

``Costo _del_for = O(k) * ( O(n+m) + ( O(n+m) + O(n * m^2) ) +  ( O(n+m) + O(n) ) + ( O(n) + O(m) )  + O(n+m))``

Por la regla de la suma (y el hecho de que como $k < n, k = O(n)$ ) la primera expresión puede reducirse a : 

``Costo_antes_del_for = O( max{n, k, n+m} ) = O(n+m)``

El mismo procedimiento se aplica a la otra expresión resultando:

``Costo _del_for = O(k) * ( O(n+m) + O( max{n+m, n * m^2} ) + O( max{n+m, n ) + O( max{n, m} )  + O(n+m) )``
    
``Costo _del_for = O(k) * ( O(n+m) + O(n * m^2) + O(n+m) + O(m) + O(n+m) )``

``Costo _del_for = O(k) * ( O( max{ n+m, n * m^2, m) )``

``Costo _del_for = O(k) * O( n * m^2)``
 
Que por la regla del producto es:   ``Costo _del_for = O(k * n * m^2)``

Entonces:

`` T(n,m,k) = Costo_antes_del_for + Costo_del_for =  O(n+m) +   O(k * n * m^2) =  O( max{n+m, k * n * m^2 } ) ``

`` T(n,m,k) = O(k * n * m^2) ``

### **Demostración de correctitud**

La demostración de correctitud pasa por demostrar varios puntos importantes:

* El problema tiene sub-estructura óptima ya que el mínimo subgrafo $(i) -cubierto$ es subconjunto de un mínimo subgrafo $(i+1)-cubierto$.

Durante el intento de demostrar esta proposición encontramos un contra-ejemplo, que demuestra que la subestructura óptima no existe, o al menos no bottom-up. 

![](counter_example.png)

En la imagen se puede observar que como la solución para k=2 se construye a partir de la solución encontrada para k=1, contiene una arista más que la solución real. 


## **Solución de multi-emparejamientos #2**

Nuestra última propuesta es realizar una modificación de la solución anterior, pero con un poco más de costo computacional, ya que no reutilizaremos la solución de (i-1) para crear la solución de (i). En lugar de hacer un emparejamiento, proponemos un flujo para cada k, de forma que el flujo máximo contenga la mayor cantidad de nodos con grado exactamente k que se puede obtener. Luego se adicionan la menor cantidad de aristas posibles para garantizar que los nodos que aún no tengan grado k, lo alcancen.

```
def Solver(G:nx.Graph) -> List[Tuple[nx.Graph,int]]:
    min_degree = get_min_degree(G)
    solution = {k:(None,0) for k in range(min_degree + 1)}
    G_k = G.copy()
    G_k.clear_edges()
    G_p = G.copy()
    solution[0] = (G_k.copy(), 0)
    for i in range(1, min_degree + 1):
        DiG = create_the_flow_graph(G_p,i)
        Flow = Edmonds_Karp(DiG)
        solution[i] = get_everyone_to_k(G,Flow,i)
            
    return solution
```
Podemos observar que el constructor del grafo para el flujo, en lugar de recibir 1 como paramétro para las capacidades, recibe el i actual. Por otro lado, las 2 funciones posteriores al flujo fueron sustituidas por  ```get_everyone_to_k```. Y eso es todo. 

Al crear el grafo dirigido sobre el que se realiza el flujo, se crea un nodo artificial ```s``` conectado a la primera partición, con capacidad $i$ (el k de la presente iteración) entre cada arista que va desde ```s``` a loa vértices de U. Luego las aristas originales se transforman en dirigidas con los arcos desde U hasta V, con capacidad 1 (para que solo puedan ser utilizadas una vez). Cada vértice de V entonces se conecta con el otro nodo artificial ```t```, y cada arco que va hacia ```t``` tiene capacidad $i$. Con esta forma de asignar las capacidades buscamos que por cada vértice solo pueda entrar y salir a lo sumo i flujo, esto implica que en el flujo máximo los nodos van a tener a lo sumo grado $i$ (contando solo las aristas saturadas), y además como el flujo maximiza, será la mayor cantidad de vértices con grado $i$ que se pueden obtener. 

¿Cuál es la magia en ```get_everyone_to_k```?
```
def get_everyone_to_k(G:nx.Graph, R:nx.DiGraph,k:int):
    satured = []
    queue = []
    for v, attr in R.succ['s'].items(): 
        queue.append(v)
    
    for u in queue: 
        for v, attr in R.succ[u].items(): 
            # satured edges that belonged in the original graph
            if (attr["flow"] == attr["capacity"]) and (v in G[u]):
                satured.append((u,v))

    G_p = G.copy()
    G_p.clear_edges()
    G_p.add_edges_from(satured)

    k_cover, nodes_to_fix = K_cover(G_p,k)
    add_edges = edges_between_lesser_k(G,nodes_to_fix)
    for u, v in add_edges:
        if G_p.degree[u] < k or G_p.degree[v] < k:
            G_p.add_edge(u,v)
    return G_p, G_p.number_of_edges()
```
Reutilizando y modificando un poco la función de las primeras dos soluciones:
```
def edges_between_lesser_k(G:nx.Graph, lesser_k:List[int]):
    # edges between lesser k (edges between nodes with degree < k)
    eblk = [] 
    # edges between nodes where one of them has degree < k
    one_is_lesser_k = []
    for u, v in G.edges():
        if u in lesser_k and v in lesser_k:
            eblk.append((u,v))
        elif u in lesser_k or v in lesser_k:
            one_is_lesser_k.append((u,v))
    if len(eblk) > 0:
        raise Exception(" the matching wasn't max ")
    return eblk + one_is_lesser_k
```

Entonces, describamos lo que pasa en las funciones anteriores. Primero, bfs-like, se capturan todos los nodos de la primera partición (U), y se guardan todas las aristas que salgan de ellos que estén saturadas. Luego se crea un grafo solo con esas aristas. Se comprueba si ya es k_cubierto, y si no lo es, se obtienen los nodos que aún no tienen grado k. 

En ```edges_between_lesser_k``` se obtienen todas las aristas que inciden sobre dichos nodos, destacando que no puede quedar ninguna entre 2 nodos con grado menor que k, porque el flujo la hubiese encontrado. 

Para finalizar por cada una de las aristas obtenidas (u,v) , se comprueba si u o v tienen grado menor que k, y en ese caso se adiciona al subgrafo que se está construyendo. De esta forma, todos los vértices con grado menor que k llegarán a grado k con la menor cantidad de aristas posibles, garantizando que el subgrafo sea mínimo todo el tiempo y haciendolo $k-cubierto$. 

O sea, utilizamos la idea de llevar una solución mejor que la óptima y la hacemos factible.

### **Complejidad temporal**

El tiempo antes del ```for``` es el mismo que en algoritmo anterior, ya que la modificación es posterior. Entonces ``Costo_antes_del_for = O(n+m)``

- El ```for``` ocurre k veces.

    - Crear el grafo dirigido es $ O(n+m)$

    - El algoritmo de hallar el flujo máximo  no fue modificado por lo que es $O(n * m^2)$

    - ```get_everyone_to_k``` 
        
        - obtiene las aristas saturadas en $O(m)$ 

        - crea el subgrafo con las aristas saturadas en $O(n+m)$

        - saber si es $k-cubierto$ y obtener los nodos con grado menor que k es $O(n+m)$
        
        - obtener las aristas incidentes en nodos con grado menor que k es $O(m)$

        - llevar a la solución factible, donde todos los vértices tienen grado k es $O(m)$


La complejidad temporal del algoritmo se puede representar como: ``T(n,m,k) = Costo_antes_del_for + Costo_del_for``

``Costo_antes_del_for = O(n+m)``

``Costo _del_for = O(k) * ( O(n+m) + O(n * m^2) +  ( O(m) + O(n+m) + O(n+m) + O(m) + O(m) ) )``
    
``Costo _del_for = O(k) * ( O(n+m) + O(n * m^2) + O(n+m) )``

``Costo _del_for = O(k) * ( O( max{ n+m, n * m^2) )``

``Costo _del_for = O(k) * O( n * m^2)``
 
Que por la regla del producto es:   ``Costo _del_for = O(k * n * m^2)``

Entonces:

`` T(n,m,k) = Costo_antes_del_for + Costo_del_for =  O(n+m) +   O(k * n * m^2) =  O( max{n+m, k * n * m^2 } ) ``

`` T(n,m,k) = O(k * n * m^2) ``

Consideramos que es importante destacar que el algoritmo podría ser $O(k*n^3)$ de haber elegido otro algoritmo para el flujo, pero en este caso la mayor parte del tiempo Edmonds-Karp es más eficiente ya que los caminos de s a t que nos interesan son directamente encontrados por el bfs.

### **Demostración de correctitud**

* Con el flujo se obtiene la mayor cantidad de nodos con grado k

    Supongamos que $|U| \geq\ |V|$, en este caso el valor del flujo está limitado por el flujo de V a t, que es $|V|*k$, pues cada arista de V a t tiene capacidad k. 

    Si no, $|U| < |V|$, en este caso el limite es el flujo que sale de s, que solo puede ser $|U|*k$.
    Por ello podemos concluir que el flujo máximo es $f \leq\ Min(|U|,|V|) * k$. Ya que cuando se saturen todas las aristas de s a U, o de V a t; no quedarán caminos aumentativos, en el grafo residual, de s a t. 

    Todos los vértices tienen grado $\geq k$, porque los k solo van hasta MinDegree.  

    Por cada vértice puede pasar a lo sumo k de flujo (porque o solo recibe k de s, o solo le puede enviar k a t).

    El flujo máximo tiene la mayor capacidad saturada  y como todas las aristas entre U y V tienen capacidad 1 eso es equivalente a decir que tiene la mayor cantidad de aristas entre U y V saturadas. 

    Eso se traduce en que al terminar el flujo se obtienen la mayor suma de grados de los vértices donde todos tienen a lo sumo grado k. Eso implica que los que aún no tienen grado k necesitan enlazarse con nodos con grado mayor o igual que k para alcanzar el grado k y con él la $k-cobertura$ del subgrafo.

    El valor del flujo es a lo sumo $Min(|U|,|V|) * k \leq\ Max(|U|,|V|) * k \leq\ $ la mínima cantidad de aristas de un subgrafo $k-cubierto$. Así que hasta ahora tenemos un subgrafo con menos aristas que el mínimo subgrafo $k-cubierto$.

* poner aristas en los nodos con grado menor que k hasta que alcancen grado k, resulta en la menor cantidad de aristas, por lo que el subgrafo cuando es $k-cubierto$, es mínimo. 

    Para que la solución sea factible es necesario que todos los nodos tengan al menos grado k, pero eso no se garantiza en el flujo. Por ello es necesario analizar los vértices que aun no tienen grado k. 

    En primer lugar, no quedan aristas no saturadas en el flujo entre 2 vértices con grado menor que k. Si ambos tienen grado menor que k había un camino de s a uno y de t a otro, si además había una arista entre ellos, no saturada, entonces hubiera un camino de s a t, luego el flujo no habría terminado. Entonces por reducción al absurdo no se pueden poner aristas entre 2 vértices con grado menor que k.

    Para que el subgrafo sea $k-cubierto$ hay que utilizar $x_i$ aristas por cada vértice i ($x_i = k - deg(i)$). Estas aristas existen, ya que en G, todos los vértices tienen al menos k aristas. No se pueden utilizar menos aristas que esas. Entonces el subgrafo que se obtiene de  llevar todos los nodos a grado k es mínimo. 

Siempre es posible llevar los nodos a grado k, en el recorrido por las aristas no saturadas que inciden en ellos, ya que los nodos originalmente tenían grado mayor o igual que k, o sea tenían al menos k aristas incidiendo en cada uno. Como solo se ponen las aristas si el nodo aún no tiene grado k, nunca se ponen aristas innecesarias. Además la primera arista que al ponerla el grafo se vuelve $k-cubierto$ es también la última. Pues, a partir de ese momento cada vez que se pregunte si alguno de los vértices de la arista tiene grado menor que k la respuesta será ``False`` y no se colocarán más aristas en el subgrafo.