#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Localiza texto de espanol rioplatense (voseo) a espanol panameno (tuteo).

Uso:
    python scripts/localizar_panameno.py <archivo1> [<archivo2> ...]

Aplica un diccionario CURADO de reemplazos palabra-por-palabra (con limites de
palabra y respetando mayusculas/minusculas). Solo toca las formas verbales de
voseo que realmente aparecen en el repo; NO toca acentos que no son voseo
(esta, que, asi, este, ahi, Usalo, etc.).

No es un traductor generico: es una lista blanca. Si aparece una forma de voseo
nueva, se agrega aca. Es seguro correrlo mas de una vez (idempotente).
"""

import re
import sys

# Mapa curado voseo -> tuteo. Clave = forma voseo exacta (como aparece),
# valor = forma tuteo panamena. Se incluyen variantes con mayuscula inicial.
REEMPLAZOS = {
    # --- verbos -ar regulares (imperativo) ---
    "preguntá": "pregunta", "Preguntá": "Pregunta",
    "derivá": "deriva", "Derivá": "Deriva",
    "generá": "genera", "Generá": "Genera",
    "normalizá": "normaliza", "Normalizá": "Normaliza",
    "usá": "usa", "Usá": "Usa",
    "asigná": "asigna", "Asigná": "Asigna",
    "agregá": "agrega", "Agregá": "Agrega",
    "respetá": "respeta", "Respetá": "Respeta",
    "identificá": "identifica", "Identificá": "Identifica",
    "indicá": "indica", "Indicá": "Indica",
    "evaluá": "evalúa", "Evaluá": "Evalúa",
    "detectá": "detecta", "Detectá": "Detecta",
    "armá": "arma", "Armá": "Arma",
    "marcá": "marca", "Marcá": "Marca",
    "juntá": "junta", "Juntá": "Junta",
    "sumá": "suma", "Sumá": "Suma",
    "revisá": "revisa", "Revisá": "Revisa",
    "listá": "lista", "Listá": "Lista",
    "sacá": "saca", "Sacá": "Saca",
    "limpiá": "limpia", "Limpiá": "Limpia",
    "avisá": "avisa", "Avisá": "Avisa",
    "planificá": "planifica", "Planificá": "Planifica",
    "reemplazá": "reemplaza", "Reemplazá": "Reemplaza",
    "instalá": "instala", "Instalá": "Instala",
    "copiá": "copia", "Copiá": "Copia",
    "completá": "completa", "Completá": "Completa",
    "conectá": "conecta", "Conectá": "Conecta",
    "referencialo": "referéncialo", "Referencialo": "Referéncialo",
    "confirmá": "confirma", "Confirmá": "Confirma",
    "chequeá": "chequea", "Chequeá": "Chequea",
    "fijá": "fija", "Fijá": "Fija",
    "exportá": "exporta", "Exportá": "Exporta",
    "ejecutá": "ejecuta", "Ejecutá": "Ejecuta",
    "reportá": "reporta", "Reportá": "Reporta",
    "separá": "separa", "Separá": "Separa",
    "esperá": "espera", "Esperá": "Espera",
    "capturá": "captura", "Capturá": "Captura",
    "nombrá": "nombra", "Nombrá": "Nombra",
    "borrá": "borra", "Borrá": "Borra",
    "ordená": "ordena", "Ordená": "Ordena",
    "evitá": "evita", "Evitá": "Evita",
    "reintentá": "reintenta", "Reintentá": "Reintenta",
    # --- verbos -ar con cambio de raiz (o->ue) ---
    "contá": "cuenta", "Contá": "Cuenta",
    "comprobá": "comprueba", "Comprobá": "Comprueba",
    # --- verbos -er/-ir regulares (imperativo) ---
    "leé": "lee", "Leé": "Lee",
    "escribí": "escribe", "Escribí": "Escribe",
    "reescribí": "reescribe", "Reescribí": "Reescribe",
    "cubrí": "cubre", "Cubrí": "Cubre",
    "abrí": "abre", "Abrí": "Abre",
    "corré": "corre", "Corré": "Corre",
    "distinguí": "distingue", "Distinguí": "Distingue",
    # --- verbos -er/-ir con cambio de raiz o forma especial ---
    "entendé": "entiende", "Entendé": "Entiende",
    "convertí": "convierte", "Convertí": "Convierte",
    "cerrá": "cierra", "Cerrá": "Cierra",
    "seguí": "sigue", "Seguí": "Sigue",
    "incluí": "incluye", "Incluí": "Incluye",
    "reuní": "reúne", "Reuní": "Reúne",
    "guardá": "guarda", "Guardá": "Guarda",
    "dejá": "deja", "Dejá": "Deja",
    # --- imperativos con enclitico (esdrujulas: llevan tilde) ---
    "marcalo": "márcalo", "Marcalo": "Márcalo",
    "dejalo": "déjalo", "Dejalo": "Déjalo",
    "aclaralo": "acláralo", "Aclaralo": "Acláralo",
    "anotalo": "anótalo", "Anotalo": "Anótalo",
    "reflejalo": "refléjalo", "Reflejalo": "Refléjalo",
    "armalo": "ármalo", "Armalo": "Ármalo",
    "guardalo": "guárdalo", "Guardalo": "Guárdalo",
    "pasalo": "pásalo", "Pasalo": "Pásalo",
    "borralo": "bórralo", "Borralo": "Bórralo",
    "usala": "úsala", "Usala": "Úsala",
    "usalas": "úsalas", "Usalas": "Úsalas",
    "agregale": "agrégale", "Agregale": "Agrégale",
    "ponele": "ponle", "Ponele": "Ponle",
    # --- presente de indicativo voseo (2a persona) ---
    "sos": "eres", "Sos": "Eres",
    "tenés": "tienes", "Tenés": "Tienes",
    "podés": "puedes", "Podés": "Puedes",
    "querés": "quieres", "Querés": "Quieres",
    "tomás": "tomas", "Tomás": "Tomas",
    "transformás": "transformas", "Transformás": "Transformas",
    "armás": "armas", "Armás": "Armas",
    "necesitás": "necesitas", "Necesitás": "Necesitas",
    "generás": "generas", "Generás": "Generas",
    "ejecutás": "ejecutas", "Ejecutás": "Ejecutas",
    "corrés": "corres", "Corrés": "Corres",
    "reportás": "reportas", "Reportás": "Reportas",
    "aplicás": "aplicas", "Aplicás": "Aplicas",
    "inventás": "inventas", "Inventás": "Inventas",
    "usás": "usas", "Usás": "Usas",
    "normalizás": "normalizas", "Normalizás": "Normalizas",
    "pegás": "pegas", "Pegás": "Pegas",
    "validás": "validas", "Validás": "Validas",
    "editás": "editas", "Editás": "Editas",
    "logueás": "logueas", "Logueás": "Logueas",
    "ponés": "pones", "Ponés": "Pones",
    "agregás": "agregas", "Agregás": "Agregas",
    "copiás": "copias", "Copiás": "Copias",
    "instalás": "instalas", "Instalás": "Instalas",
    "definís": "defines", "Definís": "Defines",
    "conectás": "conectas", "Conectás": "Conectas",
    # presente voseo -er/-ir (con cambio de raiz o forma especial)
    "pedís": "pides", "Pedís": "Pides",
    "convertís": "conviertes", "Convertís": "Conviertes",
    "producís": "produces", "Producís": "Produces",
    # imperativos irregulares (voseo -> tuteo)
    "elegí": "elige", "Elegí": "Elige",
    "poné": "pon", "Poné": "Pon",
    "hacé": "haz", "Hacé": "Haz",
    "tené": "ten", "Tené": "Ten",
    "decí": "di", "Decí": "Di",
    "vení": "ven", "Vení": "Ven",
    "andá": "anda", "Andá": "Anda",
    "subí": "sube", "Subí": "Sube",
    # --- adverbio ---
    "acá": "aquí", "Acá": "Aquí",
    "vos": "tú", "Vos": "Tú",
}

# Se ordenan las claves de mas larga a mas corta para evitar solapamientos.
_CLAVES = sorted(REEMPLAZOS.keys(), key=len, reverse=True)
_PATRON = re.compile(r"(?<!\w)(" + "|".join(re.escape(k) for k in _CLAVES) + r")(?!\w)")


def localizar(texto: str):
    conteo = {}

    def _sub(m):
        original = m.group(1)
        nuevo = REEMPLAZOS[original]
        conteo[original] = conteo.get(original, 0) + 1
        return nuevo

    return _PATRON.sub(_sub, texto), conteo


def main(argv):
    if not argv:
        print("Uso: python scripts/localizar_panameno.py <archivo1> [<archivo2> ...]")
        return 1
    total = 0
    for ruta in argv:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                original = f.read()
        except OSError as e:
            print(f"  [ERROR] No se pudo leer {ruta}: {e}")
            continue
        nuevo, conteo = localizar(original)
        cambios = sum(conteo.values())
        if nuevo != original:
            with open(ruta, "w", encoding="utf-8", newline="\n") as f:
                f.write(nuevo)
            total += cambios
            detalle = ", ".join(f"{k}->{REEMPLAZOS[k]} ({v})" for k, v in sorted(conteo.items()))
            print(f"  {ruta}: {cambios} reemplazos [{detalle}]")
        else:
            print(f"  {ruta}: sin cambios")
    print(f"Total: {total} reemplazos")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
