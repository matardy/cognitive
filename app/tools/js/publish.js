// Cargar el SDK de AWS
const AWS = require('aws-sdk');

// Configurar AWS para usar sin credenciales
AWS.config.update({
  region: 'us-east-1'
});

// Crear un objeto SNS
const sns = new AWS.SNS({
  apiVersion: '2010-03-31'
});

// Obtener argumentos de la línea de comandos
const args = process.argv.slice(2);
const topicArn = args[0];
const subject = args[1];
const message = args[2];

if (!topicArn || !subject || !message) {
  console.error('Se requieren los argumentos: topicArn, subject y message');
  process.exit(1);
}

// Función para publicar un mensaje
function publishMessage(topicArn, message, subject) {
  const params = {
    Message: message,
    Subject: subject,
    TopicArn: topicArn
  };

  sns.publish(params, (err, data) => {
    if (err) {
      console.error("Error al publicar mensaje:", err);
    } else {
      console.log("Mensaje publicado:", data);
    }
  });
}

// Publicar el mensaje
publishMessage(topicArn, message, subject);
