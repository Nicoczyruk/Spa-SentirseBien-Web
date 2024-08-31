const apiKey = '2e3c64844a3edfaa329ad539c9850deb'; // Reemplaza con tu clave de API de GNews
const query = 'spa bienestar'; // Múltiples palabras clave separadas por espacios
const url = `https://gnews.io/api/v4/search?q=${encodeURIComponent(query)}&lang=es&token=${apiKey}`;

console.log('Iniciando solicitud...');

fetch(url)
  .then(response => {
    console.log('Respuesta recibida:', response);
    if (!response.ok) {
      throw new Error('Error en la respuesta de la API');
    }
    return response.json();
  })
  .then(data => {
    console.log('Datos obtenidos:', data);
    const newsSection = document.getElementById('news-section');
    newsSection.innerHTML = ''; // Limpiar cualquier contenido previo

    if (data.articles.length === 0) {
      newsSection.innerHTML = '<p>No se encontraron noticias.</p>';
    } else {
      data.articles.forEach(article => {
        const articleElement = document.createElement('div');
        articleElement.classList.add('news-article'); // Añade una clase para aplicar estilos
        articleElement.innerHTML = `
          ${article.image ? `<img src="${article.image}" alt="${article.title}" class="news-image">` : ''}
          <h3><br>${article.title}</h3>
          <p>${article.description}</p>
          <a href="${article.url}" target="_blank">Leer más</a>
        `;
        newsSection.appendChild(articleElement);
      });
    }
  })
  .catch(error => {
    console.error('Error al obtener las noticias:', error);
    const newsSection = document.getElementById('news-section');
    newsSection.innerHTML = '<p>Hubo un error al cargar las noticias. Inténtalo de nuevo más tarde.</p>';
  });
