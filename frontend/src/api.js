import axios from 'axios';
import { apiUrl } from './config';

const api = axios.create({ baseURL: apiUrl });

export default {
  getHashtags() {
    return api.get('/hashtags')
      .then(r => r.data);
  },
  getDates() {
    return api.get('/dates')
      .then(r => r.data);
  },
  postHashtagsDate(data) {
    return api.post('/hashtags_date', data)
      .then(r => r.data);
  },
  postPlots(data) {
    return api.post('/plots', data)
      .then(r => r.data);
  },
  postSpikeDetection(data){
    return api.post('/get_spike_detection', data)
      .then(r => r.data);
  }
};

