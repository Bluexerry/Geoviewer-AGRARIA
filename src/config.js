/* Written by Ye Liu */

// Mapbox-GL library access token — set REACT_APP_MAPBOX_TOKEN in your .env file
const ACCESS_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;

if (!ACCESS_TOKEN) {
    console.error('REACT_APP_MAPBOX_TOKEN is not set. Please add it to your .env file.');
}

export { ACCESS_TOKEN };
