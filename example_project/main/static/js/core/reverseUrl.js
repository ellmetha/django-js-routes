/* eslint-disable */

const routes = {"home": "/", "home_with_arg": "/home/<year>/", "home_with_two_args": "/home/<year>/<month>/", "home_with_re_arg": "/home/<year>/", "home_with_arg_without_converter": "/home/<slug>/"};
const reverseUrl  = (function () {
  return function(name) {
    var url = routes[name];

    if (!url) {
      throw "URL '" + name + "' not found.";
    }

    const tokens = url.match(/<\w*>/g);
    if (!tokens && arguments[1] !== undefined) {
      throw "URL '" + name + "' does not expect any arguments.";
    }

    if (typeof (arguments[1]) == 'object' && !Array.isArray(arguments[1])) {
      for (var i = 0; i < tokens.length; i += 1) {
        const token = tokens[i];
        const argName = token.slice(1, -1);
        const argValue = arguments[1][argName];

        if (argValue === undefined) {
          throw "Argument '" + argName + "' not provided.";
        }
        url = url.replace(token, argValue);
      }
    } else if (arguments[1] !== undefined) {
      const argsArray = Array.isArray(arguments[1]) ? arguments[1] : Array.prototype.slice.apply(arguments, [1, arguments.length]);
      if (tokens.length !== argsArray.length) {
        throw "Wrong number of arguments ; expected " + tokens.length + " arguments.";
      }

      for (var i = 0; i < tokens.length; i += 1) {
        const token = tokens[i];
        const argValue = argsArray[i];
        url = url.replace(token, argValue);
      }
    }

    return url;
  };
})();


export default reverseUrl;
