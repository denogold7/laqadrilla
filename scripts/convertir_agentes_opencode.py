#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte los subagentes de Claude Code (.claude/agents/*.md) al formato de
opencode (.opencode/agents/*.md).

Uso:
    python scripts/convertir_agentes_opencode.py

Fuente de verdad = .claude/agents/ (editados a mano, ya localizados a panameno).
Los .opencode/agents/ son GENERADOS: para sincronizar, se vuelve a correr este
script. No editar los .opencode/agents/ a mano.

Traduccion de frontmatter:
    - name:        se descarta (opencode toma el nombre del archivo).
    - description: se conserva (clave para la auto-invocacion).
    - tools:       "Read, Write, ..." (lista Claude) -> objeto opencode en
                   minuscula. Si no hay linea `tools`, se omite (acceso total).
    - Se agrega    mode: subagent.
El cuerpo (rol/proceso/reglas) se copia tal cual.
"""

import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEN = os.path.join(RAIZ, ".claude", "agents")
DESTINO = os.path.join(RAIZ, ".opencode", "agents")

# Herramienta de Claude -> herramienta de opencode.
MAPA_TOOLS = {
    "read": "read",
    "write": "write",
    "edit": "edit",
    "glob": "glob",
    "grep": "grep",
    "bash": "bash",
    "webfetch": "webfetch",
    "websearch": "websearch",
    "task": "task",
    "list": "list",
    "patch": "patch",
}


def separar_frontmatter(texto):
    """Devuelve (dict_frontmatter, cuerpo). Parseo simple linea a linea."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", texto, re.DOTALL)
    if not m:
        raise ValueError("El archivo no tiene frontmatter YAML valido.")
    bloque, cuerpo = m.group(1), m.group(2)
    campos = {}
    for linea in bloque.splitlines():
        if ":" in linea:
            clave, valor = linea.split(":", 1)
            campos[clave.strip()] = valor.strip()
    return campos, cuerpo


def convertir_tools(valor):
    """'Read, Write, Bash' -> lista de nombres opencode en minuscula."""
    tools = []
    for parte in valor.split(","):
        nombre = parte.strip().lower()
        if not nombre:
            continue
        tools.append(MAPA_TOOLS.get(nombre, nombre))
    return tools


def escapar_yaml(valor):
    """Encierra la description en comillas dobles de forma segura."""
    return '"' + valor.replace("\\", "\\\\").replace('"', '\\"') + '"'


def construir_frontmatter(campos):
    lineas = ["---"]
    desc = campos.get("description", "").strip()
    if desc:
        lineas.append(f"description: {escapar_yaml(desc)}")
    lineas.append("mode: subagent")
    if "tools" in campos and campos["tools"].strip():
        tools = convertir_tools(campos["tools"])
        if tools:
            lineas.append("tools:")
            for t in tools:
                lineas.append(f"  {t}: true")
    # Sin linea `tools` en el origen => acceso total en opencode (no se declara).
    lineas.append("---")
    return "\n".join(lineas)


def main():
    if not os.path.isdir(ORIGEN):
        print(f"[ERROR] No existe {ORIGEN}")
        return 1
    os.makedirs(DESTINO, exist_ok=True)

    archivos = sorted(f for f in os.listdir(ORIGEN) if f.endswith(".md"))
    if not archivos:
        print(f"[ERROR] No hay agentes en {ORIGEN}")
        return 1

    for nombre in archivos:
        ruta_origen = os.path.join(ORIGEN, nombre)
        with open(ruta_origen, "r", encoding="utf-8") as f:
            texto = f.read()
        try:
            campos, cuerpo = separar_frontmatter(texto)
        except ValueError as e:
            print(f"  [SALTADO] {nombre}: {e}")
            continue

        frontmatter = construir_frontmatter(campos)
        cuerpo = cuerpo.rstrip("\n") + "\n"
        salida = frontmatter + "\n\n" + cuerpo

        ruta_destino = os.path.join(DESTINO, nombre)
        with open(ruta_destino, "w", encoding="utf-8", newline="\n") as f:
            f.write(salida)

        tools_info = campos.get("tools", "TODAS (acceso total)")
        print(f"  {nombre}: OK  [tools: {tools_info}]")

    print(f"\nGenerados {len(archivos)} agentes en .opencode/agents/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
