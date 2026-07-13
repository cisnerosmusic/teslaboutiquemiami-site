/* ============================================================
   TESLA BOUTIQUE MIAMI, backend del formulario de contacto
   Google Apps Script, se publica como Web App.
   Cuenta: ernestocisnerosmusic@gmail.com
   Envia cada consulta a los tres buzones a la vez.
   Sin DNS, sin terceros, sin servidores.

   NOTA: copia de referencia / backup versionado. La fuente que
   corre en produccion vive en script.google.com (deployment
   /exec cuya URL esta en el `action` del formulario). Si editas
   aqui, hay que reflejar el cambio alla y redesplegar como
   version nueva. NO forma parte del sitio servido (esta bajo
   _build/, excluido del deploy).
   ============================================================ */

var DESTINATARIOS = 'sales@teslaboutiquemiami.com, teslaboutiquemiami@gmail.com, ernestocisnerosmusic@gmail.com';
var ASUNTO_BASE = 'Tesla Boutique | Nueva consulta';

function doPost(e) {
  try {
    var p = (e && e.parameter) || {};

    /* 1. Honeypot: el campo oculto "company" debe llegar vacio.
       Si un bot lo llena, respondemos "ok" para no darle pistas. */
    if (p.company) return respuesta({ ok: true });

    /* 2. Trampa de tiempo: el form guarda el timestamp de carga.
       Un humano tarda mas de 3 segundos en llenar un formulario. */
    var ts = parseInt(p.ts, 10);
    if (ts && (Date.now() - ts) < 3000) return respuesta({ ok: true });

    /* 3. Validacion minima */
    var nombre   = limpiar(p.name);
    var telefono = limpiar(p.phone);
    var correo   = limpiar(p.email);
    var modelo   = limpiar(p.model);
    var servicio = limpiar(p.service);
    var mensaje  = limpiar(p.message);
    var idioma   = limpiar(p.lang) || 'en';
    var pagina   = limpiar(p.page);

    if (!nombre || (!telefono && !correo)) {
      return respuesta({ ok: false, error: 'missing_fields' });
    }

    /* 4. Cuerpo del correo */
    var cuerpo =
      'Nueva consulta desde Tesla Boutique Miami\n' +
      '------------------------------------------\n' +
      'Nombre:    ' + nombre + '\n' +
      'Telefono:  ' + (telefono || '(no dado)') + '\n' +
      'Email:     ' + (correo || '(no dado)') + '\n' +
      'Modelo:    ' + (modelo || '(no dado)') + '\n' +
      'Servicio:  ' + (servicio || '(no dado)') + '\n' +
      'Idioma:    ' + idioma + '\n' +
      'Pagina:    ' + (pagina || '(no dada)') + '\n' +
      '------------------------------------------\n\n' +
      (mensaje || '(sin mensaje)') + '\n';

    /* 5. Envio. replyTo apunta al cliente para que el jefe
       pueda responder directo desde su buzon.
       IMPORTANTE: from explicito. Sin el, Gmail usa el alias
       "Enviar como" predeterminado de la cuenta (en este caso
       ernest@ernestocisneros.art, dominio sin correo), y los
       mensajes fallan la autenticacion y caen en spam. */
    var opciones = {
      name: 'Tesla Boutique Miami',
      from: 'ernestocisnerosmusic@gmail.com'
    };
    if (correo) opciones.replyTo = correo;

    GmailApp.sendEmail(
      DESTINATARIOS,
      ASUNTO_BASE + ': ' + nombre + (modelo ? ' (' + modelo + ')' : ''),
      cuerpo,
      opciones
    );

    /* 6. Autoresponder: confirmacion amable al cliente, en su idioma.
       Solo si dejo email. Si falla, no rompe el flujo principal. */
    if (correo) {
      try {
        var esEs = (idioma === 'es');
        var asuntoCliente = esEs
          ? 'Recibimos tu consulta | Tesla Boutique Miami'
          : 'We received your inquiry | Tesla Boutique Miami';
        var cuerpoCliente = esEs
          ? ('Hola ' + nombre + ',\n\n' +
             'Tu mensaje ha sido recibido. Nos pondremos en contacto contigo a la mayor brevedad para atender tu consulta' +
             (modelo ? ' sobre tu ' + modelo : '') + '.\n\n' +
             'Si prefieres atencion inmediata, llamanos al (786) 505-6162, de lunes a viernes de 9:00 AM a 5:30 PM.\n\n' +
             'Gracias por tu preferencia.\n\n' +
             'Tesla Boutique Miami\n' +
             'Un servicio de Unlimited Wraps, Distribuidor Exclusivo XPEL\n' +
             '1835 NW 79th Ave, Doral, FL 33126\n' +
             'https://teslaboutiquemiami.com')
          : ('Hello ' + nombre + ',\n\n' +
             'Your message has been received. We will get back to you as soon as possible regarding your inquiry' +
             (modelo ? ' about your ' + modelo : '') + '.\n\n' +
             'If you prefer immediate assistance, call us at (786) 505-6162, Monday to Friday, 9:00 AM to 5:30 PM.\n\n' +
             'Thank you for choosing us.\n\n' +
             'Tesla Boutique Miami\n' +
             'A service by Unlimited Wraps, Exclusive XPEL Dealer\n' +
             '1835 NW 79th Ave, Doral, FL 33126\n' +
             'https://teslaboutiquemiami.com');

        GmailApp.sendEmail(correo, asuntoCliente, cuerpoCliente, {
          name: 'Tesla Boutique Miami',
          from: 'ernestocisnerosmusic@gmail.com'
        });
      } catch (e2) { /* la confirmacion es cortesia, no critica */ }
    }

    return respuesta({ ok: true });

  } catch (err) {
    return respuesta({ ok: false, error: 'server', detail: String(err) });
  }
}

/* Funcion de prueba: ejecutarla UNA VEZ desde el editor
   (menu desplegable de funciones > prueba > Ejecutar).
   Fuerza el permiso de Gmail y muestra cualquier error real. */
function prueba() {
  GmailApp.sendEmail(
    DESTINATARIOS,
    ASUNTO_BASE + ': PRUEBA desde el editor',
    'Si este correo llega a Recibidos de ambos buzones, el sistema esta aprobado.',
    { name: 'Tesla Boutique Miami', from: 'ernestocisnerosmusic@gmail.com' }
  );
}

/* Visita directa a la URL: responde un ping de salud. */
function doGet() {
  return respuesta({ ok: true, service: 'tesla-boutique-form' });
}

function limpiar(v) {
  return (v || '').toString().trim().substring(0, 1000);
}

function respuesta(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
