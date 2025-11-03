# Dominio de Conocimiento: Vermicompostaje Doméstico

Este documento describe el dominio específico que cubre el dataset, basado en las necesidades del proyecto **VermiKhipu**.

---

## 🎯 Alcance del Proyecto

### Contexto: VermiKhipu

VermiKhipu es un sistema de vermicompostaje doméstico asistido por IA que:
- Opera **100% offline** con interacción por voz en español
- Escala doméstica: **1-5 kg/semana** de residuos orgánicos
- Control automatizado de hábitat (temperatura, humedad)
- Dosificación inteligente de materiales
- Asistente conversacional basado en RAG local

### Objetivo del Dataset

Proporcionar una **base de conocimiento estructurada y verificable** sobre vermicompostaje doméstico para:
1. Responder preguntas del usuario sobre el proceso
2. Fundamentar decisiones del sistema de control
3. Diagnosticar problemas y sugerir soluciones
4. Educar sobre mejores prácticas

---

## 📚 Taxonomía del Conocimiento

### Categoría 1: BIOLOGÍA (BIO)

**Objetivo:** Comprender los organismos del sistema y sus necesidades.

#### Subcategorías Prioritarias:

**1.1 Especies de Lombrices**
- Eisenia fetida (lombriz roja californiana)
- Eisenia andrei (lombriz del estiércol)
- Diferencias entre especies
- Compatibilidad y convivencia

**1.2 Fisiología**
- Respiración cutánea y requerimientos de oxígeno
- Digestión y microbiota intestinal
- Reproducción: ciclo de vida, cocones, madurez sexual
- Metabolismo y tasa de consumo

**1.3 Comportamiento**
- Respuesta a luz (fotofobia)
- Respuesta a temperatura y humedad
- Patrones de migración vertical
- Comportamiento gregario vs individual

**1.4 Condiciones Letales**
- Límites de temperatura (min/max)
- Rangos de humedad críticos
- Niveles de pH tóxicos
- Sustancias químicas dañinas

**1.5 Señales de Estrés**
- Indicadores de malestar (escape, agrupamiento)
- Síntomas de enfermedad
- Mortalidad anormal: causas y diagnóstico

**Ejemplo de chunk BIO:**
```json
{
  "category": "BIO",
  "subcategory": "Rangos Térmicos",
  "primary_entity": "Eisenia fetida",
  "source_field": "Las lombrices Eisenia fetida operan en un rango térmico de 10-30°C, con óptimo entre 20-25°C. Por debajo de 10°C reducen actividad metabólica significativamente, y sobre 30°C entran en estrés térmico con riesgo de mortalidad si persiste >48 horas.",
  "keywords": ["temperatura", "rango óptimo", "estrés térmico", "metabolismo"]
}
```

---

### Categoría 2: PROCESO (PROC)

**Objetivo:** Entender la cinética y parámetros del vermicompostaje.

#### Subcategorías Prioritarias:

**2.1 Relación C:N (Carbono:Nitrógeno)**
- Concepto y relevancia bioquímica
- Rangos óptimos (típicamente 20:1 a 30:1)
- Efectos de desbalance (exceso C o N)
- Métodos de ajuste

**2.2 pH**
- Rangos funcionales (6.0-8.0)
- Efectos de acidez (<6.0): causas y soluciones
- Efectos de alcalinidad (>8.5): menos común
- Materiales buffer (cáscara de huevo, cal)

**2.3 Humedad**
- Rangos operativos (60-80%)
- Métodos de medición (capacitivo, peso, táctil)
- Efectos de exceso: anaerobiosis, lixiviados
- Efectos de deficiencia: deshidratación, actividad reducida

**2.4 Temperatura**
- Rango óptimo del proceso (15-25°C)
- Diferencia con compostaje termofílico (>55°C)
- Control de temperatura en climas extremos
- Temperatura vs velocidad de degradación

**2.5 Aireación**
- Requerimientos de oxígeno
- Métodos de aireación (mezcla, volteo)
- Frecuencia según condiciones
- Indicadores de anaerobiosis (olor)

**2.6 Tiempo de Procesamiento**
- Variables que afectan velocidad
- Tiempo típico por tipo de residuo
- Precompostaje vs vermicompostaje
- Indicadores de madurez del humus

