import React from 'react';
import ReactDOM from 'react-dom';

import App from './containers/App';
import './index.scss';
import "react-datepicker/dist/react-datepicker.css";

const rootElement = document.getElementById('root');
ReactDOM.render(<App />, rootElement);

