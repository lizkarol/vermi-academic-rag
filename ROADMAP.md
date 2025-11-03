# Roadmap del Proyecto

Este documento describe los hitos de desarrollo y evolución del dataset `vermi-academic-rag`.

## Hitos por Fase

```
┌────────────────┬───────────┬──────────────┬──────────────┬──────────┐
│ Fase           │ Chunks    │ Cobertura(%) │ Fuentes      │ Tiempo   │
├────────────────┼───────────┼──────────────┼──────────────┼──────────┤
│ MVP            │ 100-150   │ 70%          │ 5-10         │ 3-4 sem  │
│ Expansión      │ 200-300   │ 90%          │ 20+          │ 4-6 sem  │
│ Refinamiento   │ 300-400   │ 100%         │ 30+          │ 3-4 sem  │
│ Mantenimiento  │ 400+      │ 100%         │ Dinámico     │ 6 meses  │
└────────────────┴───────────┴──────────────┴──────────────┴──────────┘
```

## Criterios para Avanzar de Fase

Para pasar a la siguiente fase, se deben cumplir los siguientes criterios:

-   **Cobertura taxonómica:** Alcanzar el umbral de cobertura especificado para la fase.
-   **Conflictos documentados:** ≥80% de los conflictos conocidos deben estar documentados (a partir de la fase de Expansión).
-   **Redundancia:** El porcentaje de chunks redundantes debe ser inferior al 5%.
-   **Deprecación:** El porcentaje de chunks obsoletos debe ser inferior al 5%.
-   **Métricas de Test (RAGAs):** El test set debe superar los umbrales definidos, por ejemplo, `Context Relevance ≥ 80%`.

El plan futuro se centra en la expansión continua del dataset, la mejora de la calidad a través del feedback de la comunidad y la integración de nuevas fuentes de conocimiento, siempre bajo la política BYOS.

