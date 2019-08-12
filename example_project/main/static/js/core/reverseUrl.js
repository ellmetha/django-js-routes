/* eslint-disable */

const routes = {"home": "/", "home_with_arg": "/home/<year>/", "home_with_two_args": "/home/<year>/<month>/", "home_with_re_arg": "/home/<year>/", "home_with_arg_without_converter": "/home/<slug>/"};
const reverseUrl  = function(urlName) {
  var url = routes[urlName];
  if (!url) {
    throw "URL '" + urlName + "' was not found.";
  }

  const args = arguments;
  const argTokens = url.match(/<\w*>/g);
  if (!argTokens && args[1] !== undefined) {
    throw "Invalid URL lookup: URL '" + urlName + "' does not expect any arguments.";
  }

  if (typeof (args[1]) == 'object' && !Array.isArray(args[1])) {
    argTokens.forEach(function(token) {
      const argName = token.slice(1, -1);
      const argValue = args[1][argName];
      if (argValue === undefined) {
        throw "Invalid URL lookup: Argument '" + argName + "' was not provided.";
      }

      url = url.replace(token, argValue);
    });
  } else if (args[1] !== undefined) {
    const argsArray = Array.isArray(args[1]) ? args[1] : Array.prototype.slice.apply(args, [1, args.length]);
    if (argTokens.length !== argsArray.length) {
      throw "Invalid URL lookup: Wrong number of arguments ; expected " + argTokens.length + " arguments.";
    }

    argTokens.forEach(function(token, i) {
      const argValue = argsArray[i];
      url = url.replace(token, argValue);
    });
  }

  return url;
};


export default reverseUrl;
