/* eslint-env browser */
import 'regenerator-runtime/runtime';

import controllers from './controllers';
import DOMRouter from './core/DOMRouter';


const router = new DOMRouter(controllers);

document.addEventListener('DOMContentLoaded', () => {
  // Initializes the DOM router. The DOM router is used to execute specific portions of JS code for
  // each specific page.
  router.init();
});