**Ejemplo de chunk PROC:**
```json
{
  "category": "PROC",
  "subcategory": "Relación C:N",
  "primary_entity": "balance carbono-nitrógeno",
  "source_field": "Una relación C:N entre 20:1 y 25:1 favorece la degradación óptima. Relaciones >30:1 ralentizan el proceso por deficiencia de nitrógeno para síntesis microbiana, mientras que <15:1 pueden generar pérdidas de nitrógeno por volatilización de amoníaco.",
  "keywords": ["C:N", "carbono", "nitrógeno", "balance", "degradación"]
}
```

---

### Categoría 3: MATERIALES (MAT)

**Objetivo:** Clasificar residuos orgánicos y sus propiedades.

#### Subcategorías Prioritarias:

**3.1 Residuos Orgánicos Verdes (alto N)**
- Restos de frutas y verduras
- Posos de café, té
- Césped fresco
- Propiedades: pH, C:N, velocidad degradación

**3.2 Materiales Secos (alto C)**
- Cartón corrugado
- Papel periódico
- Hojas secas
- Funciones: absorción, estructura, balance C:N

**3.3 Materiales Buffer**
- Cáscara de huevo molida
- Carbonato de calcio
- Ceniza de madera (con precaución)
- Dosis y frecuencia

**3.4 Materiales Restringidos**
- Cítricos: acidez, aceites esenciales
- Cebollas y ajos: compuestos azufrados
- Grasas y aceites: rancidez, anaerobiosis
- Carnes y lácteos: olores, plagas

**3.5 Materiales Prohibidos**
- Plásticos y sintéticos
- Vidrio y metales
- Heces de mascotas (parásitos)
- Residuos con pesticidas

**Ejemplo de chunk MAT:**
```json
{
  "category": "MAT",
  "subcategory": "Materiales Restringidos",
  "primary_entity": "cítricos",
  "source_field": "Los cítricos (limón, naranja, toronja) pueden agregarse en cantidades moderadas (<10% del total) pero su acidez natural (pH 2-4) y aceites esenciales en la cáscara pueden estresar las lombrices si se concentran. Se recomienda mezclar con materiales secos y evitar grandes cantidades de una vez.",
  "keywords": ["cítricos", "acidez", "aceites esenciales", "restricción", "moderación"]
}
```

---

### Categoría 4: OPERACIÓN (OPER)

**Objetivo:** Guiar intervenciones y control del sistema.

#### Subcategorías Prioritarias:

**4.1 Riego**
- Cuándo regar: indicadores (sensor, tacto)
- Cantidad de agua según condiciones
- Frecuencia típica
- Riesgos de exceso y deficiencia

**4.2 Mezcla/Aireación**
- Cuándo mezclar: frecuencia, eventos que lo requieren
- Técnicas de mezcla sin dañar lombrices
- Profundidad de mezcla
- Indicadores de necesidad

**4.3 Dosificación de Materiales**
- Alimentación: frecuencia, cantidades por ciclo
- Compensación C:N: cuándo agregar secos
- Corrección de pH: dosificación de buffer
- Evitar sobrecarga

**4.4 Control de Plagas**
- Moscas de fruta: prevención y control
- Hormigas: causas y soluciones
- Ácaros: identificación y gestión
- Métodos no tóxicos

**4.5 Diagnóstico de Problemas**
- Olores: tipos, causas, acciones
- Escape de lombrices: por qué y qué hacer
- Actividad reducida: posibles causas
- Problemas de humedad o temperatura

**4.6 Cosecha**
- Métodos de separación (luz, mallas, tubo rotativo)
- Frecuencia de cosecha
- Signos de humus maduro
- Manejo de lombrices durante cosecha

**Ejemplo de chunk OPER:**
```json
{
  "category": "OPER",
  "subcategory": "Riego",
  "primary_entity": "control de humedad",
  "source_field": "El riego debe realizarse cuando la humedad cae por debajo del 60%, indicado por sustrato que se siente seco al tacto o lecturas del sensor capacitivo <40%. Se recomienda riego por pulsos cortos con periodos de observación para evitar saturación, manteniendo humedad objetivo entre 65-75%.",
  "keywords": ["riego", "humedad", "sensor", "frecuencia", "pulsos"]
}
```

---

### Categoría 5: PRODUCTO (PROD)

