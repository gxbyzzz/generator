# Credit Card Generator API

Esta es una API REST para generar números de tarjetas de crédito aleatorios basados en un BIN dado, mes, año y CVV. La API está construida con Flask y puede ser hospedada en Render con Cloudflare para mayor seguridad.

## Endpoints

### Generar Números de Tarjetas de Crédito

**URL**: `/generate`

**Método**: `POST`

**Cuerpo de la Solicitud**:
```json
{
  "bin": "string",
  "mm": "string",  // Opcional, por defecto es 'rnd'
  "yy": "string",  // Opcional, por defecto es 'rnd'
  "cvv": "string"  // Opcional, por defecto es 'rnd'
}
