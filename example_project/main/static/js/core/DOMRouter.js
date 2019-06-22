class DOMRouter {
  constructor(controllers) {
    this.controllers = (controllers === undefined) ? {} : controllers;
  }

  /**
   * Executes the given action associated with the considered controller.
   * @param {String} controller - The codename of the controller.
   * @param {String} action - The name of the action to execute.
   */
  execAction(controller, action) {
    if (controller !== '' && this.controllers[controller]
        && typeof this.controllers[controller][action] === 'function') {
      this.controllers[controller][action]();
    }
  }

  /**
   * Initializes the router object.
   */
  init() {
    if (document.body) {
      const { body } = document;
      const controller = body.getAttribute('data-controller');
      const action = body.getAttribute('data-action');

      if (controller) {
        this.execAction(controller, 'init');
        this.execAction(controller, action);
      }
    }
  }
}


export default DOMRouter;