**Objetivo:** Caracterizar y usar el producto final.

#### Subcategorías Prioritarias:

**5.1 Humus de Lombriz**
- Características físicas (color, textura, olor)
- Indicadores de calidad y madurez
- Composición nutricional típica (NPK, micronutrientes)
- Propiedades biológicas (microbiota)

**5.2 Aplicaciones del Humus**
- Enmienda de suelos: dosis por tipo de suelo
- Sustrato para macetas: proporciones de mezcla
- Té de humus: preparación y usos
- Compatibilidad con plantas

**5.3 Lixiviados**
- Composición y diferencias con té de humus
- Usos: fertilizante líquido, diluciones
- Precauciones: olor, patógenos potenciales
- Almacenamiento

**5.4 Almacenamiento y Conservación**
- Condiciones óptimas de almacenamiento
- Duración: vida útil del humus
- Pérdida de propiedades con el tiempo
- Empaquetado

**Ejemplo de chunk PROD:**
```json
{
  "category": "PROD",
  "subcategory": "Indicadores de Madurez",
  "primary_entity": "humus maduro",
  "source_field": "El humus maduro presenta color marrón oscuro a negro, textura granular uniforme, olor a tierra húmeda (no amoniacal ni pútrido), y ausencia de material orgánico reconocible. Retiene humedad sin estar saturado y tiene pH cercano a neutro (6.5-7.5).",
  "keywords": ["humus maduro", "color", "textura", "olor", "pH", "calidad"]
}
```

---

## 🔍 Criterios de Inclusión/Exclusión

### ✅ Conocimiento DENTRO del alcance:

- Vermicompostaje doméstico (1-5 kg/semana)
- Especies Eisenia fetida y Eisenia andrei
- Residuos orgánicos domésticos típicos
- Control de parámetros con herramientas básicas
- Soluciones de bajo costo y baja tecnología
- Contexto urbano/periurbano

### ❌ Conocimiento FUERA del alcance:

- Vermicompostaje industrial (>1 ton/día)
- Otras especies de lombrices (Lumbricus terrestris, etc.)
- Gestión de residuos municipales
- Tratamiento químico/pesticidas
- Equipamiento industrial costoso
- Normativas comerciales/exportación

---

## 📊 Cobertura Objetivo por Categoría

| Categoría  | Subcategorías | Chunks Objetivo | Prioridad |
|-----------|---------------|----------------|-----------|
| BIOLOGÍA  | 5             | 40-60          | ALTA      |
| PROCESO   | 6             | 60-80          | CRÍTICA   |
| MATERIALES| 5             | 50-70          | ALTA      |
| OPERACIÓN | 6             | 30-40          | MEDIA     |
| PRODUCTO  | 4             | 20-30          | MEDIA     |
| **TOTAL** | **26**        | **200-280**    |           |

### Justificación de Prioridades:

1. **PROCESO (crítica):** Fundamenta todas las decisiones del sistema
2. **BIOLOGÍA y MATERIALES (alta):** Base para diagnóstico y recomendaciones
3. **OPERACIÓN y PRODUCTO (media):** Importantes pero menos urgentes para MVP

---

## 🎓 Fuentes Deseadas

### Prioritarias:
- Manuales técnicos de FAO sobre vermicompostaje
- Papers sobre Eisenia fetida/andrei (fisiología, comportamiento)
- Estudios de parámetros óptimos (C:N, pH, humedad)
- Guías de materiales orgánicos y restricciones

### Secundarias:
- Experiencias de usuario validadas (blogs, foros especializados)
- Tesis de universidades agrícolas
- Documentos de extensión agrícola (INTA, INIA, etc.)
- Libros de referencia (ej: "Vermiculture Technology" - Edwards et al.)

---

## 🔗 Referencias

Para más detalles sobre:
- **Esquema de datos:** Ver [`DATA_SCHEMA.md`](DATA_SCHEMA.md)
- **Ejemplos completos:** Ver `dataset/chunks_enriched/chunks_enriched_v1.0.jsonl`
- **Métricas de calidad:** Ver [`QUALITY_METRICS.md`](QUALITY_METRICS.md)
- **Contexto del robot:** Ver documentos adjuntos del proyecto VermiKhipu

---

**Última actualización:** 2025-11-03  
**Versión:** 1.0
