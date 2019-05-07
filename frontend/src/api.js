import axios from 'axios';
import { apiUrl } from './config';

const api = axios.create({ baseURL: apiUrl });

export default {
  getHashtags(data) {
    return api.get('/hashtags')
      .then(r => r.data);
  },
};

