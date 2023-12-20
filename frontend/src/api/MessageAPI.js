import axios from "axios";
import { BASE_URL } from "../config";


const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

const GET_MESSAGES = (msg_id="", params={}) => api.get(msg_id + "/", {params: params});
const SEND_MESSAGE = (data) => api.post("/", data);
const CONFIRM_MESSAGE = (data) => api.put("/", data);

export {
    api,
    GET_MESSAGES,
    SEND_MESSAGE,
    CONFIRM_MESSAGE
};
