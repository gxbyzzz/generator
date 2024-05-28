# ONYX APIs 2024 | Giant free APIs for the community

**Documentación de la API del Proyecto Onyx**

`/Descripcion General`

Bienvenido a la API del Proyecto Onyx, una API diseñada para proporcionar generación de números de tarjetas de crédito para pruebas. Esta API es ideal para desarrolladores, analistas de datos y educadores que requieren datos de tarjetas de crédito para pruebas, análisis y enseñanza.

`/HOST`

| https://cc-gen-api.onrender.com |

**Rutas**

| Nombre      | Método | Descripción                                                               |
|-------------|--------|---------------------------------------------------------------------------|
| /generate/  | GET    | Generar números de tarjetas de crédito a partir de un bin |

# Ejemplos de Uso | Python

### Generar Tarjetas de Crédito

```python
import requests

params = '401658|12|2024|rnd'  # (Tus parametros)
generated_cards = requests.get(f'https://cc-gen-api.onrender.com/generate/{params}').json()
print(generated_cards)
```

**Outpout**

```JSON

{
    "result": "\nInput: 401658|12|2024|rnd\n401658xxxxxxxxxx|12|2024|123\n...",
    "Success": true
}
```

#Ejemplos de Uso | PHP
```php
<?php
$params = '401658|12|2024|rnd';  // Reemplaza con los parámetros que desees usar
$url = 'https://cc-gen-api.onrender.com/generate/' . $params;

$curl = curl_init($url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($curl);
$generated_cards = json_decode($response, true);

print_r($generated_cards);

curl_close($curl);
?>
```

**Outpout**

```JSON
{
    "result": "\nInput: 401658|12|2024|rnd\n401658xxxxxxxxxx|12|2024|123\n...",
    "Success": true
}

"About API": [
        {
            "Dev": "@gxbyzzz | @Unnamed_086",
            "Project": "Onyx APIs 2024"
        }
    ],
    "Success": true
}
```

Notas Importantes


Uso Responsable: Esta API es gratuita y se pide a los usuarios utilizarla de manera responsable para evitar sobrecargas.

Sin Fines de Lucro: Cualquier cobro por el uso de esta API no está autorizado y podría ser considerado como fraude.

Para Desarrollo y Pruebas: Ideal para pruebas de software, análisis de datos y propósitos educativos.
Información Adicional

Autores: @gxbyzzz | @Unnamed_086
Fecha de Creación: Mayo del 2024
Proyecto: Onyx APIs 2024
