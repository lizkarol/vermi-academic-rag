# Preguntas Frecuentes (FAQ)

### P: ¿Puedo subir un PDF al repo?

**R:** No. PDFs tienen copyright; distribuirlos viola DMCA y derechos de autor. Usa el flujo BYOS: descárgalo localmente, parafrasea en JSON, sube solo el JSON con referencias DOI/URL.

### P: ¿Qué pasa si quiero usar contenido CC-BY?

**R:** ¡Excelente! FAO, por ejemplo, desde 2024 publica bajo CC-BY. Puedes incluir adaptaciones con atribución explícita. Añade campo `license_note: "CC-BY 4.0 (FAO 2024)"` en el chunk.

### P: ¿Cómo genero chunks si no sé programar?

**R:** Usa la guía manual en `generate_cards_local.md`. Copia tu .md privado, pégalo en Gemini/ChatGPT, usa el prompt dado, copia el JSON resultado. No necesitas código.

### P: ¿Es esto legal?

**R:** Sí. Parafrasear + citar fuentes es fair use. No redistribuir copyrighted material + siempre atribuir = DMCA-safe y éticamente correcto.

### P: ¿Puedo forkear para mi propio proyecto?

**R:** Absolutamente. El código y método son MIT. Ajusta la taxonomía (p.ej., para otro dominio), usa tus propias fuentes privadas, genera chunks, y tienes tu dataset. El kit es reutilizable.

### P: ¿Cuánto cuesta generar chunks con LLMs?

**R:** ~$50–100 para generar 300–500 chunks usando GPT-4 o Gemini batch. Es un costo one-time por versión.

### P: ¿Puede cualquiera contribuir chunks?

**R:** Sí, vía Pull Request. Deben seguir BYOS: parafrasear, citar, validar. CI + revisión manual garantiza calidad.
