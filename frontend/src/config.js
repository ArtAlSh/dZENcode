const BASE_URL = 'http://0.0.0.0:8000';
const BASE_WS = "ws://0.0.0.0:8000/ws/chat/";

const ALLOWED_FILE_FORMATS = ["txt"];
const MAX_FILE_SIZE = 100000;   // bites

const ALLOWED_IMAGE_FORMATS = ["jpg", "gif", "png"];
const MAX_IMAGE_HEIGHT = 240;   // px
const MAX_IMAGE_WIDTH = 320;    // px

export {
    BASE_URL,
    BASE_WS,
    ALLOWED_FILE_FORMATS,
    MAX_FILE_SIZE,
    ALLOWED_IMAGE_FORMATS,
    MAX_IMAGE_HEIGHT,
    MAX_IMAGE_WIDTH,
};
