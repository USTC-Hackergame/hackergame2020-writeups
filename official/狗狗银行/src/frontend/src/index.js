import React from 'react';
import ReactDOM from 'react-dom';

import App from './app';


let token = (history.state || {}).token;
if (!token) {
  token = new URL(location.href).searchParams.get('token');
  if (!token) {
    alert('请使用 Hackergame 网站上的题目链接访问');
  }
  history.replaceState({token}, '', '/');
}
if (token) {
  ReactDOM.render(<App token={token} />, document.getElementById('root'));
}
